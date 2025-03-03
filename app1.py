import streamlit as st
import requests
import webbrowser

# API endpoint for random fun facts NEW UPDATE
API_URL = "https://uselessfacts.jsph.pl/random.json?language=en"

def fetch_fun_fact():
    """Fetch a random fun fact from the internet."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return data.get("text", "Couldn't fetch a fun fact. Try again!")
    except requests.exceptions.RequestException:
        return "Error fetching fun fact. Check your internet connection."

# Initialize session state
if "stage" not in st.session_state:
    st.session_state.stage = "start"
if "fact" not in st.session_state:
    st.session_state.fact = ""

# Start screen
if st.session_state.stage == "start":
    st.write("Click here when you are ready for your fun fact.")
    if st.button("Here"):
        st.session_state.fact = fetch_fun_fact()
        st.session_state.stage = "fact_shown"
        st.rerun()

# Show fact and ask if user wants to learn more
elif st.session_state.stage == "fact_shown":
    st.write(st.session_state.fact)
    st.write("Do you want to learn more?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Yes"):
            search_url = f"https://www.google.com/search?q={st.session_state.fact.replace(' ', '+')}"
            webbrowser.open(search_url)
    
    with col2:
        if st.button("No"):
            st.session_state.stage = "stay_ignorant"
            st.rerun()

# "Stay ignorant" screen, offers to go back or get a new fact
elif st.session_state.stage == "stay_ignorant":
    st.write("Ok, stay ignorant.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Here"):  # Get a new fun fact
            st.session_state.fact = fetch_fun_fact()
            st.session_state.stage = "fact_shown"
            st.rerun()

    with col2:
        if st.button("No, I don't want to be ignorant, take me back!"):  # Return to the last fact
            st.session_state.stage = "fact_shown"
            st.rerun()