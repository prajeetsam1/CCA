from cryptography.fernet import Fernet

# ⚠️ Must be shared between both apps
FERNET_KEY = Fernet.generate_key()
fernet = Fernet(FERNET_KEY)

def encrypt(msg):
    return fernet.encrypt(msg.encode()).decode()

def decrypt(token):
    return fernet.decrypt(token.encode()).decode()
