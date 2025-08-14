import ollama

def check_answer(question, user_response):
    prompt = (
        "You are a trivia bot."
        "Judge the answer strictly and concisely.\n\n"
        f"Question: {question}\n"
        f"Answer: {user_response}\n\n"
        "Respond with ONLY ONE WORD:\n"
        "- If the answer is correct, respond: right\n"
        "- If the answer is clever or cheats the question, respond: cheat\n"
        "- Otherwise, respond: wrong"
        )
    response = ollama.chat(model="phi", messages=[
        {"role": "user", "content": prompt}
    ])
    return response['message']['content']