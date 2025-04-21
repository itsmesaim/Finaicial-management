from google.oauth2 import id_token as firebase_id_token
from google.auth.transport import requests

firebase_request_adapter = requests.Request()


# def validateFirebaseToken(id_token):
#     if not id_token:
#         return None
    
#     user_token =None
    
#     try:
#         return google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
#     except ValueError as err:
#         print("Token validation error:", str(err))
#         return None
#     return user_token


def validate_firebase_token(id_token):
    if not id_token:
        return None
    try:
        return firebase_id_token.verify_firebase_token(id_token, firebase_request_adapter)
    except ValueError as err:
        print("Token validation error:", str(err))
        return None
