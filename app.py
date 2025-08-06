import streamlit as st
import time
import ollama
import random

# Ponder the AI

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



# APP INTERFACE BEGINS HERE

st.set_page_config(page_title="Bridgekeeper", page_icon="🧙")
st.image("assets/stop.jpg", use_container_width=True)
st.title("The Bridge of Death")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.name = ""
    st.session_state.quest = ""
    st.session_state.colour = ""
    st.session_state.hard_q = None
    st.session_state.hard_a = None
    st.session_state.result = ""
    st.session_state.chatlog = [
        ("Bridgekeeper", "Stop! Who would cross the Bridge of Death must answer me these questions three, ere the other side he sees."),
        ("You", "Ask me the questions, Bridgekeeper. I'm not afraid."),
    ]
    st.session_state.waiting_for_question = False

for key in ["user_failed", "bridgekeeper_failed", "ask_colour", "total_survived", "total_fallen", "history"]:
    if key not in st.session_state:
        st.session_state[key] = False if "failed" in key else 0 if "total" in key else None if "ask" in key else []

if "history" not in st.session_state:
    st.session_state.history = []

def add_to_chat(speaker, message):
    st.session_state.chatlog.append((speaker, message))

def reset():
    if st.session_state.step >= 3:
        st.session_state.history.append({
            "chatlog": st.session_state.chatlog.copy(),
            "result": st.session_state.result,
            "user_failed": st.session_state.get("user_failed", False),
            "bridgekeeper_failed": st.session_state.get("bridgekeeper_failed", False),
        })
    st.session_state.step = 0
    st.session_state.name = ""
    st.session_state.quest = ""
    st.session_state.colour = ""
    st.session_state.hard_q = None
    st.session_state.hard_a = None
    st.session_state.result = ""
    st.session_state.chatlog = [
        ("Bridgekeeper", "Stop!"),
    ]
    st.session_state.waiting_for_question = False
    st.session_state.ask_colour = False
    st.session_state.user_failed = False
    st.session_state.bridgekeeper_failed = False

def restart_bridgekeeper():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Display chatlog
for speaker, message in st.session_state.chatlog:
    st.markdown(f"**{speaker}:** {message}")

# Step 1: What is your name?
if st.session_state.step == 0:
    if not st.session_state.waiting_for_question:
        add_to_chat("Bridgekeeper", "What is your name?")
        st.session_state.waiting_for_question = True
        st.rerun()

    name = st.text_input("", key="input_name")
    if name:
        st.session_state.name = name
        add_to_chat("You", name)
        time.sleep(1)
        st.session_state.step += 1
        st.session_state.waiting_for_question = False
        st.rerun()

# Step 2: What is your quest?
elif st.session_state.step == 1:
    if not st.session_state.waiting_for_question:
        add_to_chat("Bridgekeeper", "What is your quest?")
        st.session_state.waiting_for_question = True
        st.rerun()

    quest = st.text_input("", key="input_quest")
    if quest:
        st.session_state.quest = quest
        add_to_chat("You", quest)
        time.sleep(1)
        st.session_state.step += 1
        st.session_state.waiting_for_question = False
        st.rerun()

# Step 3: Final question
elif st.session_state.step == 2:
    
    st.session_state.ask_colour = random.choice([True, False])
    
    if st.session_state.ask_colour:
        # Easy
        if not st.session_state.waiting_for_question:
            add_to_chat("Bridgekeeper", "What is your favourite colour?")
            st.session_state.waiting_for_question = True
            st.rerun()

        colour = st.text_input("", key="input_colour")
        if colour:
            st.session_state.colour = colour
            add_to_chat("You", colour)
            time.sleep(1)
            st.session_state.result = "Right! Off you go."
            add_to_chat("Bridgekeeper", st.session_state.result)
            st.session_state.step += 1
            st.session_state.waiting_for_question = False
            st.rerun()
    else:
        # Hard
        if not st.session_state.hard_q:
            q = generate_hard_question()
            st.session_state.hard_q = q
            st.rerun()
        elif not st.session_state.waiting_for_question:
            add_to_chat("Bridgekeeper", st.session_state.hard_q)
            st.session_state.waiting_for_question = True
            st.rerun()
        else:
            answer = st.text_input("", key="input_hard")
            if answer:
                add_to_chat("You", answer)
                a = check_answer(st.session_state.hard_q, answer.strip().lower())
                if 'right' in a.lower():
                    st.session_state.result = "Right! Off you go."
                elif 'wrong' in a.lower():
                    st.session_state.result = "WRONG!"
                    st.session_state.user_failed = True
                elif 'cheat' in a.lower():
                    st.session_state.result = "Uh- I don't know that- AAAAAAAH!"
                    st.session_state.bridgekeeper_failed = True
                else:
                    st.session_state.result = a
                add_to_chat("Bridgekeeper", st.session_state.result)
                st.session_state.step += 1
                st.session_state.waiting_for_question = False
                st.rerun()

# Step 4: Show result
elif st.session_state.step == 3:
    if st.session_state.get("user_failed"):
        st.image("assets/userFail.gif", use_container_width=True)
    elif st.session_state.get("bridgekeeper_failed"):
        st.image("assets/bridgekeeperFail.gif", use_container_width=True)
    if not st.session_state.bridgekeeper_failed:
        st.button("Go Again", on_click=reset)
    
    if st.session_state.bridgekeeper_failed:
        st.markdown("---")
        add_to_chat("Narrator", "The Bridgekeeper has fallen. None shall pass.")
        st.image("assets/noneShallPass.jpg", use_container_width=True)
        st.markdown("## The Bridgekeeper is gone. Click below to start a new game.")
        if st.button("Restart Game"):
            restart_bridgekeeper()
        st.stop()


if st.session_state.history:
    st.markdown("---")
    st.subheader("Past Attempts")

    for i, entry in enumerate(st.session_state.history[::-1], 1):
        st.markdown(f"### Attempt #{len(st.session_state.history) - i + 1}")
        for role, msg in entry["chatlog"]:
            st.markdown(f"**{role}:** {msg}")
        if entry["user_failed"]:
            st.image("assets/userFail.gif", use_container_width=True)
        elif entry["bridgekeeper_failed"]:
            st.image("assets/bridgekeeperFail.gif", use_container_width=True)
        st.markdown("---")