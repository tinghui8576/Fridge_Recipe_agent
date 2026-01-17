import firebase_admin
from firebase_admin import credentials, firestore
from typing import Dict, Optional
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

class UserCookingStateDB:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.doc_ref = db.collection("users").document(user_id)
    
    def exists(self) -> bool:
        return self.doc_ref.get().exists
    
    def create_user(self, data: dict):
        self.doc_ref.set({
            **data,
            "last_updated": firestore.SERVER_TIMESTAMP
        })

    def get_state(self) -> Dict:
        return self.doc_ref.get().to_dict()

    def add_items(self, field: str, items: Dict[str, int]):
        """
        field: 'fridge_items', 'spices', or 'equipment'
        items: dictionary of {item_name: quantity}
        """
        doc = self.get_state()
        current = doc.get(field, {})
        for k, v in items.items():
            current[k] = current.get(k, 0) + v
        self.doc_ref.update({
            field: current,
            "last_updated": firestore.SERVER_TIMESTAMP
        })

    def use_items(self, field: str, items: Dict[str, int]):
        """
        Reduce quantities when used in a recipe
        """
        doc = self.get_state()
        current = doc.get(field, {})
        for k, v in items.items():
            if k in current:
                current[k] = max(current[k] - v, 0)
                if current[k] == 0:
                    del current[k] 
        self.doc_ref.update({
            field: current,
            "last_updated": firestore.SERVER_TIMESTAMP
        })