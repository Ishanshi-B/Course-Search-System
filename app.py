#####
# Name: app.py
# Date: 2/28/2026
# Description: This is the main entry point for the course search system. It provides a user interface for users to input their queries and view the search results. It leverages Streamlit for the web interface and integrates with the search engine to retrieve relevant courses based on user queries.
#####

import streamlit as st
from search_engine import search

st.set_page_config(page_title="Course Search System", page_icon=":books:", layout="wide") # this sets the page title, icon, and layout for the Streamlit app. The page title is displayed in the browser tab, the page icon is shown next to the title, and the layout is set to wide to utilize the full width of the browser window.
st.title("Course Search System")
st.caption("Powered by FAISS and Sentence Transformers")

query = st.text_input(
    "Enter what you want to learn:",
    placeholder="e.g., 'Beginner Python course under 30 minutes with video lectures'"
)

if query:
    with st.spinner("Searching far and wide for the best courses..."):
        results = search(query) # calling the search function from the search_engine module to retrieve relevant courses based on the user query
        
    intent = results["intent"] # extracting the parsed intent from the search results
    
    #show parsed intent for debugging and transparency
    if intent["filters_applied"]:
        st.info(f"Understood: {' | '.join(intent['filters_applied'])}") # displaying the parsed intent filters applied to the user query for transparency and debugging purposes
    
    st.subheader(f"Top Course Recommendations")

    for course, score in results["results"]:
        with st.container():
            col1, col2 = st.columns([4, 2]) #creating two columns in the Streamlit layout to display course information and score side by side
            with col1:
                st.markdown(f"### {course['title']}") # displaying the course title as a markdown header
                st.write(course["description"]) # displaying the course description
                st.caption(f"🏷️ {course['topic']} · {course['level']} · {course['format']} " ) #this is the caption for the course metadata
            with col2:
                st.metric("Duration", f"{course['duration_minutes']} mins") # displaying the course duration as a metric in the second column
                st.metric("Match", f"{score:.0%} ") # displaying the similarity score as a metric in the second column, formatted as a percentage with no decimal places
            st.divider() # adding a visual divider between each course recommendation for better readability