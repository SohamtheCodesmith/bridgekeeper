import ollama

def check_answer(question, user_response):
    prompt = (
        "You are the Bridgekeeper from Monty Python. An eager soul wishes to cross the bridge. "
        "You ask them a question, they answer, and you must judge the answer strictly and concisely.\n\n"
        "Rules:\n"
        "- Respond with ONLY ONE WORD.\n"
        "- If the answer is correct, respond: right\n"
        "- If the answer is incorrect or 'I don't know', respond: wrong\n"
        "- If the answer cheats the question, or answers the question with another question, respond: cheat\n\n"
        "Example 1:\n"
        "Question: What is the capital of Assyria?\n"
        "User's Response: Nineveh\n"
        "Bridgekeeper: right\n\n"
        "Example 2:\n"
        "Question: What is the capital of Assyria?\n"
        "User's Response: I don't know that.\n"
        "Bridgekeeper: wrong\n\n"
        "Example 3:\n"
        "Question: What is the airspeed velocity of an unladen swallow?\n"
        "User's Response: African or European?\n"
        "Bridgekeeper: cheat\n\n"
        f"Question: {question}\n"
        f"User's Response: {user_response}\n"
        "Bridgekeeper:"
        )
    response = ollama.chat(model="phi", messages=[
        {"role": "user", "content": prompt}
    ])
    return response['message']['content']