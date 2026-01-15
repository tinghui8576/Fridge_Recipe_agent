from States import CookingState, Recipe
from RecipeAgent import recipe_agent_node

def validate_node(state: CookingState) -> CookingState:
    errors = []

    recipe = state.get("recipe", {})
    ingredients = recipe.get("ingredients", [])

    for i in ingredients:
        if i not in state["fridge_items"]:
            errors.append(i)

    if errors:
        return {
            **state,
            "valid": False,
            "error": f"Invalid ingredients: {errors}"
        }

    return {
        **state,
        "valid": True,
        "error": None
    }

def route_after_validation(state: CookingState) -> str:
    if state["valid"]:
        print("✅ Recipe is valid, proceeding to END.")
        return "end"
    
    # Retry limit
    if state["llm_calls"] >= 3:
        print(f"⚠️ Retry limit reached (llm_calls={state['llm_calls']}), stopping.")
        return "end"
    
    print(f"❌ Recipe invalid: {state['error']}, retrying...")
    return "retry"


state: CookingState = {
    "messages": [],
    "city": "taipei",
    "dietary_restrictions": [],
    "fridge_items": ["apple", "flour", "butter"],
    "spices": ["salt", "pepper", "cinnamon", "sugar"],
    "equipment": ["pan", "spatula"],
    "llm_calls": 0
}

from langgraph.graph import StateGraph, END

graph = StateGraph(CookingState)
graph.add_node("generate", recipe_agent_node)
graph.add_node("validate", validate_node)
graph.add_node("retry", recipe_agent_node)

graph.set_entry_point("generate")

graph.add_edge("generate", "validate")
graph.add_edge("retry", "validate")

graph.add_conditional_edges(
    "validate",
    route_after_validation,
    {
        "retry": "retry",
        "end": END
    }
)

app = graph.compile()
result = app.invoke(state)
print(result)