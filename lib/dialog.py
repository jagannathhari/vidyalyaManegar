from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.app import App


class Dialog(MDDialog):
    def __init__(self, **kwargs):

        self.btn1text = "Ok"
        self.btn2text = "Cancle"
        self.title = "Dialog"
        self.text = ""
        self.result = 0
        self.buttons = [
            MDFlatButton(
                text=self.btn1text,
                text_color=App.get_running_app().theme_cls.primary_color,
                on_release=self.btn1click
            ),
            MDFlatButton(
                text=self.btn2text,
                text_color=App.get_running_app().theme_cls.primary_color,
                on_release=self.btn2click
            ),
        ]
        super().__init__(**kwargs)

    def btn2click(self, x):
        self.dismiss()
        self.result = 0

    def btn1click(self, x):
        self.dismiss()
        self.result = 1
