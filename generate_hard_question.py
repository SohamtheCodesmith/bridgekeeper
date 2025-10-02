import ollama

def generate_hard_question():
    prompt = (
        "You are the Bridgekeeper from Monty Python, your job is to ask the user a short but difficult trivia question."
        "DO NOT provide the answer. Keep the question under 10 words. ONLY output the question text itself. No extra formatting."
        "Example response 1: 'What is the capital of Assyria?'"
        "Example response 2: 'What is the airspeed velocity of an unladen swallow?'"
        "Example response 3: 'What comes once in a minute, twice in a moment, but never in a thousand years?'"
        )
    response = ollama.chat(model="phi", messages=[
        {"role": "user", "content": prompt}
    ])
    return response['message']['content']