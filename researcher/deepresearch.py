import uuid
import asyncio
from langchain_community.agent_toolkits.load_tools import load_tools
#from langchain_community.utilities import GoogleSerperAPIWrapper
config = {
    "thread_id": str(uuid.uuid4()),
    "search_api": "serper",
}
from dotenv import load_dotenv

# --- Cargar variables de entorno ---
load_dotenv()
from typing import List, Literal, Annotated, TypedDict
from pydantic import BaseModel, Field
import operator

class Section(BaseModel):
    name: str = Field(..., description="Name for this section of the report.")
    description: str = Field(..., description="Scope of research for this section.")
    content: str = Field(..., description="The written content of the section.")

class Sections(BaseModel):
    sections: List[str] = Field(..., description="Sections of the report.")

class Introduction(BaseModel):
    name: str
    content: str

class Conclusion(BaseModel):
    name: str
    content: str

class SearchQuery(BaseModel):
    search_query: str

class ReportStateOutput(TypedDict):
    final_report: str

from langgraph.graph import MessagesState

class ReportState(MessagesState):
    sections: list[str]
    completed_sections: Annotated[list, operator.add]
    final_report: str

class SectionState(MessagesState):
    section: str
    completed_sections: list[Section]

class SectionOutputState(TypedDict):
    completed_sections: list[Section]

import time

from langchain_core.tools import tool

@tool
class SectionTool(BaseModel):
    name: str = Field(description="Name for this section of the report.")
    description: str = Field(description="Research scope for this section of the report.")
    content: str = Field(description="The content of the section.")

@tool
class SectionsTool(BaseModel):
    sections: List[str] = Field(description="Sections of the report.")

@tool
class IntroductionTool(BaseModel):
    name: str = Field(description="Name for the report.")
    content: str = Field(description="The introduction text.")

@tool
class ConclusionTool(BaseModel):
    name: str = Field(description="Name for the conclusion of the report.")
    content: str = Field(description="The conclusion text.")

from dataclasses import dataclass, fields
from typing import Optional
from enum import Enum

class SearchAPI(Enum):
    TAVILY = "tavily"
    DUCKDUCKGO = "duckduckgo"
    SERPER = "serper"
@dataclass(kw_only=True)
class Configuration:
    # Keep what you actually use
    search_api: SearchAPI = SearchAPI.SERPER  # NEEDED - used by get_search_tool()

    @classmethod
    def from_runnable_config(cls, config: Optional[dict] = None) -> "Configuration":
        configurable = config.get("configurable", {}) if config else {}
        values = {
            f.name: configurable.get(f.name)
            for f in fields(cls) if f.init
        }
        return cls(**{k: v for k, v in values.items() if v is not None})

def get_config_value(value):
    """Return the value from enums/dicts/str as needed."""
    if isinstance(value, str):
        return value
    elif isinstance(value, dict):
        return value
    else:
        return value.value  # For Enums like SearchAPI.TAVILY
    
SUPERVISOR_INSTRUCTIONS = f"""You are a research supervisor. Follow these steps:

1. **Initial Research**: Use `{config["search_api"]}` to understand the user's topic.
2. **Clarify**: If the user's request is ambiguous or could be improved, ALWAYS ask the user follow-up questions to refine the scope. Do NOT proceed to research or tool calls until the user has answered your clarifying questions.
3. **Structure**: Use `SectionsTool` to define 3-5 research sections (no intro/conclusion).
4. **Finalize**: When sections return, use `IntroductionTool` then `ConclusionTool`.

Always check your message history to avoid duplicate tool calls."""

RESEARCH_INSTRUCTIONS = """Complete this section: {section_description}

Required steps:
1. **Search 3+ times** using `"""+config["search_api"]+"""` for comprehensive coverage
2. **Call `SectionTool`** with:
  - name: Section title
  - description: Brief research scope
  - content: 150-word markdown section starting with "## Title" and ending with "### Sources" listing 4+ URLs

You MUST call `SectionTool` to complete your work. Do not stop without submitting content."""



def get_search_tool(config: dict):
    cfg = Configuration.from_runnable_config(config)
    api = get_config_value(cfg.search_api)
    if api == "tavily":
        pass
        #return tavily_search
    elif api == "duckduckgo":
        raise ValueError(f"Search API '{api}' not supported.")
        #return  duckduckgo_search
    elif api == "serper":
        import os
        
        return  load_tools(["google-serper"], serper_api_key=os.environ["SERPER_API_KEY"])[0]
    else:
        raise ValueError(f"Search API '{api}' not supported.")

def get_supervisor_tools(config: dict):
    search = get_search_tool(config)
    tools = [search, SectionsTool, IntroductionTool, ConclusionTool]
    return tools, {t.name: t for t in tools}

def get_research_tools(config: dict):
    search = get_search_tool(config)
    tools = [search, SectionTool]
    return tools, {t.name: t for t in tools}


from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, Send
from langgraph.graph import MessagesState
from typing import Literal
from langchain_openai import AzureChatOpenAI

# --- Define LangGraph State Nodes ---

async def supervisor(state: ReportState, config: dict):
    messages = state["messages"]
    cfg = Configuration.from_runnable_config(config)
    llm =AzureChatOpenAI(
        azure_deployment="gpt-4o-mini-alex-udesa",
        api_version="2023-05-15",
        temperature=0.3,
        model_name="gpt-4o-mini",
        azure_endpoint="https://abodn-maeidvlk-eastus2.cognitiveservices.azure.com/",
        api_key = "BwuJbV7aiCeu4F6XIVDmPOHyomhEPxVl1LKzqj5KQqQhzwmMOX6MJQQJ99BEACHYHv6XJ3w3AAAAACOGk2VZ"
        )

    # CRITICAL: Check if research is complete before proceeding to intro/conclusion
    if state.get("completed_sections") and not state.get("final_report"):
        research_complete_message = {
            "role": "user",
            "content": "Research is complete. Now write the introduction and conclusion for the report. Here are the completed main body sections: \n\n" + "\n\n".join([s.content for s in state["completed_sections"]])
        }
        messages = messages + [research_complete_message]

    tools, _ = get_supervisor_tools(config)

    return {
        "messages": [
            await llm.bind_tools(tools, parallel_tool_calls=False).ainvoke(
                [{"role": "system", "content": SUPERVISOR_INSTRUCTIONS}] + messages
            )
        ]
    }

async def supervisor_tools(state: ReportState, config: dict) -> Command[Literal["supervisor", "research_team", "__end__"]]:
    result = []
    sections = []
    intro = None
    conclusion = None

    _, tools = get_supervisor_tools(config)

    for call in state["messages"][-1].tool_calls:
        tool = tools[call["name"]]
        obs = await tool.ainvoke(call["args"]) if hasattr(tool, "ainvoke") else tool.invoke(call["args"])
        result.append({"role": "tool", "content": str(obs), "name": call["name"], "tool_call_id": call["id"]})

        if call["name"] == "SectionsTool":
            sections = obs.sections  # This is list[str] from your SectionsTool
        elif call["name"] == "IntroductionTool":
            intro = f"# {obs.name}\n\n{obs.content}" if not obs.content.startswith("# ") else obs.content
        elif call["name"] == "ConclusionTool":
            conclusion = f"## {obs.name}\n\n{obs.content}" if not obs.content.startswith("## ") else obs.content

    if sections:
        # Send sections to research team - this will populate completed_sections when research is done
        return Command(goto=[Send("research_team", {"section": s}) for s in sections], update={"messages": result})
    elif intro:
        # Store introduction and guide to write conclusion
        result.append({"role": "user", "content": "Introduction written. Now write a conclusion section."})
        return Command(goto="supervisor", update={"final_report": intro, "messages": result})
    elif conclusion:
        # Assemble final report
        intro = state.get("final_report", "")
        body = "\n\n".join([s.content for s in state["completed_sections"]])
        final = f"{intro}\n\n{body}\n\n{conclusion}"
        result.append({"role": "user", "content": "Report is complete."})
        return Command(goto="supervisor", update={"final_report": final, "messages": result})
    else:
        # Default case (search tools, etc.)
        return Command(goto="supervisor", update={"messages": result})



async def supervisor_should_continue(state: ReportState) -> Literal["supervisor_tools", END]:
    return "supervisor_tools" if state["messages"][-1].tool_calls else END

async def research_agent(state: SectionState, config: dict):
    cfg = Configuration.from_runnable_config(config)
    llm =AzureChatOpenAI(
        azure_deployment="gpt-4o-mini-alex-udesa",
        api_version="2023-05-15",
        temperature=0.3,
        model_name="gpt-4o-mini",
        azure_endpoint="https://abodn-maeidvlk-eastus2.cognitiveservices.azure.com/",
        api_key = "BwuJbV7aiCeu4F6XIVDmPOHyomhEPxVl1LKzqj5KQqQhzwmMOX6MJQQJ99BEACHYHv6XJ3w3AAAAACOGk2VZ"
        )
    #llm = init_chat_model(model=model, model_provider="openai")  # or "anthropic"
    tools, _ = get_research_tools(config)
    return {
        "messages": [
            await llm.bind_tools(tools).ainvoke(
                [{"role": "system", "content": RESEARCH_INSTRUCTIONS.format(section_description=state["section"])}] + state["messages"]
            )
        ]
    }
async def research_agent_tools(state: SectionState, config: dict):
    result = []
    completed = None
    _, tools = get_research_tools(config)

    for call in state["messages"][-1].tool_calls:
        tool = tools[call["name"]]
        obs = await tool.ainvoke(call["args"]) if hasattr(tool, "ainvoke") else tool.invoke(call["args"])
        result.append({"role": "tool", "content": str(obs), "name": call["name"], "tool_call_id": call["id"]})

        if call["name"] == "SectionTool":
            # Convert tool output to your data model
            completed = Section(
                name=obs.name,
                description=obs.description,
                content=obs.content
            )

    return {"messages": result, "completed_sections": [completed]} if completed else {"messages": result}

async def research_agent_should_continue(state: SectionState) :
    return "research_agent_tools" if state["messages"][-1].tool_calls else END

# --- Build Graphs ---

research_builder = StateGraph(SectionState, output=SectionOutputState, config_schema=Configuration)
research_builder.add_node("research_agent", research_agent)
research_builder.add_node("research_agent_tools", research_agent_tools)
research_builder.add_edge(START, "research_agent")
research_builder.add_conditional_edges("research_agent", research_agent_should_continue, {
    "research_agent_tools": "research_agent_tools",
    END: END
})
research_builder.add_edge("research_agent_tools", "research_agent")

supervisor_builder = StateGraph(ReportState, input=MessagesState, output=ReportStateOutput, config_schema=Configuration)
supervisor_builder.add_node("supervisor", supervisor)
supervisor_builder.add_node("supervisor_tools", supervisor_tools)
supervisor_builder.add_node("research_team", research_builder.compile())
supervisor_builder.add_edge(START, "supervisor")
supervisor_builder.add_conditional_edges("supervisor", supervisor_should_continue, {
    "supervisor_tools": "supervisor_tools",
    END: END
})
supervisor_builder.add_edge("research_team", "supervisor")

# ✅ COMPILE GRAPH
graph = supervisor_builder.compile()


from langgraph.checkpoint.memory import MemorySaver
import os



async def deepresearch(initial_msg,
                      AgenteReviewer=None
    ):
    # 1. Checkpointer
    checkpointer = MemorySaver()

    # 2. Compile the multi-agent graph
    graph = supervisor_builder.compile(checkpointer=checkpointer, debug=True)


    thread_config = {"configurable": config}

    initial_msg = {"role": "user", "content": initial_msg}

    # 4. Simulated user flow
    await graph.ainvoke({"messages": [initial_msg]}, config=thread_config)
    messages = graph.get_state(thread_config).values['messages']
    print("Messages exchanged during the research workflow:")
    print(messages[-1].content)
    print("\n---\n")


    if AgenteReviewer is not None:
        # 3. If a reviewer agent is provided, invoke it with the initial message
        review_msg = await AgenteReviewer.responder_pregunta(messages[-1].content)

        print("Reviewer's response to the initial message:")
        print(review_msg)
    followup_msg = {"role": "user", "content": review_msg}
    await graph.ainvoke({"messages": [followup_msg]}, config=thread_config)

    # 5. Get report
    final_state = graph.get_state(thread_config)

    # Get report from final_report field
    report = final_state.values.get("final_report", "No report generated.")
    if not report or report == "No report generated.":
        # Fallback: try last message
        last_message = final_state.values["messages"][-1]
        if hasattr(last_message, 'content') and last_message.content:
            report = last_message.content


    # Save final report
    with open('final_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)

    print("Multi-agent research workflow completed successfully!")
    print(f"Research sections completed: {len(final_state.values.get('completed_sections', []))}")
    print(f"Final report generated: {len(report)} characters")
    print("- SAVED: final_report.txt (complete research report)")
    return report
