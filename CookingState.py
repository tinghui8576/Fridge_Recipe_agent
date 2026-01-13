from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator

class CookingState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    weather: str | None
    dietary_restrictions: list[str]
    fridge_items: list[str]
    spices: list[str]
    equipment: list[str]
    llm_calls: int
    
