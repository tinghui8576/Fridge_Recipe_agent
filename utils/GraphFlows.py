from utils.States import CookingState
from utils.RecipeAgent import recipe_agent_node
from langgraph.graph import StateGraph, END

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

def run_recipe_graph(state: CookingState) -> CookingState:
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
    return app.invoke(state)