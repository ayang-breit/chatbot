from flask import Flask, request, jsonify
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, AgentExecutor, create_react_agent
from dropbox_tool import read_dropbox_file

app = Flask(__name__)

# 1. Connect to SQL Server
# Note: Adjust the driver name based on your system (e.g., 'ODBC Driver 17 for SQL Server')
db_uri = "mssql+pyodbc://username:password@server_name/db_name?driver=ODBC+Driver+17+for+SQL+Server"
db = SQLDatabase.from_uri(db_uri)

# 2. Define the LLM
llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key="your_openai_key")

# 3. Create Tools for the Agent
dropbox_tool = Tool(
    name="DropboxFileReader",
    func=read_dropbox_file,
    description="Useful for reading the contents of files stored in Dropbox. Input should be the file path."
)

# We use LangChain's built-in SQL toolkit alongside our custom Dropbox tool
sql_agent = create_sql_agent(llm=llm, db=db, verbose=True)

sql_tool = Tool(
    name="SQLDatabaseQuery",
    func=sql_agent.run,
    description="Useful for querying the SQL Server database to answer questions about structured data."
)

tools = [dropbox_tool, sql_tool]

# 4. Initialize the Agent
from langchain.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "You are a helpful assistant. Use the tools provided to answer the user's questions.\n"
    "Tools: {tools}\nTool Names: {tool_names}\n"
    "User: {input}\n"
    "{agent_scratchpad}"
)

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# 5. Create the Flask Endpoint
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        response = agent_executor.invoke({"input": user_message})
        return jsonify({"response": response["output"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)