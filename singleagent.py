from agents.news_agent.agent import NewsAgentBuilder

news_agent = NewsAgentBuilder().build();

config = {"configurable": {"thread_id": "user_session_123"}}

input_message = {
    "role": "user",
    "content": "Give me the most important financial news in Argentina",
}

for step in news_agent.stream(
    {"messages": [input_message]}, config, stream_mode="values"
):
    step["messages"][-1].pretty_print()