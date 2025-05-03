from google.oauth2 import id_token as firebase_id_token
from google.auth.transport import requests

firebase_request_adapter = requests.Request()

def validate_firebase_token(id_token):
    if not id_token:
        return None

    try:
        decoded_token = firebase_id_token.verify_firebase_token(id_token, firebase_request_adapter)
        
        # Debugging: print decoded token
        print("Decoded Token:", decoded_token)

        # Safe fallback
        uid = decoded_token.get('uid') or decoded_token.get('sub')
        if not uid:
            print("UID not found in token.")
            return None
        
        # Attach uid manually if not present
        if 'uid' not in decoded_token and 'sub' in decoded_token:
            decoded_token['uid'] = decoded_token['sub']
        
        return decoded_token

    except ValueError as err:
        print("Token validation error:", str(err))
        return None
