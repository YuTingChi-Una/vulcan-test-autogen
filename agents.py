"""AutoGen agent, tool, skill, and MCP definitions."""
import autogen
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# ===== AI MODEL CONFIG =====
gpt4o_config = {"config_list": [{"model": "gpt-4o", "api_key": "YOUR_API_KEY"}]}
gpt4o_mini_config = {"config_list": [{"model": "gpt-4o-mini", "api_key": "YOUR_API_KEY"}]}

# ===== MCP SERVERS =====
MCP_SERVERS = {
      "knowledge_base": {"url": "http://localhost:8010/sse", "transport": "sse"},
      "filesystem": {"url": "http://localhost:8020/sse", "transport": "sse"},
}

# ===== TOOLS =====
def web_search(query: str) -> str:
      """Tool: Search the web for information on the given query."""
      return f"Search results for: {query}"

def read_file(filepath: str) -> str:
      """Tool: Read content from a local file."""
      return f"Contents of: {filepath}"

def execute_python(code: str) -> str:
      """Tool: Execute Python code and return the output."""
      return f"Output: {code[:100]}"

# ===== AGENTS =====
research_assistant = AssistantAgent(
      name="ResearchAssistant",
      system_message="You are a research assistant. Gather and analyze information thoroughly.",
      llm_config=gpt4o_config,
)

writer_assistant = AssistantAgent(
      name="WriterAssistant",
      system_message="You are a content writer. Produce clear, well-structured articles.",
      llm_config=gpt4o_config,
)

critic_assistant = AssistantAgent(
      name="CriticAssistant",
      system_message="You review content for quality, accuracy, and clarity.",
      llm_config=gpt4o_mini_config,
)

user_proxy = UserProxyAgent(
      name="UserProxy",
      human_input_mode="NEVER",
      max_consecutive_auto_reply=5,
      code_execution_config={"work_dir": "workspace", "use_docker": False},
)

autogen.register_function(web_search, caller=research_assistant, executor=user_proxy,
                              description="Search the web for information")
autogen.register_function(read_file, caller=research_assistant, executor=user_proxy,
                              description="Read content from a file")
autogen.register_function(execute_python, caller=writer_assistant, executor=user_proxy,
                              description="Execute Python code")

# ===== SKILLS (multi-agent workflows) =====
def research_and_write_skill(task: str) -> None:
      """Skill: Multi-agent research, writing, and review workflow."""
      groupchat = GroupChat(
          agents=[research_assistant, writer_assistant, critic_assistant, user_proxy],
          messages=[],
          max_round=8,
      )
      manager = GroupChatManager(groupchat=groupchat, llm_config=gpt4o_config)
    user_proxy.initiate_chat(manager, message=task)

def quick_research_skill(question: str) -> None:
      """Skill: Two-agent research and Q&A workflow."""
      user_proxy.initiate_chat(research_assistant, message=question, max_turns=4)
  
