import ollama

def generate_hard_question():
    prompt = (
        "You are a trivia bot."
        "Ask a short and difficult trivia question."
        "DO NOT provide the answer. Keep the question under 10 words."
        "ONLY output the question text itself. No extra formatting."
        )
    response = ollama.chat(model="phi", messages=[
        {"role": "user", "content": prompt}
    ])
    return response['message']['content']