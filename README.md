# AI Web Search Agent
LLMs are trained on historical data and the answers they provide are only based on the context up to a certain cut-off point in time. 

By building an AI agent with reasoning and acting capabilities ("ReAct Agent") in addition with a web search toolkit, the LLM can assess whether the question from the user would require searching from the internet, and incorporate the most updated information in its response.

The demonstration in this GitHub repository connects to the Amazon Nova Pro model via AWS Bedrock as the reasoning engine, with Tavily's web search tool bound to the model for it to be called when necessary.

![websearch_agent](https://github.com/tonytsoi/websearch_agent/blob/main/websearch_agent.jpg?raw=true)
