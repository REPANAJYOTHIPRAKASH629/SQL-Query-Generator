import streamlit as st
import requests

# Hugging Face API Key (make sure it has inference access)
HUGGINGFACE_API_KEY = "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"

# API endpoint and headers
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# Function to send prompts to Hugging Face model
def ask_huggingface(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()

    if isinstance(result, list):
        return result[0]['generated_text'].strip()
    else:
        return result.get("error", "❌ Error: Could not get a valid response from the model.")

# Main app
def main():
    st.set_page_config(page_title="SQL Query Generator", page_icon=":robot_face:")
    st.markdown(
        """
        <div style="text-align: center;">
            <h1 style="color:#4CAF50;">SQL Query Generator</h1>
            <h3>Generate SQL Queries for you</h3>
            <h4>With explanation as well!!!</h4>
            <p>This is a simple SQL query generator that helps you create SQL queries based on your input.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    text_input = st.text_area(
        "Enter your SQL query here in English 👇", height=150,
        placeholder="e.g. Show all customers who ordered more than 5 items in March"
    )

    submit_button = st.button("🚀 Generate SQL Query")

    if submit_button and text_input.strip():
        with st.spinner("Generating SQL query..."):

            # Prompt to generate SQL
            prompt_sql = f"""
            #Create a SQL query snippet using the below text:
            ```
            {text_input}
            ```
            #I just want a SQL query. No explanation.
            """
            sql_query = ask_huggingface(prompt_sql)
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

            # Prompt to generate expected output
            prompt_output = f"""
            What would be the expected response of this SQL Query snippet?
            ```
            {sql_query}
            ```
            Provide a sample tabular output in markdown format, no explanation.
            """
            eoutput = ask_huggingface(prompt_output)

            # Prompt to generate explanation
            prompt_explain = f"""
            Explain this SQL Query:
            ```
            {sql_query}
            ```
            Please provide the simplest explanation possible.
            """
            explanation_response = ask_huggingface(prompt_explain)

            # Output to UI
            with st.container():
                st.success("✅ SQL Query Generated Successfully!")
                st.code(sql_query, language="sql")

                st.success("📊 Expected Output of This SQL Query:")
                st.markdown(eoutput)

                st.success("🧠 Explanation of This SQL Query:")
                st.markdown(explanation_response)

    elif submit_button:
        st.warning("⚠️ Please enter a valid input.")

# Run the app
if __name__ == "__main__":
    main()
