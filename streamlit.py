import streamlit as st
from Backend.chat import Chat  # Assuming the Chat class is in a file named chat_backend.py

# Initialize the Chat class
chatbot = Chat()

# Streamlit app title
st.title("Incentive Buddy")

# Description for the app
st.write("""
I am here to answer all your incentive related queries!! Let's have a chat!
""")

# Input query from the user
user_query = st.text_input("Ask your question about the data:", placeholder="Ask your question")

# When the user clicks the "Get Response" button
if st.button("Get Response"):
    if user_query:
        try:
            # Call the backend to execute the query
            with st.spinner("Processing your query..."):
                result = chatbot.exe_query(user_query)
            
            # Display the result
            st.success("Rephrased Output:")
            st.write(result)
        
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query to get a response.")

