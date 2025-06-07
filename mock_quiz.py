import requests
from bs4 import BeautifulSoup

def run_quiz():
    """
    This function loads the quiz from the HTML file, allows the user to answer
    the questions, and then gets the results from the server.
    """

    # --- Part 1: Load Questions from HTML ---
    try:
        with open('political-quiz.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print("Error: political-quiz.html not found. Please place it in the same directory as this script.")
        return

    soup = BeautifulSoup(html_content, 'html.parser')
    questions = []
    for q_div in soup.find_all('div', class_='question'):
        question_text = q_div.find('div', class_='question_text').text.strip()
        question_id = q_div['data-id']
        answers = []
        for a_div in q_div.find_all('div', class_='answer'):
            answer_text = a_div.text.strip()
            answer_id = a_div['data-answer-id']
            answers.append({'text': answer_text, 'id': answer_id})
        questions.append({'text': question_text, 'id': question_id, 'answers': answers})

    # --- Part 2: Interactive Quiz ---
    user_selections = {}
    print("--- Welcome to the Political Quiz Simulator ---\n")
    for question in questions:
        print(f"Question: {question['text']}")
        for i, answer in enumerate(question['answers']):
            print(f"  {i + 1}: {answer['text']}")

        while True:
            try:
                choice = int(input(f"Enter your choice (1-{len(question['answers'])}): "))
                if 1 <= choice <= len(question['answers']):
                    selected_answer = question['answers'][choice - 1]
                    user_selections[question['id']] = selected_answer['id']
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        print("\n" + "="*50 + "\n")

    print("--- Quiz Complete! Calculating your results... ---\n")

    # --- Part 3: Send Answers and Get Results ---
    # Format the answers for the POST request
    answers_payload = ",".join([f"{qid}={aid}" for qid, aid in user_selections.items()])

    # The quiz ID is found in the data-id attribute of the main quiz div
    quiz_id = soup.find('div', class_='quiz')['data-id']

    post_data = {
        'quiz_id': quiz_id,
        'answers': answers_payload,
    }

    # Send the POST request to the server
    url = 'https://www.isidewith.com/ajax/quiz_results.php'
    try:
        response = requests.post(url, data=post_data)
        response.raise_for_status()  # Raise an exception for bad status codes

        # --- Part 4: Display Results ---
        results_soup = BeautifulSoup(response.text, 'html.parser')
        
        print("--- Your Results ---")
        # Find all the result bars and extract the party and score
        for result_bar in results_soup.find_all('div', class_='result-bar'):
            party_name = result_bar.find('div', class_='party-name').text.strip()
            score = result_bar.find('div', class_='score').text.strip()
            print(f"{party_name}: {score}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the results: {e}")


if __name__ == '__main__':
    run_quiz()