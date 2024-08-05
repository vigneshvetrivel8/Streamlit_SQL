import streamlit as st
import os
import psycopg2
from langchain_google_genai import GoogleGenerativeAI
import re
from dotenv import load_dotenv

load_dotenv()  # Load all the environment variables

# Initialize the Google Generative AI model
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))

# Function To Load Google Gemini Model and provide queries as response
def get_gemini_response(user_query):
    prompt = (
        """
        You are an expert in converting English questions to SQL query!
        The SQL database has the name STUDENT and has the following columns - ID, NAME, SUBJECT, 
        SCORE.

        For example,

        Example 1
        Question:How many entries of records are present?
        Command:SELECT COUNT(*) FROM STUDENT;

        Example 2:
        Question:Add a new student named ABCD with Subject Physics.
        Command:INSERT INTO STUDENT (ID, NAME, SUBJECT, SCORE) VALUES (NULL, 'ABCD', 'Physics, NULL);

        So what is the Command for the following question.
        Question: {question}
        """
    ).format(question=user_query)
    response = llm.invoke(prompt)
    return response

# Basic SQL Commands
basic_sql_commands = [
    "SELECT",      # Retrieves data from one or more tables
    "INSERT",      # Adds new rows of data into a table
    "UPDATE",      # Modifies existing rows in a table
    "DELETE",      # Removes rows from a table
    "TRUNCATE TABLE", # Deletes all rows from a table but keeps the table structure
    "CREATE INDEX", # Creates an index on a table to improve query performance
    "DROP INDEX",   # Removes an index from a table
    "JOIN",         # Combines rows from two or more tables based on a related column
    "GROUP BY",     # Groups rows with the same values into summary rows
    "ORDER BY",     # Sorts the result set of a query
    "HAVING",       # Filters groups of rows after aggregation
    "DISTINCT"      # Selects unique values
]

# SQL Commands with Significant Consequences
consequential_sql_commands = [
    "ALTER TABLE", # Modifies the structure of an existing table
    "DROP TABLE",  # Deletes a table and its data
    "CREATE TABLE",# Creates a new table
    "DROP DATABASE",    # Deletes an entire database and all of its tables
    "RENAME TABLE",     # Changes the name of an existing table
    "ALTER TABLE ... DROP COLUMN", # Removes a column from a table
    "ALTER TABLE ... MODIFY COLUMN", # Changes the data type or properties of an existing column
    "ALTER TABLE ... RENAME COLUMN", # Changes the name of a column in a table
    "CREATE VIEW",      # Creates a virtual table based on a SELECT query
    "DROP VIEW",        # Deletes a view from the database
    "CREATE PROCEDURE", # Defines a stored procedure that can be executed later
    "DROP PROCEDURE",   # Deletes a stored procedure
    "CREATE TRIGGER",   # Sets up a trigger to automatically perform actions in response to certain events
    "DROP TRIGGER",     # Removes a trigger
    "CREATE FUNCTION",  # Defines a user-defined function that can be used in SQL queries
    "DROP FUNCTION"     # Deletes a user-defined function
]

def extract_command_from_response(response):
    # Combine the command lists for searching
    all_commands = basic_sql_commands + consequential_sql_commands

    # Create a regex pattern to search for SQL commands
    pattern = r'\b(' + '|'.join(re.escape(cmd) for cmd in all_commands) + r')\b'

    # Find all matches in the response
    matches = re.findall(pattern, response, re.IGNORECASE)

    if matches:
        # Extract the first command found
        command = matches[0]

        # Find the position of the command and the end of the command
        start_index = response.upper().find(command)
        end_index = response.find(';', start_index) + 1

        # Extract the command from the response
        extracted_command = response[start_index:end_index].strip()
        return extracted_command
    else:
        return None

## Function To execute SQL query from PostgreSQL database
def execute_sql_query(sql, db_params):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute(sql)
    try:
        rows = cur.fetchall()
    except psycopg2.ProgrammingError:
        rows = []
    conn.commit()
    conn.close()
    return rows

## Streamlit App
st.set_page_config(page_title="Retrieve SQL query")
st.header("App to perform SQL actions")

question = st.text_input("Input: ", key="input")

submit = st.button("Submit")

# Database connection parameters
db_params = {
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT")
}

# if submit is clicked
if submit:
    response = get_gemini_response(question)
    extracted_command = extract_command_from_response(response)
    print("extracted_command:", extracted_command)

    if extracted_command:
        # Check if the command starts with any of the words in basic_sql_commands
        command_type = extracted_command.split()[0].upper()
        st.subheader("Command used:")
        st.write(extracted_command)
        if command_type in [cmd.upper() for cmd in basic_sql_commands]:
            try:
                result = execute_sql_query(extracted_command, db_params)
                st.subheader("Response:")
                for row in result:
                    st.write(row)
                st.subheader("Command executed successfully.")
            except Exception as e:
                st.subheader("Response:")
                st.error(f"Error executing SQL query: {e}")
        else:
            st.write("This query can't be executed. Commands allowed are:", basic_sql_commands)
            st.error("Operation failed")
    else:
        st.subheader("Response:")
        st.error("Failed to extract a valid SQL command for the input")
