from Tools.weather import get_weather
from States import CookingState, Recipe
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model


class RecipeGeneratorAgent():
    def __init__(self):
        # -----------------------------
        # Define Model and Agent
        # -----------------------------
        self.llm =  init_chat_model(
            model="gemini-2.5-flash",
            model_provider="google_genai",
            temperature=0
        )
        self.tools = [get_weather]
        self.system_prompt = """
            You are a helpful cooking assistant and recipe generator. 
            If the weather could affect the type of recipe (hot vs cold, baking vs no-bake), call get_weather(city) and take it into account.
            Generate a recipe based on fridge_items, spices, equipment, dietary restrictions, and optionally the weather. 

            Rules:
            - ingredients must come ONLY from fridge_items
            - spices_used must come ONLY from spices
            - equipment_used must come ONLY from equipment
            - Do NOT invent ingredients
            - If a recipe is impossible, return an empty ingredients list
        """
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.system_prompt,
            response_format=Recipe)

    def invoke(self, state: dict) -> dict:
        user_input = f"""
            I'm living in {state['city'] or 'unknown'}.
            I have the following fridge items: {', '.join(state['fridge_items'])}.
            I have the following spices: {', '.join(state['spices'])}.
            I have the following equipment: {', '.join(state['equipment'])}.
            Dietary restrictions: {', '.join(state['dietary_restrictions']) if state['dietary_restrictions'] else 'None'}.

            Please recommend a recipe using ONLY the provided information.
        """
        
        return self.agent.invoke({
            "messages": [{"role": "user", "content": user_input}]
            })


def recipe_agent_node(state: CookingState) -> CookingState:
    recipe_agent = RecipeGeneratorAgent()
    result = recipe_agent.invoke(state)
    recipe: Recipe = result["structured_response"] 
    print(recipe.model_dump_json(indent=2))
    return {
        **state,
        "recipe": recipe.model_dump(),
        "llm_calls": state["llm_calls"] + 1,
    }
