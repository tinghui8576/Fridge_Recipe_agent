from langchain.tools import tool
import requests
from dotenv import load_dotenv
import os

load_dotenv()
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")

url = "https://api.spoonacular.com/recipes/complexSearch"


def search_recipe(
    query: str,
    diet: str | None = None,
    intolerances: str | None = None,
    N_max_results: int =3
) -> str:
    """
    Search for a recipe using Spoonacular complexSearch.
    ingredients: comma-separated
    diet: vegetarian, vegan, keto, etc.
    intolerances: comma-separated (gluten,dairy,...)
    """

    params = {
        "query": query,
        "number": N_max_results,
        "addRecipeInformation": True,
        "apiKey": SPOONACULAR_API_KEY
    }

    if diet:
        params["diet"] = diet
    if intolerances:
        params["intolerances"] = intolerances

    res = requests.get(
        "https://api.spoonacular.com/recipes/complexSearch",
        params=params
    )
    data = res.json()

    if not data.get("results"):
        return "No matching recipe found."

    r = data["results"][0]
    return f"""{r}
        """

state = {
    "messages": [],
    "city": "taipei",
    "dietary_restrictions": [],
    "fridge_items": ["egg", "tomato"],
    "spices": ["salt", "pepper"],
    "equipment": ["pan", "spatula"],
    "llm_calls": 0
}

ingredients = ",".join(state["fridge_items"])
diet = state["dietary_restrictions"][0] if state["dietary_restrictions"] else None

print(ingredients, diet)
print(search_recipe(
    query="Apple Pancakes",
    diet=diet
    ))