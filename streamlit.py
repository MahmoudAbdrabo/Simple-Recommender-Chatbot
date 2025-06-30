import streamlit as st
from recommended1 import BookRecommender
from chat import IntentClassifier

# titel pag
st.set_page_config(page_title="📚 Book Chatbot", layout="centered")
st.title("🤖 Simple book recommendation chatbot")

# lode model
import_features = ['title', 'authors', 'categories', 'description', 'published_year', 'average_rating']
recommender = BookRecommender("data.csv", import_features)
classifier = IntentClassifier("intents1.json")

# history
if "history" not in st.session_state:
    st.session_state.history = []

for key in ["awaiting_book_for_recommend", "awaiting_book_for_author", "awaiting_book_for_year"]:
    if key not in st.session_state:
        st.session_state[key] = False

# user input
user_input = st.text_input("🗨️Enter your message:")

if user_input:
    st.session_state.history.append(("🧑", user_input))

    # wating 
    if st.session_state.awaiting_book_for_recommend:
        results = recommender.recommend(user_input)
        if "❌" in results[0]:
            st.session_state.history.append(("🤖", results[0]))
        else:
            st.session_state.history.append(("🤖", "📚 Suggested books:"))
            for title in results:
                st.session_state.history.append(("📘", title))
        st.session_state.awaiting_book_for_recommend = False

    elif st.session_state.awaiting_book_for_author:
        author = recommender.get_author(user_input)
        st.session_state.history.append(("🤖", author))
        st.session_state.awaiting_book_for_author = False

    elif st.session_state.awaiting_book_for_year:
        year = recommender.get_publish_year(user_input)
        st.session_state.history.append(("🤖", year))
        st.session_state.awaiting_book_for_year = False

    else:
        intent = classifier.classify(user_input)
        response = classifier.get_response(intent)
        st.session_state.history.append(("🤖", response))

        if intent == "book_recommendation":
            st.session_state.awaiting_book_for_recommend = True
        elif intent == "ask_author":
            st.session_state.awaiting_book_for_author = True
        elif intent == "ask_publish_year":
            st.session_state.awaiting_book_for_year = True
        elif intent == "bestsellers":
            bestsellers = recommender.get_bestsellers()
            st.session_state.history.append(("🤖", "📈 The most popular books according to readers' ratings:"))
            for title in bestsellers:
                st.session_state.history.append(("📘", title))

# show chat 
for speaker, message in st.session_state.history:
    if speaker == "📘":
        st.markdown(f"- {message}")
    else:
        st.markdown(f"**{speaker}:** {message}")
