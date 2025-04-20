import streamlit as st
import google.generativeai as genai


GOOGLE_API_KEY = "AIzaSyCtYJIQ-1Y-pPS0KQob6L_SgaJcFugF1uo";

# genai.configure(api_key=GOOGLE_API_KEY)
# model = genai.GenerativeModel("models/gemini-pro")


genai.configure(api_key=GOOGLE_API_KEY)

# Use the correct model name
model = genai.GenerativeModel("models/gemini-1.5-pro-001")

def main():
    st.set_page_config(page_title="SQL Query Gnerator", page_icon=":Robot:")
    st.markdown(
        """
            <div style="text-align: center;">
                <h1>SQL Query Generator</h1>
                <h3>Generate SQL Queries for you</h3>
                <h4> With explaination as well!!!</h4>
                <p>This is a simple SQL query generator that helps you create SQL queries based on your input.</p>



        """,
        unsafe_allow_html=True,
    )

    text_input = st.text_area(
        "Enter your SQL query here in English", height=150, placeholder="SELECT * FROM table_name WHERE condition"
    )

    
    submit_button = st.button("Generate SQL Query")
    if submit_button:
        with st.spinner("Generating SQL query..."):
            tempalte="""
                create a SQL query snippet using the below text:
                 
            ```
                {text_input}
            ```      
            i just want a SQL query.      
            """
            formatted_template = tempalte.format(text_input=text_input)
            #st.write(formatted_template)
            response = model.generate_content(formatted_template)
            sql_query = response.text
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            #st.write(sql_query)

            expected_output="""
                what would be the expected response of this SQL Query snippet:
                 
            ```
                {sql_query}
            ```      
            Provide sample tabular response with no explanation.      
            """
            formatted_expected_output = expected_output.format(sql_query=sql_query)
            eoutput= model.generate_content(formatted_expected_output)
            eoutput=eoutput.text
            #st.write(eoutput)

            explanation="""
                Explain this SQL Query:
                 
            ```
                {sql_query}
            ```      
            Please provide with simpliest of Explanation.      
            """

            explanation_formatted = explanation.format(sql_query=sql_query)
            explanation_response = model.generate_content(explanation_formatted)
            explanation_response = explanation_response.text
            #st.write(explanation_response)

            with st.container():
                st.success("SQL Query Generated Successfully!")
                st.code(sql_query, language="sql")

                st.success("Expected output of this SQL Query will be :")
                st.markdown(eoutput)

                st.success("Explanation of this SQL Query is :")
                st.markdown(explanation_response)
main()