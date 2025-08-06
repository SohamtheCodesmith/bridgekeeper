# 🧙 Bridgekeeper

**Stop! Who would cross the Bridge of Death must answer me these questions three, ere the other side he sees.**

A Monty Python-inspired AI-powered trivia game built with Streamlit.

## 🎮 Features

- AI-generated absurd questions
- Randomised outcomes based on answers
- Animated GIFs for user and Bridgekeeper deaths
- Persistent session history of who survived and who perished
- Hidden cheat codes 👀

## ⚙️ How to Run

Install dependencies:

```bash
pip install -r requirements.txt
````

Make sure [Ollama](https://ollama.com) is installed and running:

```bash
ollama run phi
```

Run the app:

```bash
streamlit run app.py
```

## 🚧 Roadmap

* Better question generation
* AI-based explanation of failures
* Multiplayer support
* Flask+JS port