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
