import re
import json
from CookingState import CookingState
from langgraph.graph import StateGraph, START, END
from langchain.messages import AIMessage, HumanMessage
from langchain.chat_models import init_chat_model
# -------- Nodes --------

def detect_first_time(state: CookingState):
    return {} 

def setup_router(state: CookingState):
    if state["fridge_items"]:
        return "done"           
    if has_user_replied(state):
        return "parse"    
    return "ask"             

def has_user_replied(state: CookingState) -> bool:
    if not state["messages"]:
        return False
    return isinstance(state["messages"][-1], HumanMessage)


def setup_node(state: CookingState):
    return {
            "messages": [
                AIMessage(
                    content=(
                        "I need your setup first.\n"
                        "What food is in your fridge?\n"
                        "What spices do you have?\n"
                        "What equipment do you have?\n"
                        "Any dietary restrictions?"
                    )
                )
            ]
    }

def parse_node(state: CookingState): 
    text = state["messages"][-1].content 
    # Later: call LLM to extract structured data 
    # For now, fake it: 
    return { 
        "fridge_items": ["chicken", "eggs"], 
        "spices": ["salt", "pepper"], 
        "equipment": ["pan"], 
        "dietary_restrictions": [] }

# from dotenv import load_dotenv
# from langchain.chat_models import init_chat_model
# load_dotenv()
# model = init_chat_model(
#     model="gemini-2.5-flash",
#     model_provider="google_genai",
#     temperature=0
# )
# def parse_setup(state: CookingState):
#     user_text = state["messages"][-1].content

#     prompt = [
#         {"role": "system", "content": (
#             "Extract cooking setup from user input. "
#             "Return JSON with keys: fridge_items, spices, equipment, dietary_restrictions."
#         )},
#         {"role": "user", "content": user_text}
#     ]

#     response = model.invoke(prompt)
#     print("LLM response:", response.content)
#     clean_text = re.sub(r"```json|```", "", response.content).strip()

#     match = re.search(r"\{.*\}", clean_text, re.DOTALL)
#     if match:
#         clean_text = match.group(0)
#     try:
#         data = json.loads(clean_text)
#     except Exception:
#         data = {
#             "fridge_items": [],
#             "spices": [],
#             "equipment": [],
#             "dietary_restrictions": []
#         }
#     return data

# -------- Graph --------
def build_agent():
    builder = StateGraph(CookingState)
    builder.add_node("router", setup_router)
    builder.add_node("first", detect_first_time)
    builder.add_node("setup", setup_node)
    builder.add_node("parse", parse_node)
    builder.add_edge(START, "first")
    builder.add_conditional_edges(
        "first",
        setup_router,  # re-use same router
        {
            "ask": "setup",     # loop until human reply
            "parse": "parse",   # after reply, parse and continue
            "done": END
        }
    )
    

    return builder.compile()