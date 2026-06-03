import autogen

config_list = [{"model": "gpt-4o", "api_key": "YOUR_API_KEY"}]
llm_config = {"config_list": config_list}

# ===== AGENT =====
assistant = autogen.AssistantAgent(
      name="AssistantAgent",
      llm_config=llm_config,
      system_message="You are a helpful AI assistant.",
)
coder = autogen.AssistantAgent(
      name="CoderAgent",
      llm_config=llm_config,
      system_message="You are an expert Python developer.",
)
critic = autogen.AssistantAgent(
      name="CriticAgent",
      llm_config=llm_config,
      system_message="You review solutions and provide constructive feedback.",
)
user_proxy = autogen.UserProxyAgent(
      name="UserProxy",
      human_input_mode="NEVER",
      max_consecutive_auto_reply=5,
)

# ===== TOOL =====
def web_search(query: str) -> str:
      """Tool: Search the web for information."""
      return f"Search results for: {query}"

def read_file(filepath: str) -> str:
      """Tool: Read content from a file."""
      return f"Contents of: {filepath}"

autogen.register_function(web_search, caller=assistant, executor=user_proxy, description="Search the web")
autogen.register_function(read_file, caller=coder, executor=user_proxy, description="Read a file")

# ===== SKILL =====
def coding_skill(task: str):
      """Skill: Multi-agent coding and review workflow."""
      groupchat = autogen.GroupChat(agents=[coder, critic, user_proxy], messages=[], max_round=6)
      manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
      user_proxy.initiate_chat(manager, message=task)

def research_skill(question: str):
      """Skill: Two-agent research and Q&A."""
      user_proxy.initiate_chat(assistant, message=question, max_turns=3)

# ===== MCP SERVER =====
MCP_SERVER_CONFIG = {
      "name": "AutoGen MCP Server",
      "transport": "stdio",
      "agents": ["AssistantAgent", "CoderAgent", "CriticAgent"],
      "tools": ["web_search", "read_file"],
}

# ===== AI MODEL =====
gpt4o_agent = autogen.AssistantAgent(name="GPT4oAgent", llm_config={"config_list": [{"model": "gpt-4o", "api_key": "YOUR_API_KEY"}]})
gpt4o_mini_agent = autogen.AssistantAgent(name="GPT4oMiniAgent", llm_config={"config_list": [{"model": "gpt-4o-mini", "api_key": "YOUR_API_KEY"}]})

# ===== OTHER =====
class ConversationLogger:
      """Utility for logging and exporting agent conversations."""
      def __init__(self):
                self.logs = []
            def log(self, agent: str, msg: str):
                      self.logs.append({"agent": agent, "message": msg})
                  def export(self) -> list:
                            return self.logs
                    
