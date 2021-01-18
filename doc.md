# System Requirement

### Hardware Requirement

- RAM 256Mb **Recommended 512Mb**
- CPU Architecture- x86, x86_64, Arm

### Software Requirement

- Operating System- Windows7 (Updated) and above , Linux , Mac
- MySQL
- python3.7 (Must Added To path)

### Project Directory Structure

```
vidyalyaManegment
├── assest
│   └── user.png
├── lib
│   ├── database.py
│   ├── dialog.py
│   ├── __init__.py
│   ├── screendb.py
│   └── setting.py
├── main.py
├── ui
│   ├── screenDatabase.kv
│   └── setting.kv
├──vmanegar.py
└── requiremts.txt
```

### setting Up development Environment

```bash
pip install virtualenv
```
```bash
virtualenv vidyalyaManegment 

vidyalyaManegment\scripts\activate

pip install -r requrements.txt
```


### requirement.txt

```
kivy==2.0.0
SQLAlchemy==1.3.22 
PyMySQL==1.0.2
kivymd
```

### File Contents

- lib/database.py

```python
from sqlalchemy import Column, Integer, String, Table, Float
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from lib.dialog import Dialog

d = Dialog()
meta = MetaData()


def db(backend, dbname, username="", password="", host="localhost"):
    if backend == "SQLite":
        engine = create_engine(f'sqlite:///{dbname}', )
        return engine
    else:
        engine = create_engine(
            f"mysql+pymysql://{username}:{password}@{host}/{dbname}")
        return engine


students = Table(
    'students', meta,
    Column('name', String),
    Column('father_name', String),
    Column('mother_name', String),
    Column('phone', String),
    Column('addr', String),
    Column('class', String),
    Column('section', String),
    Column('roll_no', Integer),
    Column('english', Float),
    Column('math', Float),
    Column('science', Float),
    Column('computer', Float),
    Column('hindi', Float),
    Column('social', Float),
    Column('music', Float),
    Column('art', Float),
    Column('addmission_no', Integer, primary_key=True),
)


def create(engine):
    meta.create_all(engine)
    conn = engine.connect()

    return conn


def get_detail(conn, trans, addmission_no):
    query = students.select().where(students.c.addmission_no == int(addmission_no))
    result = conn.execute(query)
    result = result.fetchone()
    return result


def update_student(connection, trans, addmission_no, name="",
                   father_name="", mother_name="", phone="",
                   addr="", clss="", roll_no="", section=""):

    kwargs = {"name": name,
              "father_name": father_name,
              "mother_name": mother_name,
              "phone": phone,
              "addr": addr,
              "class": clss,
              "roll_no": int(roll_no) if roll_no else "",
              "section": section}

    kwargs_ = dict()
    for key in kwargs:
        if kwargs[key] != "":
            kwargs_[key] = kwargs[key]
    update = \
        students.update() \
        .where(students.c.addmission_no == int(addmission_no)) \
        .values(**kwargs_)
    result = connection.execute(update)
    trans.commit()

    return result


def add_student(connection, trans, addmission_no, name,
                father_name, mother_name, phone,
                addr, clss, roll_no, section):
    kwargs = {"addmission_no": int(addmission_no),
              "name": name,
              "father_name": father_name,
              "mother_name": mother_name,
              "phone": phone,
              "addr": addr,
              "class": clss,
              "roll_no": int(roll_no),
              "section": section}
    data = get_detail(connection, trans, addmission_no)
    if not data:
        insert = students.insert().values(**kwargs)
        result = connection.execute(insert)
        trans.commit()
        return result
    else:
        d.title = "Exists"
        d.text = "Data already exists. Do you want to update"
        d.open()
        if d.result == 1:
            update_student(**kwargs)


def delete(conn, trans, addmission_no):
    delete = students.delete() \
        .where(students.c.addmission_no == int(addmission_no))
    result = conn.execute(delete)
    trans.commit()
    return result


def add_marks(conn, trans, addmission_no, marks):
    if len(marks) < 8:
        m_len = 8 - len(marks)
        marks = marks.split() + [0] * m_len
    new_marks = list(map(float, marks.split()))
    subjects = ('english', 'math', 'science', 'computer',
                'hindi', 'social', 'music', 'art')
    kwargs = dict(zip(subjects, new_marks))
    update = \
        students.update() \
        .where(students.c.addmission_no == int(addmission_no)) \
        .values(**kwargs)
    result = conn.execute(update)
    trans.commit()
    return result


def find_marks(conn, trans, addmission_no):
    data = get_detail(conn, trans, addmission_no)
    marks = ""
    if data:
        for i in range(8, 15):
            marks += str(data[i]) + " "
    return marks
```

- lib/screendb.py

```python
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
```

- lib/dialog.py
  
  ```python
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
  
  ```
- lib\setting.py

```python
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
```

- ui/screenDatabase.kv
  
  ```python
  <CMDTextField@MDTextField>:
      line_spacing: 10      
  <ScreenDb>:
      name:"screendb"
      MDTabs:
          id: tabs
          lock_swiping:True
          Tab:
              text: 'Student'
              ScrollView:
                  effect_cls:"ScrollEffect"
                  MDGridLayout:
                      cols:1
                      padding:[40,10,40,10]
                      pos_hint: {'center_x': .5, 'center_y': .5}
                      adaptive_height: True
                      CMDTextField:
                          id:txt_name
                          hint_text: "Student Name"
                      CMDTextField:
                          id:txt_fname
                          hint_text: "Father's Name"
                      CMDTextField:
                          id:txt_mname
                          hint_text: "Mother's Name"
                      CMDTextField:
                          id:txt_phone
                          hint_text: "Contact Number"
                      CMDTextField:
                          id:txt_addr
                          hint_text: "Address"
                      CMDTextField:
                          id:txt_class
                          hint_text: "Class"
                      CMDTextField:
                          id:txt_section
                          hint_text: "Section"
                      CMDTextField:
                          id:txt_rno
                          hint_text: "Roll No"
                          input_filter:root.filter
                      CMDTextField:
                          id:txt_ano
                          hint_text: "Addmission No"
                          input_filter:root.filter
                      MDGridLayout:                        
                          rows: 1
                          adaptive_height: True
                          spacing:[20,20]
                          MDRaisedButton:
                              text: 'Add'
                              on_release:root.btn_add_click()   
                          MDRaisedButton:
                              text: 'Update'
                              on_release:root.btn_update_click()
                          MDRaisedButton:
                              text: 'Find'
                              on_release:root.btn_Find_click()
                          MDRaisedButton:
                              text: 'Remove'
                              on_release:root.btn_Remove_click()
                          MDRaisedButton:
                              text: 'Clear'
                              on_release:root.btn_clear_click()
                          MDIconButton:
                              icon: 'tools'
                              pos_hint:{"right":1,"bottom":1}
                              on_release:root.btn_setting_click()
          Tab:
              text:"Marks"
              ScrollView:
                  effect_cls:"ScrollEffect"
                  MDGridLayout:
                      pos_hint: {'center_x': .5, 'center_y': .5}
                      cols:1
                      padding:[40,40,40,40]
  
                      adaptive_height: True
                      MDLabel:
                          text:"English Maths Science Computer Hindi Social Music Art"
                          size_hint: (1, None)
                          height: 30
                      CMDTextField:
                          id:txt_marks
                          hint_text:"Enter marks seperated by space"
                      CMDTextField:
                          id:txt_an
                          hint_text: "Addmission No"
                          input_filter:root.filter
                      MDGridLayout:
                          rows:1
                          spacing: 10
                          MDRaisedButton:
                              text: 'Add/Update'
                              on_release:root.add_marks()
                          MDRaisedButton:
                              text: 'Find'
                              on_release:root.find_marks()
                          MDRaisedButton:
                              text: 'Create Report Card'
                              on_release:root.create_card()
  <ScreenCard>:
      name:"screencard"
      MDCard:
          size_hint: None, None
          size: "680dp", "580dp"
          pos_hint: {"center_x": .5, "center_y": .5}
          padding: "8dp"
  
          MDGridLayout:
              spacing: 5
              adaptive_height:True
              rows:3
              MDLabel:
                  text: (" "*46)+'Sanatan International Academy'+(" "*46)+"\n"
              MDBoxLayout:
                  adaptive_height:True
                  spacing: 10
  
                  Image:
                      size_hint: None, None
                      size: "128dp", "128dp"
                      source: "assest/user.png"
                      pos_hint: {"center_x": .5, "center_y": .5}
                  MDLabel:
                      markup: True
                      text:"[b]sdf[b]\nn\nm\nr s s\n"
              MDBoxLayout:
                  cols:1
                  size_hint_y: None
                  height: 400
                  padding:[0,0,0,0]
                  #pos_hint: {"y":.08}
                  pos: (44, 44)
                  spacing:3
                  orientation: 'vertical'
                  MDLabel:
                      id:txt_0
                      text:"English "
                  MDLabel:
                      id:txt_1
                      text:"Math    "
                  MDLabel:
                      id:txt_2
                      text:"Science "
                  MDLabel:
                      id:txt_3
                      text:"Computer"
                  MDLabel:
                      id:txt_4
                      text:"Hindi   "
                  MDLabel:
                      id:txt_5
                      text:"Social   "
                  MDLabel:
                      id:txt_6
                      text:"Music   "
                  MDLabel:
                      id:id:txt_7
                      text:"Art     "
                  MDBoxLayout:
                      MDLabel:
                          text: 'Total'
                          id:txt_total
                      MDLabel:
                          id:txt_percent
                          text:"Percentage"
  ```


- ui/setting.kv
  ```python
  #:import App kivy.app.App
  <ScreenSetting>:
      name:"settings"
      MDIconButton:
          icon: 'brightness-6'
          pos_hint:{"right":1,"top":1}
          id:btn_theme
          on_release:root.btn_theme_click()
      MDBoxLayout:
          padding:[50,50,50,50]
          id:layout_setting
          orientation: 'vertical'
          # adaptive_height: True
          # pos_hint: {'center_x': .5, 'center_y': .5}
  
          MDBoxLayout:
              size_hint_y: .2
              MDLabel:
                  text:"Database Backend"
                  size_hint: (None, None)
                  pos_hint: { 'center_y': .5,'center_y': .5}
  
                  width: 400
                  #color:App.get_running_app().opposite_colors
              MDDropDownItem:
                  id: db_backend
                  text: 'SQLite'
                  pos_hint: { 'center_y': .5,'center_y': .5}
                  on_release: root.menu.open()
  
          MDBoxLayout:
              orientation: 'vertical'
              size_hint_y: None
              height: 300
              id:layout_myql
              MDTextField:
                  id:txt_uname
                  hint_text: "User Name"
                  line_spacing: 10
                  disabled: True if db_backend.current_item =="SQLite" else False
  
              MDTextField:
                  id:txt_pass
                  hint_text: "Password"
                  line_spacing: 10
                  disabled: True if db_backend.current_item =="SQLite" else False                
              MDTextField:
                  id:txt_dbname
                  hint_text: "Database Name Or path"
                  line_spacing: 10
                  input_filter: lambda text, from_undo: text[:64 - len(self.text)]
              MDRaisedButton:
                  pos_hint: {'center_x': .5, 'center_y': .5}
                  text:"Apply Changes"
                  on_release:root.btn_change_click()
  ```


- vmanegar.py
  
  ```python
   import os
   from kivy.config import Config
  
   # os.environ["KIVY_NO_FILELOG"] = "1"
   # #os.environ["KIVY_NO_CONSOLELOG"] = "0"
   # os.environ['KIVY_HOME'] = os.getcwd()
  
   # Config.set('input', 'mouse', 'mouse,disable_multitouch')
   # Config.set('graphics', 'window_state', 'maximized')
   # Config.write()
  
   from kivymd.app import MDApp
   from kivy.app import App
   from kivy.lang import Builder
  
   # from kivy.core.text import LabelBase
  
   # from kivymd.font_definitions import theme_font_styles
  
   from kivy.uix.screenmanager import ScreenManager
  
   from lib.setting import Setting
  
   ui_files = os.listdir("ui")
   setting = Setting()
   for ui_file in ui_files:
       Builder.load_file(os.path.join("ui", ui_file))
  
   if os.path.exists("settings.db"):
       if setting.dbfile and setting.dbname:
           setting.firstscreen = "ScreenDb"
           setting.secondscreen = "ScreenSetting"
       else:
           setting.firstscreen = "ScreenSetting"
           setting.secondscreen = "ScreenDb"
   else:
       setting.firstscreen = "ScreenSetting"
       setting.secondscreen = "ScreenDb"
   setting.save_setting()
   fs = setting.firstscreen
   ss = setting.secondscreen
  
   kv = f'''
   #:import ScreenSetting lib.setting.ScreenSetting
   #:import ScreenDb lib.screendb.ScreenDb
   #:import ScreenCard lib.screendb.ScreenCard
   MDBoxLayout:
       ScrnManager:
           id:scr
           {fs}:
           {ss}:
           ScreenCard:
   '''
  
   class ScrnManager(ScreenManager):
       pass
  
   class VidyalayaManegment(MDApp):
       def build(self):
           # LabelBase.register(
           #     name="JetBrains Mono",
           #     fn_regular="assest/JetBrainsMono-Regular.ttf")
  
           # theme_font_styles.append('JetBrains Mono')
           # self.theme_cls.font_styles["JetBrains Mono"] = [
           #     "JetBrains Mono",
           #     16,
           #     False,
           #     0.15,
           # ]
           self.theme_cls.primary_palette = "BlueGray"
           self.theme_cls.theme_style = setting.theme  # "Light"
           ROOT_LAYOUT = Builder.load_string(kv)
           return ROOT_LAYOUT
  
       # def on_start(self):
       #     App.get_running_app().root.ids.scr.current = 'screendb'
  
   def main():
       Vidyalaya_manegment = VidyalayaManegment()
       Vidyalaya_manegment.run()
   if __name__ == "__main__":
       main()
  ```


- main.py
  
  ```python
  import vmanegar
  vmanegar.main()
  ```


### To run the Application

```bash
python main.py
```

