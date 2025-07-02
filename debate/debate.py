import asyncio
from copy import deepcopy
from output_utils.logger import new_logger
from debate.round import FirstRound, SecondRoundWithResearch, ThirdRound, SecondRound, ProposalRound, VoteProposals, FinalProposalRound
from pydantic_utils.response_structures import ProposalsParagraph, VoteProposal
import json
import os

logger = new_logger("output_utils/debate_system.log")
#logger = new_logger("output_utils/debate_system_unbalanced.log")
#logger = new_logger("output_utils/debate_system_proposals.log")


class DebateThreeRoundsWithResearch:
    
    def __init__(self, agents, law, reviewer,ley_id, mock_research = False, use_research = True, debate_nro = 0):
        
        self.agents = agents
        self.law = law
        self.reviewer = reviewer 
        self.mock_research = mock_research 
        self.ley_id = ley_id
        self.use_research = use_research
        self.debate_nro = debate_nro
    async def run_debate(self, output_folder = "debates"):
        full_debate = {}
        if self.use_research:
            self.research, self.questions_and_answers = await self.reviewer.make_deep_research(ley=self.law, mock = self.mock_research, id = self.ley_id)
            self.rounds = [FirstRound(self.law), SecondRoundWithResearch(self.law, self.research), ThirdRound(self.law)]
            full_debate = {'preguntas y respuestas deep research': self.questions_and_answers,}

        else:
            self.rounds = [FirstRound(self.law), SecondRound(self.law), ThirdRound(self.law)]        

        
        #research = await self.reviewer.make_deep_research(self.law, mock = self.mock_research, id = id)
        #self.rounds[1] = SecondRoundWithResearch(self.law, research)

        context = [{"role":"user",
                    "content":  f"""Este es un debate simulado entre agentes políticos argentinos sobre la ley {self.law}.
                                    El debate constará de tres rondas:
                                    1. **Primera ronda**: Cada agente expresará su postura inicial, presentando argumentos a favor o en contra de la ley.
                                    2. **Segunda ronda**: Los agentes recibirán un informe con datos (provenientes de búsquedas en Google) y los argumentos expuestos por el resto de los agentes. Con esta información, podrán formular contraargumentos o reforzar su postura inicial.
                                    3. **Tercera ronda**: Los agentes recibirán tanto los argumentos iniciales como los contraargumentos de las rondas previas. En base a ello, deberán realizar una argumentación final y emitir una conclusión definitiva.
                                    En cada ronda, al finalizar su exposición, cada agente deberá explicitar su voto (a favor o en contra de la ley). El voto puede modificarse de ronda a ronda, pero el voto que determina la aprobación o rechazo de la ley será el emitido en la última ronda."""
                                    }]

        
        for round in self.rounds:
            logger.info(f"-----------------------------------Round {round.round_nr} -----------------------------------")
            result = await self.debate_round(context, round, full_debate)
            context+= result

        full_debate["Debate Completo"] = context
        logger.info("-------------------------------------------------")
        final_summary =  await self.reviewer.make_final_summary(full_debate)
        logger.info("---------------------- Final Summary------------------------")
        logger.info(final_summary)
        full_debate["Resumen final"] = final_summary
        
        logger.info("--- Full debate ---")
        logger.info(full_debate)
        research_folder= 'con_research' if self.use_research else 'sin_research'
        #os.makedirs(output_folder, exist_ok=True)
        path = os.path.join(output_folder,research_folder, f"ley_{self.ley_id}")
        os.makedirs(path, exist_ok=True)

        with open(os.path.join(path, f"debate_{self.debate_nro}.json"), "w", encoding ='utf8') as archivo:
            json.dump(full_debate, archivo, indent=4, ensure_ascii = False)
            
        return full_debate

    async def debate_round(self,prev_round_context, round, full_debate):
        
        prev_round_context.append({"role":"user",
            "content": f"Ahora arranca la ronda {round.round_nr}"})
        
        full_debate[f"Round {round.round_nr}"] = {}
        
        round_context = []
        prev_round_context.append({"role":"user", "content": round.prompt})

        for agent in self.agents:
            
            logger.info(f"Agente: {agent.agent_name}")
            dar_palabra = {"role":"user", "content": f"Tiene la palabra el {agent.agent_name}"} #este es el reviewer
            agent_context = deepcopy(prev_round_context)
            agent_context.append(dar_palabra)

            agent_response = await agent.speak(agent_context)
            full_debate[f"Round {round.round_nr}"][agent.agent_name] = {"argumentacion": agent_response["content"]["argumentacion"], "voto": agent_response["content"]["voto"]}
            
            agent_context = agent_response
            agent_context['content'] = agent_context['content']['argumentacion']
            
            logger.info(agent_response['content'])
            round_context.append(dar_palabra)

            round_context.append(agent_context)
            
        return round_context


    def conclusiones(self,full_debate):
        return self.reviewer.make_final_summary(full_debate)
    
class DebateNRounds:
    
    def __init__(self, n_rounds, agents, law, reviewer,ley_id, mock_research = False, use_research = True, debate_nro = 0):
        self.n_rounds = n_rounds
        self.agents = agents
        self.law = law
        self.reviewer = reviewer 
        self.mock_research = mock_research 
        self.ley_id = ley_id
        self.use_research = use_research
        self.debate_nro = debate_nro
    async def run_debate(self, output_folder = "debates_5_rondas"):
        full_debate = {}
        if self.use_research:
            self.research, self.questions_and_answers = await self.reviewer.make_deep_research(ley=self.law, mock = self.mock_research, id = self.ley_id)
            self.rounds = [FirstRound(self.law)] +[ SecondRoundWithResearch(self.law, self.research) for i in range(self.n_rounds -2)]+ [ThirdRound(self.law)]
            full_debate = {'preguntas y respuestas deep research': self.questions_and_answers,}

        else:
            self.rounds = [FirstRound(self.law)] +[ SecondRound(self.law, i+1) for i in range(self.n_rounds -2)]+ [ThirdRound(self.law, self.n_rounds-1)]

        context = [{"role":"user",
                    "content":  f"""Este es un debate simulado entre agentes políticos argentinos sobre la ley {self.law}.
                                    El debate constará de {self.n_rounds} rondas:
                                    1. **Primera ronda**: Cada agente expresará su postura inicial, presentando argumentos a favor o en contra de la ley.
                                    2-{self.n_rounds-1}. **Rondas 2 a {self.n_rounds-1}**: Los agentes recibirán un informe con datos (provenientes de búsquedas en Google) y los argumentos expuestos por el resto de los agentes. Con esta información, podrán formular contraargumentos o reforzar su postura inicial.
                                    {self.n_rounds}. **Última ronda**: Los agentes recibirán tanto los argumentos iniciales como los contraargumentos de las rondas previas. En base a ello, deberán realizar una argumentación final y emitir una conclusión definitiva.
                                    En cada ronda, al finalizar su exposición, cada agente deberá explicitar su voto (a favor o en contra de la ley). El voto puede modificarse de ronda a ronda, pero el voto que determina la aprobación o rechazo de la ley será el emitido en la última ronda."""
                                    }]

        
        for round in self.rounds:
            result = await self.debate_round(context, round, full_debate)
            context+= result

        full_debate["Debate Completo"] = context
        final_summary =  await self.reviewer.make_final_summary(full_debate)

        full_debate["Resumen final"] = final_summary

        research_folder= 'con_research' if self.use_research else 'sin_research'
        #os.makedirs(output_folder, exist_ok=True)
        path = os.path.join(output_folder,research_folder, f"ley_{self.ley_id}")
        os.makedirs(path, exist_ok=True)

        with open(os.path.join(path, f"debate_{self.debate_nro}.json"), "w", encoding ='utf8') as archivo:
            json.dump(full_debate, archivo, indent=4, ensure_ascii = False)
            
        return full_debate

    async def debate_round(self,prev_round_context, round, full_debate):
        
        prev_round_context.append({"role":"user",
            "content": f"Ahora arranca la ronda {round.round_nr}"})
        
        full_debate[f"Round {round.round_nr}"] = {}
        
        round_context = []
        prev_round_context.append({"role":"user", "content": round.prompt})

        for agent in self.agents:
            
            logger.info(f"Agente: {agent.agent_name}")
            dar_palabra = {"role":"user", "content": f"Tiene la palabra el {agent.agent_name}"} #este es el reviewer
            agent_context = deepcopy(prev_round_context)
            agent_context.append(dar_palabra)

            agent_response = await agent.speak(agent_context)
            full_debate[f"Round {round.round_nr}"][agent.agent_name] = {"argumentacion": agent_response["content"]["argumentacion"], "voto": agent_response["content"]["voto"]}
            
            agent_context = agent_response
            agent_context['content'] = agent_context['content']['argumentacion']
            
            logger.info(agent_response['content'])
            round_context.append(dar_palabra)

            round_context.append(agent_context)
            
        return round_context


    def conclusiones(self,full_debate):
        return self.reviewer.make_final_summary(full_debate)
    

    
class DebateWithProposals:
    
    def __init__(self, agents, law, reviewer,ley_id, mock_research = False, use_research = True):
        
        self.agents = agents
        self.law = law
        self.reviewer = reviewer 
        self.mock_research = mock_research 
        self.ley_id = ley_id
        self.use_research = use_research

    async def run_debate(self, output_folder = "evaluaciones_proposals"):
        if self.use_research:
            self.research, self.questions_and_answers = await self.reviewer.make_deep_research(self.law, mock = self.mock_research, id = self.ley_id)
            self.rounds = [FirstRound(self.law), SecondRoundWithResearch(self.law, self.research)]
        else:
            self.rounds = [FirstRound(self.law), SecondRound(self.law)]  

        full_debate = {'preguntas y respuestas deep research': self.questions_and_answers,}
        
        #research = await self.reviewer.make_deep_research(self.law, mock = self.mock_research, id = id)
        #self.rounds[1] = SecondRoundWithResearch(self.law, research)

        context = [{"role":"user",
                    "content":  f"""Este es un debate simulado entre agentes políticos argentinos sobre la ley {self.law}.
                                    El debate constará de tres rondas:
                                    1. **Primera ronda**: Cada agente expresará su postura inicial, presentando argumentos a favor o en contra de la ley.
                                    2. **Segunda ronda**: Los agentes recibirán un informe con datos (provenientes de búsquedas en Google) y los argumentos expuestos por el resto de los agentes. Con esta información, podrán formular contraargumentos o reforzar su postura inicial.
                                    3. **Tercera ronda**: Los agentes recibirán tanto los argumentos iniciales como los contraargumentos de las rondas previas. En base a ello, deberán realizar una argumentación final y emitir una conclusión definitiva.
                                    En cada ronda, al finalizar su exposición, cada agente deberá explicitar su voto (a favor o en contra de la ley). El voto puede modificarse de ronda a ronda, pero el voto que determina la aprobación o rechazo de la ley será el emitido en la última ronda."""
                                    }]

        
        for round in self.rounds:
            logger.info(f"-----------------------------------Round {round.round_nr} -----------------------------------")
            result = await self.debate_round(context, round, full_debate)
            context+= result
        
        round = ProposalRound(self.law)
        result, proposals = await self.get_proposals(context, round, full_debate)

        context += result

        logger.info(proposals)

        round = VoteProposals(self.law)
        result, voted_proposals = await self.vote_proposals(context, round, proposals, full_debate)

        context += result
        logger.info(voted_proposals)

        round  = FinalProposalRound(self.law, voted_proposals)
        logger.info(f"-----------------------------------Round {round.round_nr} -----------------------------------")
        result = await self.debate_round(context, round, full_debate)
        context+= result

        full_debate["Debate Completo"] = context
        logger.info("-------------------------------------------------")
        final_summary =  await self.reviewer.make_final_summary(full_debate)
        logger.info("---------------------- Final Summary------------------------")
        logger.info(final_summary)
        full_debate["Resumen final"] = final_summary
        
        logger.info("--- Full debate ---")
        logger.info(full_debate)
        os.makedirs(output_folder, exist_ok=True)

        with open(os.path.join(output_folder,f"debate_{self.ley_id}.json"), "w", encoding ='utf8') as archivo:
            json.dump(full_debate, archivo, indent=4, ensure_ascii = False)
            
        return full_debate

    async def debate_round(self,prev_round_context, round, full_debate):
        
        prev_round_context.append({"role":"user",
            "content": f"Ahora arranca la ronda {round.round_nr}"})
        
        full_debate[f"Round {round.round_nr}"] = {}
        
        round_context = []
        prev_round_context.append({"role":"user", "content": round.prompt})

        for agent in self.agents:
            
            logger.info(f"Agente: {agent.agent_name}")
            dar_palabra = {"role":"user", "content": f"Tiene la palabra el {agent.agent_name}"} #este es el reviewer
            agent_context = deepcopy(prev_round_context)
            agent_context.append(dar_palabra)

            agent_response = await agent.speak(agent_context)
            full_debate[f"Round {round.round_nr}"][agent.agent_name] = {"argumentacion": agent_response["content"]["argumentacion"], "voto": agent_response["content"]["voto"]}
            
            agent_context = agent_response
            agent_context['content'] = agent_context['content']['argumentacion']
            
            logger.info(agent_response['content'])
            round_context.append(dar_palabra)

            round_context.append(agent_context)
            
        return round_context

    async def get_proposals(self,prev_round_context,round, full_debate):
        
        prev_round_context.append({"role":"user",
            "content": f"Ahora arranca la ronda {round.round_nr}"})
        
        full_debate[f"Round {round.round_nr}"] = {}
        
        propuestas_paragraphs = ""
        prev_round_context.append({"role":"user", "content": round.prompt})

        context_round = []
        
        for agent in self.agents:
            logger.info(f"Agente: {agent.agent_name}")
            dar_palabra = {"role":"user", "content": f"Tiene la palabra el {agent.agent_name}"} #este es el reviewer
            agent_context = deepcopy(prev_round_context)
            agent_context.append(dar_palabra)

            agent_response = await agent.propose(agent_context, ProposalsParagraph)
            full_debate[f"Round {round.round_nr}"][agent.agent_name] = {"propuestas": agent_response.propuestas}

            context_round.append({
            "role": "assistant",
            "content": f"Propuestas: {agent_response.propuestas}",
        })
            
            propuestas_paragraphs += agent_response.propuestas + "\n"
            logger.info(agent_response.propuestas)
        
        propuestas_list = await self.reviewer.separar_propuestas(propuestas_paragraphs)
        
        return context_round, propuestas_list
    
    async def vote_proposals(self, prev_round_context, round, proposals, full_debate):
        prev_round_context.append({"role":"user",
            "content": f"Ahora arranca la ronda {round.round_nr}"})
        
        full_debate[f"Round {round.round_nr}"] = {}
        context_round = []
        prev_round_context.append({"role":"user", "content": round.prompt})
        approved_proposals = []

        for agent in self.agents:
            full_debate[f"Round {round.round_nr}"][agent.agent_name] = {}
        for proposal in proposals:
            logger.info(proposal)
            in_favour = 0
            for agent in self.agents:
                logger.info(f"Agente: {agent.agent_name}")
                dar_palabra = {"role":"user", "content": f"Tiene la palabra el {agent.agent_name}"} #este es el reviewer
                agent_context = deepcopy(prev_round_context)
                agent_context.append(dar_palabra)
                vote = await agent.vote_proposal(agent_context, VoteProposal, proposal)
                
                context_round.append({
                "role": "assistant",
                "content": f"[{agent.agent_name}] voto {vote.voto} para la propuesta {proposal} \n",
            })
                full_debate[f"Round {round.round_nr}"][agent.agent_name][proposal] = vote.voto

                if vote.voto == 1:
                    in_favour += 1
                logger.info(vote.razonamiento)
                logger.info(vote.voto)
            if in_favour >= len(self.agents) // 2 + 1:
                approved_proposals.append(proposal)
        
        return context_round, approved_proposals
            
    def conclusiones(self,full_debate):
        return self.reviewer.make_final_summary(full_debate)