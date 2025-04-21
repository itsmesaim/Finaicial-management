from google.cloud import firestore
from google.cloud.firestore import DocumentReference
from datetime import datetime

firestore_db = firestore.Client()

class FirestoreService:

    @staticmethod
    def create_user(user_id: str, email: str, display_name: str = "") -> DocumentReference:
        user_data = {
            "email": email,
            "display_name": display_name,
            "created_at": firestore.SERVER_TIMESTAMP,
        }
        return firestore_db.collection("users").document(user_id).set(user_data)

    @staticmethod
    def get_user(user_id: str):
        user_ref = firestore_db.collection("users").document(user_id)
        user = user_ref.get()
        if user.exists:
            data = user.to_dict()
            data["id"] = user_id
            return data
        return None
