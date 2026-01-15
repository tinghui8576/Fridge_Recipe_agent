from langchain.messages import AnyMessage
from typing_extensions import Annotated
from typing import TypedDict, List, Optional
from pydantic import BaseModel
import operator

# -----------------------------
# Define CookingState schema
# -----------------------------
class CookingState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

    # input fields
    city: str | None
    dietary_restrictions: list[str]
    fridge_items: list[str]
    spices: list[str]
    equipment: list[str]

    # recipe fields
    recipe: dict | None

    # stats
    llm_calls: int
    valid: bool | None
    error: str | None
    

# -----------------------------
# Define Recipe schema
# -----------------------------
class Recipe(BaseModel):
    title: str
    ingredients: List[str]
    spices_used: List[str]
    equipment_used: List[str]
    steps: List[str]
    notes: str