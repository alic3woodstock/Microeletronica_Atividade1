import os

import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from genericForm import GenericForm
from myButton import MyButton, MyButtonBorder

os.environ['KIVY_METRICS_DENSITY'] = '1'

kivy.require('2.3.1')
from kivy.config import Config

Config.set('kivy', 'default_font', '["RobotoMono", '
                                   '"fonts/RobotoMono-Regular.ttf", '
                                   '"fonts/RobotoMono-Italic.ttf", '
                                   '"fonts/RobotoMono-Bold.ttf", '
                                   '"fonts/RobotoMono-BoldItalic.ttf"]')

Config.set('kivy', 'kivy_clock', 'free_all')
Config.set('kivy', 'desktop', '1')
Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'minimum_width', '800')
Config.set('graphics', 'minimum_height', '600')
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')
Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.uix.boxlayout import BoxLayout


class FrmPrincipal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        grid = GridLayout(cols=2)
        layout1 = BoxLayout(size_hint=(None, 1), orientation='vertical')
        layout1.width = 200
        generic_form = GenericForm()
        generic_form.add_text_field("μn:", 'y')
        generic_form.add_text_field("Cox:", 'c')
        generic_form.add_text_field("W:", 'w')
        generic_form.add_text_field("L:", 'l')
        generic_form.add_text_field("Vgs:", 'vgs')
        generic_form.add_text_field("Vr:", 'vr')
        generic_form.add_text_field("Vds:", 'vds')
        layout1.add_widget(generic_form)

        btn_calc  = MyButtonBorder(size=(128, 64), size_hint=(None, None), text='Calcular')
        layout1.add_widget(btn_calc)

        grid.add_widget(layout1)
        self.add_widget(grid)



class Principal(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.FrmPrincipal = None

    def build(self):
        self.FrmPrincipal = FrmPrincipal()
        return self.FrmPrincipal

    def on_start(self):
        pass


if __name__ == '__main__':
    Principal().run()
