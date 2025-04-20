from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests

FIREBASE_API_KEY = "YOUR_FIREBASE_API_KEY"

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.email = TextInput(hint_text="Email")
        self.password = TextInput(hint_text="Password", password=True)
        login_btn = Button(text="Login", on_press=self.login)
        signup_btn = Button(text="Sign Up", on_press=self.signup)

        for widget in [self.email, self.password, login_btn, signup_btn]:
            layout.add_widget(widget)
        self.add_widget(layout)

    def signup(self, _):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
        self._auth_request(url)

    def login(self, _):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
        self._auth_request(url)

    def _auth_request(self, url):
        payload = {
            "email": self.email.text,
            "password": self.password.text,
            "returnSecureToken": True
        }
        res = requests.post(url, json=payload).json()
        if "idToken" in res:
            self.manager.get_screen('chat').init_user(res["email"], res["idToken"])
            self.manager.current = 'chat'
        else:
            print("Auth failed:", res.get("error", {}).get("message", "Unknown error"))
