from langchain.messages import AIMessage, HumanMessage
from typing_extensions import TypedDict, Annotated
import operator
from Tools.weather import get_weather
from CookingState import CookingState
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
import re
import json
from typing import List
from pydantic import BaseModel

# -----------------------------
# Define structured schema
# -----------------------------
class Recipe(BaseModel):
    title: str
    ingredients: List[str]
    spices_used: List[str]
    equipment_used: List[str]
    steps: List[str]
    notes: str

# -----------------------------
# Define Model and Agent
# -----------------------------
model = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google_genai",
    temperature=0
)

tools = [get_weather]

system_prompt = """
You are a helpful cooking assistant and recipe generator. 
You can call get_weather(city) to check the weather.
Generate a recipe based on fridge_items, spices, equipment, dietary restrictions, and optionally the weather. 

Rules:
- ingredients must come ONLY from fridge_items
- spices_used must come ONLY from spices
- equipment_used must come ONLY from equipment
- Do NOT invent ingredients
- If a recipe is impossible, return an empty ingredients list
"""

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt,
    response_format=Recipe )


# -----------------------------
# Input State and Invocation
# -----------------------------
state: CookingState = {
    "messages": [],
    "city": "taipei",
    "dietary_restrictions": [],
    "fridge_items": ["apple", "flour", "butter"],
    "spices": ["salt", "pepper", "cinnamon", "sugar"],
    "equipment": ["pan", "spatula"],
    "llm_calls": 0
}

user_input = f"""
I'm living in {state['city'] or 'unknown'}.
I have the following fridge items: {', '.join(state['fridge_items'])}.
I have the following spices: {', '.join(state['spices'])}.
I have the following equipment: {', '.join(state['equipment'])}.
Dietary restrictions: {', '.join(state['dietary_restrictions']) if state['dietary_restrictions'] else 'None'}.

Please recommend a recipe I can make with these ingredients.
"""

result = agent.invoke(
    {"messages": [{"role": "user", "content": user_input}]}
)
recipe: Recipe = result["structured_response"] 
print("Structured Recipe JSON:")
print(recipe.model_dump_json(indent=2))