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
    def get_user(user_id):
        from google.cloud import firestore
        db = firestore.Client()
        user_ref = db.collection('users').document(user_id)
        doc = user_ref.get()
        if doc.exists:
            return doc.to_dict()
        return None

    #to save the bank information
    @staticmethod
    def save_bank_account_info(uid, account_holder_name, account_last4, bank_name, account_type):
        bank_data = {
            'account_holder_name': account_holder_name,
            'account_last4': account_last4,
            'bank_name': bank_name,
            'account_type': account_type,
            'created_by_uid': uid,
            'created_at': datetime.utcnow()
        }
        return firestore_db.collection('bank_accounts').document(uid).set(bank_data)



    @staticmethod
    def get_all_users():
        from google.cloud import firestore
        db = firestore.Client()
        users_ref = db.collection('users')
        docs = users_ref.stream()
        all_users = []
        for doc in docs:
            all_users.append(doc.to_dict())
        return all_users

    @staticmethod
    def save_transaction(user_id, amount):
        from google.cloud import firestore
        db = firestore.Client()
        transactions_ref = db.collection('transactions')
        transactions_ref.add({
            "user_id": user_id,
            "amount": amount,
            "timestamp": firestore.SERVER_TIMESTAMP
        })

    @staticmethod
    def save_user(user_id, email, name):
        from google.cloud import firestore
        db = firestore.Client()
        user_ref = db.collection('users').document(user_id)
        user_ref.set({
            "email": email,
            "name": name,
            "uid": user_id
        })

    @staticmethod
    #def add_event_budget():
    #def get_event_budgets(user_id):

    # To Save a new overspending alert.
    @staticmethod
    def save_alert(user_id, alert_data):
        from google.cloud import firestore
        db = firestore.Client()
        alerts_ref = db.collection('users').document(user_id).collection('alerts')
        alerts_ref.add({
            **alert_data,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
    # Retrieve all overspending alerts for the given user.
    @staticmethod
    def get_user_alerts(user_id):
        from google.cloud import firestore
        db = firestore.Client()
        alerts_ref = db.collection('users').document(user_id).collection('alerts')
        docs = alerts_ref.stream()
        all_alerts = []
        for doc in docs:
            alert = doc.to_dict()
            alert['alert_id'] = doc.id
            all_alerts.append(alert)
        return all_alerts

    @staticmethod
    def delete_alert(user_id, alert_id):
        from google.cloud import firestore
        db = firestore.Client()
        alert_ref =db.collection('users').document(user_id).collection('alerts').document(alert_id)
        if alert_ref.get().exists:
            alert_ref.delete()
            return True
        return False

