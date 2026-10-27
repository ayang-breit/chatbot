import domain.dropbox.dropbox as dropbox
import core.config as config
from flask import Flask, request, jsonify, render_template, render_template_string
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import Tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
import datetime
import json

app = Flask(__name__)

llm = ChatAnthropic(
    model="claude-opus-5-5",
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

memory = MemorySaver()
agent_executor = create_agent(llm, tools, checkpointer=memory)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")
    session_id = data.get("session_id")

    if not user_message or not session_id:
        return jsonify({"error": "Message and session_id are required"}), 400

    try:
        config = {"configurable": {"thread_id": session_id}}

        messages_payload = []
        if not memory.get(config):
            messages_payload.append(
                ("system", "You are a helpful assistant. Use the tools provided to answer the user's questions.")
            )

        messages_payload.append(("user", user_message))

        response = agent_executor.invoke(
            {"messages": messages_payload},
            config=config
        )

        raw_content = response["messages"][-1].content
        if isinstance(raw_content, list):
            final_answer = "".join([
                block.get("text", "")
                for block in raw_content
                if isinstance(block, dict) and block.get("type") == "text"
            ])
        else:
            final_answer = str(raw_content)

        return jsonify({"response": final_answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)