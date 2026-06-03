---
name: multi-agent-workflow
license: MIT
description: >
  AutoGen skill for multi-agent research, writing, and review workflow.
    Orchestrates ResearchAssistant, WriterAssistant, and CriticAssistant
      via GroupChat with a UserProxy executor.
      tools:
        - name: web_search
            description: Search the web for information
              - name: read_file
                  description: Read content from a local file
                    - name: execute_python
                        description: Execute Python code and return output
                        ---

                        # Multi-Agent Workflow Skill

                        Autogen GroupChat workflow for research, writing, and content review.

                        ## Agents
                        - **ResearchAssistant**: Gathers information using web search and file tools.
                        - **WriterAssistant**: Produces structured content from research.
                        - **CriticAssistant**: Reviews and validates content quality.
                        - **UserProxy**: Executes tool calls on behalf of other agents.

                        ## MCP Servers
                        - **Knowledge Base**: SSE MCP for domain knowledge (port 8010).
                        - **Filesystem**: SSE MCP for file access (port 8020).
                        
