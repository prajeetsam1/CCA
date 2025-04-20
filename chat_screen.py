from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import threading
import requests
import time
from utils import encrypt, decrypt

FIREBASE_DB_URL = "https://YOUR_PROJECT.firebaseio.com/messages.json"

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.email = None
        self.id_token = None
        self.chat_box = BoxLayout(orientation='vertical', size_hint_y=None)
        self.chat_box.bind(minimum_height=self.chat_box.setter('height'))
        self.scroll = ScrollView()
        self.scroll.add_widget(self.chat_box)

        self.msg_input = TextInput(size_hint_y=0.1, multiline=False)
        send_btn = Button(text="Send", size_hint_y=0.1, on_press=self.send_msg)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.scroll)
        layout.add_widget(self.msg_input)
        layout.add_widget(send_btn)

        self.add_widget(layout)

    def init_user(self, email, id_token):
        self.email = email
        self.id_token = id_token
        threading.Thread(target=self.listen_for_msgs, daemon=True).start()

    def send_msg(self, _):
        if not self.msg_input.text.strip():
            return
        msg = {
            "from": self.email,
            "text": encrypt(self.msg_input.text.strip()),
            "timestamp": time.time(),
            "read": False,
            "isVanish": True
        }
        requests.post(FIREBASE_DB_URL, json=msg)
        self.msg_input.text = ""

    def listen_for_msgs(self):
        while True:
            res = requests.get(FIREBASE_DB_URL).json()
            self.chat_box.clear_widgets()
            if res:
                for k, msg in sorted(res.items(), key=lambda x: x[1]['timestamp']):
                    if msg['from'] == self.email:
                        who = "You"
                    else:
                        who = "GF"
                        if msg.get("isVanish") and not msg.get("read"):
                            # delete after read
                            requests.delete(f"{FIREBASE_DB_URL[:-5]}/{k}.json")
                    label = Label(text=f"[{who}]: {decrypt(msg['text'])}", size_hint_y=None, height=30)
                    self.chat_box.add_widget(label)
            time.sleep(2)
