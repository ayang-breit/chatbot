from flask import Flask, request, jsonify
from langchain_anthropic import ChatAnthropic
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
import domain.dropbox.dropbox as dropbox
import core.config as config

app = Flask(__name__)

llm = ChatAnthropic(
    model="claude-opus-5-5",
    temperature=0,
    anthropic_api_key=config.read_encrypted_flag('claude_api_key')
)

dropbox_read_tool = Tool(
    name="DropboxFileReader",
    func=dropbox.read_dropbox_file,
    description="Useful for reading the contents of files stored in Dropbox. Input should be the file path."
)

dropbox_list_tool = Tool(
    name="DropboxFileList",
    func=dropbox.list_dropbox_directory,
    description="Useful for listing contents of folders stored in Dropbox. Input should be the file path."
)

tools = [dropbox_read_tool, dropbox_list_tool]

prompt = PromptTemplate.from_template(
    "You are a helpful assistant. Use the tools provided to answer the user's questions.\n"
    "Tools: {tools}\nTool Names: {tool_names}\n"
    "User: {input}\n"
    "{agent_scratchpad}"
)

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

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
    app.run(host='0.0.0.0', port=5000, debug=True)