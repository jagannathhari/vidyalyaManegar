import json
import string
import os

from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from lib.dialog import Dialog
from kivy.clock import Clock


class Setting:
    def __init__(self):
        self.setting_file = "settings.db"
        self.theme = "Dark"
        self.username = ""
        self.password = ""
        self.backend = "SQLite"
        self.height = 800
        self.width = 800
        self.dbfile = ""
        self.dbname = ""
        self.firstscreen = "ScreenSetting"
        self.secondscreen = "ScreenDb"
        self.setting = self.load_setting()

    def _setting(self):
        data = {"theme": self.theme,
                "username": self.username,
                "password": self.password,
                "dbfile": self.dbfile,
                "dbname": self.dbname,
                "height": self.height,
                "widht": self.width,
                "backend": self.backend,
                "firstscreen": self.firstscreen,
                "secondscreen": self.secondscreen}
        return data

    def set_theme(self, theme):
        self.theme = theme

    def set_username(self, username):
        self.username = username.strip()

    def set_password(self, password):
        self.password = password.strip()

    def set_dbfile(self, file):
        self.dbfile = file.strip()

    def set_dbname(self, name):
        self.dbname = name.strip()

    def set_height(self, h):
        self.height = h

    def set_width(self, w):
        self.widht = w

    def set_backend(self, backend):
        self.backend = backend

    def load_setting(self):
        if os.path.exists(self.setting_file):
            with open(self.setting_file) as sfile:
                data = json.load(sfile)
                self.theme = data["theme"]
                self.username = data["username"]
                self.password = data["password"]
                self.backend = data["backend"]
                self.height = data["height"]
                self.width = data["widht"]
                self.dbfile = data["dbfile"]
                self.dbname = data["dbname"]
                self.secondscreen = data["secondscreen"]
                self.firstscreen = data["firstscreen"]

    def save_setting(self):
        with open(self.setting_file, "w") as write_file:
            self.setting = self._setting()
            write_file.write(json.dumps(self.setting, indent=4))


class ScreenSetting(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        menu_items = [{"icon": "database", "text": "SQLite"},
                      {"icon": "database", "text": "MySQL"}]
        self.menu = MDDropdownMenu(
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.menu.bind(on_release=self.set_item)

        Clock.schedule_once(self.on_screen_paint)

    def on_screen_paint(self, *args):
        self.menu.caller = self.ids.db_backend
        setting = Setting()
        self.ids.db_backend.set_item(setting.backend)
        self.ids.txt_uname.text = setting.username
        self.ids.txt_pass.text = setting.password
        if setting.backend == "SQLite":
            self.ids.txt_dbname.text = setting.dbfile
        else:
            self.ids.txt_dbname.text = setting.dbname

    def set_item(self, instance_menu, instance_menu_item):
        self.ids.db_backend.set_item(instance_menu_item.text)
        self.menu.dismiss()
        setting = Setting()
        setting.backend = instance_menu_item.text
        setting.save_setting()

    def btn_theme_click(self):
        theme = App.get_running_app().theme_cls
        setting = Setting()
        if theme.theme_style == "Dark":
            theme.theme_style = "Light"
            setting.theme = "Light"
        else:
            theme.theme_style = "Dark"
            setting.theme = "Dark"
        setting.save_setting()

    def btn_change_click(self):
        dialog = Dialog()
        dialog.title = "Error!"
        setting = Setting()
        if self.ids.txt_dbname.text == "":

            dialog.text = "DataBase Name Or Path Can't Empty"
            dialog.open()
            return None
        else:

            acsii_letter = string.ascii_letters + string.digits
            file_path, file_name = os.path.split(self.ids.txt_dbname.text)
            if os.path.isdir(file_path):
                setting.dbfile = self.ids.txt_dbname.text
            name = ""
            for i in self.ids.txt_dbname.text:
                if i in acsii_letter:
                    name += i
            self.ids.txt_dbname.text = name
            setting.set_dbname(name)

        if self.ids.db_backend.current_item == "MySQL":
            username = self.ids.txt_uname.text
            password = self.ids.txt_pass.text

            if username and password:
                setting.username = self.ids.txt_uname.text
                setting.password = self.ids.txt_pass.text

            else:

                dialog.text = "Username or Password can,t be Empty"
                dialog.open()
                return None
        setting.save_setting()
        App.get_running_app().root.ids.scr.current = 'screendb'
