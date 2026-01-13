from CookingAgent import build_agent
from langchain.messages import AIMessage, HumanMessage

agent = build_agent()

state = {
    "messages": [],
    "llm_calls": 0,
    "fridge_items": [],
    "spices": [],
    "equipment": [],
    "dietary_restrictions": [],
    "weather": None
}

while True:
    state = agent.invoke(state)
    # Break if agent is done
    if state["fridge_items"]:  # or some other end condition
        break

    # Check if last message is AI asking for input
    last_msg = state["messages"][-1] if state["messages"] else None
    if isinstance(last_msg, AIMessage):
        user_text = input(f"{last_msg.content}\n> ")
        state["messages"].append(HumanMessage(content=user_text))
    
   
    


for msg in state["messages"]:
    msg.pretty_print()

print("LLM calls:", state["llm_calls"])
print("Fridge items:", state["fridge_items"])
print("Spices:", state["spices"])
print("Equipment:", state["equipment"])
print("Dietary restrictions:", state["dietary_restrictions"])
