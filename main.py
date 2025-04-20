from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from login_screen import LoginScreen
from chat_screen import ChatScreen

class ChatApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(ChatScreen(name='chat'))
        return sm

if __name__ == '__main__':
    ChatApp().run()
