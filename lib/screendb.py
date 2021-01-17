import os

from kivy.config import Config
os.environ["KIVY_NO_FILELOG"] = "1"
#os.environ["KIVY_NO_CONSOLELOG"] = "0"
os.environ['KIVY_HOME'] = os.getcwd()
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('graphics', 'resizable', True)
Config.write()

from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabsBase
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App

from lib import database
from lib.dialog import Dialog
from lib.setting import Setting
setting = Setting()
backend = setting.backend
username = ""
password = ""
if backend == "MySQL":
    password = setting.password
    username = setting.username
    dbname = setting.dbname
dbname = setting.dbfile
engine = database.db(backend, dbname=dbname,
                     username=username, password=password)

conn = database.create(engine=engine)
trans = conn.begin()
dlg = Dialog()

class ScreenDb(MDScreen):

    def get_textinputs(self):
        txtinputs = (self.ids.txt_name,
                     self.ids.txt_fname,
                     self.ids.txt_mname,
                     self.ids.txt_phone,
                     self.ids.txt_addr,
                     self.ids.txt_class,
                     self.ids.txt_section,
                     self.ids.txt_rno,
                     self.ids.txt_ano, )
        return txtinputs

    def get_text(self):
        kwargs = {"addmission_no": self.ids.txt_ano.text,
                  "connection": conn,
                  "trans": trans,
                  "name": self.ids.txt_name.text,
                  "father_name": self.ids.txt_fname.text,
                  "mother_name": self.ids.txt_mname.text,
                  "phone": self.ids.txt_phone.text,
                  "addr": self.ids.txt_addr.text,
                  "clss": self.ids.txt_class.text,
                  "roll_no": self.ids.txt_rno.text,
                  "section": self.ids.txt_section.text}
        return kwargs

    def btn_add_click(self):
        kwargs = self.get_text()
        dlg.title = "Empty field(s)"
        dlg.text = "All fields are required."

        for val in kwargs.values():
            if val == "":
                dlg.open()
                return
        database.add_student(**kwargs)
        self.btn_clear_click()

    def filter(self, text, from_undo):
        if text.isdigit():
            return text

    def btn_update_click(self):
        kwargs = self.get_text()
        database.update_student(**kwargs)
        self.btn_clear_click()

    def btn_Find_click(self):
        data = database.get_detail(conn, trans,
                                   self.ids.txt_ano.text)
        colmns = [i for i in range(8)] + [16]

        inputs = self.get_textinputs()
        dlg.title = "Empty field"
        dlg.text = "Enter Addmission Number"

        if inputs[8].text == "":
            dlg.open()
            return 0
        if data:
            for i, j in zip(colmns, inputs):
                j.text = str(data[i])
            return

        dlg.text = "No data found"
        dlg.title = "Not found!"
        dlg.open()

    def btn_clear_click(self):
        inputs = self.get_textinputs()

        for i in inputs:
            i.text = ""

    def find_marks(self):
        ano = self.ids.txt_an.text
        if not ano:
            dlg.text = "Error"
            dlg.title = "Enter Addmission Number"
            dlg.open()
            return
        data = database.find_marks(conn, trans, ano)
        if not data:
            dlg.text = "No data found"
            dlg.title = "Not found!"
            dlg.open()
            return
        else:
            self.ids.txt_marks.text = data

    def add_marks(self):
        ano = self.ids.txt_an.text
        marks = self.ids.txt_marks.text
        if not ano:
            dlg.text = "Error"
            dlg.title = "Enter Addmission Number"
            dlg.open()
            return
        data = database.find_marks(conn, trans, ano)
        if data:
            database.add_marks(conn, trans, ano, marks)
        else:
            dlg.text = "Error"
            dlg.title = "No data found!"
            dlg.open()
            return

    def btn_Remove_click(self):
        data = database.get_detail(conn, trans,
                                   self.ids.txt_ano.text)
        ano = self.ids.txt_ano.text
        if not ano:
            dlg.text = "Error"
            dlg.title = "Enter Addmission Number"
            dlg.open()
            return
        if data:
            database.delete(conn, trans, self.ids.txt_ano.text)
        else:
            dlg.text = "Error"
            dlg.title = "No data found!"
            dlg.open()
            return

    def create_card(self):

        data = database.find_marks(conn, trans, self.ids.txt_an.text)
        if not data:
            dlg.text = "No data found"
            dlg.title = "Not found!"
            dlg.open()
            return
        else:
            total = 0
            root = App.get_running_app().root  #
            for i, j in zip(data.split(), range(7)):
                total += float(i)
                root.ids.scr.get_screen(
                    'screencard').ids[f"txt_{j}"].text += (" " * 100) + i

            root.ids.scr.get_screen(
                'screencard').ids.txt_total.text = "Total " + str(total)
            root.ids.scr.get_screen(
                'screencard').ids.txt_percent.text \
                = "Percent " + str(total / 8)
            App.get_running_app().root.ids.scr.current = 'screencard'

    def btn_setting_click(self):
        App.get_running_app().root.ids.scr.current = 'settings'


class Tab(FloatLayout, MDTabsBase):
    pass


class ScreenCard(MDScreen):
    pass
