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
    #to save the bank information
    @staticmethod
    def save_bank_account_info(uid, account_holder_name, account_last4):
        bank_data = {
            'account_holder_name': account_holder_name,
            'account_last4': account_last4,
            'created_by_uid': uid,
            'created_at': datetime.utcnow()
        }
        return firestore_db.collection('bank_accounts').document(uid).set(bank_data)
    

