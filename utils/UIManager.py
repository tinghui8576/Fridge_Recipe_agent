from utils.UserCookingStateDB import UserCookingStateDB
from utils.States import CookingState

class UIManager:
    def __init__(self, username: str):
        self.username = username
        self.db = UserCookingStateDB(username)

        if not self.db.exists():
            print("👋 New user detected. Let's set up your fridge!")
            self.first_time_setup()
        else:
            print(f"👋 Welcome back, {username}!")
            
    def _parse_items(self, prompt: str):
        items_str = input(prompt)
        items = {}

        for pair in items_str.split(","):
            pair = pair.strip()
            if not pair:
                continue
            if pair.upper() == 'Q':
                break
            if ":" in pair:
                name, qty = pair.split(":")
                try:
                    qty = int(qty.strip())
                except ValueError:
                    qty = 1
            else:
                name, qty = pair, 1

            items[name.strip()] = items.get(name.strip(), 0) + qty

        return items
    
    def first_time_setup(self):
        city = input("Enter your city: ").strip()
        dietary = input("Do you have any other dietary restrictions?: ").strip()
        fridge_items = self._parse_items("Enter fridge items (item:qty): ")
        spices = self._parse_items("Enter spices (item:qty): ")
        equipment = self._parse_items("Enter equipment (item:qty): ")

        self.db.create_user({
            "city": city,
            "dietary_restrictions": dietary,
            "fridge_items": fridge_items,
            "spices": spices,
            "equipment": equipment,
            "llm_calls": 0
        })
        print("✅ User setup complete!")

    def show_state(self):
        """Show current data with quantities"""
        state = self.db.get_state()
        print(f"\n{self.username}'s Data:")
        print(f"City: {state['city']}")
        print(f"Dietary Restrictions: {state['dietary_restrictions']}")
        for field in ["fridge_items", "spices", "equipment"]:
            print(f"{field}:")
            for k, v in state.get(field, {}).items():
                print(f"  - {k}: {v}")
            if not state.get(field):
                print("  (empty)")

    def add_items_ui(self, field: str):
        items = self._parse_items(f"Add {field} (item:qty, comma-separate): ")
        self.db.add_items(field, items)
        print(f"✅ Items added to {field}!")

    def firestore_to_cooking_state(self) -> CookingState:
        data = self.db.get_state()
        return {
            "messages": [],
            "city": data.get("city"),

            "dietary_restrictions": data.get("dietary_restrictions", []),

            "fridge_items": list(data.get("fridge_items", {}).keys()),
            "spices": list(data.get("spices", {}).keys()),
            "equipment": list(data.get("equipment", {}).keys()),

            "recipe": None,
            "llm_calls": 0,
            "valid": None,
            "error": None
        }


