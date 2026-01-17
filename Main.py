
from utils.UIManager import UIManager
from utils.GraphFlows import run_recipe_graph

if __name__ == "__main__":
    username = input("Enter your username: ").strip()
    manager = UIManager(username)
    while True:
        print("\nOptions:")
        print("A → Add items")
        print("C → Check what's in my fridge")
        print("R → Generate recipe")
        print("Q → Quit")

        choice = input("Choose: ").upper()

        if choice == "A":
            f = input("F=fridge, S=spices, E=equipment: ").upper()
            field_map = {"F": "fridge_items", "S": "spices", "E": "equipment"}
            if f in field_map:
                items = manager._parse_items(f"Add {field_map[f]} (item:qty): ")
                manager.db.add_items(field_map[f], items)
        elif choice == "C":
            manager.show_state()
        elif choice == "R":
            print("🍳 Generating recipe...")

            cooking_state = manager.firestore_to_cooking_state()

            result = run_recipe_graph(cooking_state)

            recipe = result.get("recipe")
            if recipe:
                print("\n✅ Recipe generated:")
                print("Title:", recipe.get("title"))
                print("Ingredients:", recipe.get("ingredients"))
                print("Steps:")
                for step in recipe.get("steps", []):
                    print("-", step)
                print("Notes", recipe.get("notes"))

            else:
                print("❌ No valid recipe generated.")
        elif choice == "Q":
            print("Goodbye 👋")
            break
        else:
            print("Invalid option, try again.")
