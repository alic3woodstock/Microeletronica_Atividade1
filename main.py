import os

import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from genericForm import GenericForm
from myButton import MyButtonBorder
from myLayout import MyBoxLayout

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
        self.orientation = 'vertical'

        grid = GridLayout(cols=2)
        layout1 = MyBoxLayout(size_hint=(None, 1), orientation='vertical')
        layout1.width = 300
        layout1.borders = ['left', 'top', 'right']
        self.generic_form = GenericForm()
        generic_form = self.generic_form
        generic_form.add_text_field("k'n:", 'kp')
        generic_form.add_text_field("W:", 'w')
        generic_form.add_text_field("L:", 'l')
        generic_form.add_text_field("Vgs:", 'vgs')
        generic_form.add_text_field("Vt:", 'vt')
        generic_form.add_text_field("Vds:", 'vds')

        # Valores apresentados na primeira aula
        generic_form.ids.kp.text = '340e-6'
        generic_form.ids.w.text = '2e-6'
        generic_form.ids.l.text = '1e-6'
        generic_form.ids.vgs.text = '3'
        generic_form.ids.vt.text = '1'
        generic_form.ids.vds.text = '2'

        btn_calc = MyButtonBorder(text='Calcular')
        btn_calc.height = generic_form.children_height
        generic_form.topLayout.add_widget(Label(text=""))
        generic_form.topLayout.add_widget(btn_calc)
        layout1.add_widget(generic_form)

        layout2 = MyBoxLayout()
        layout2.borders = ['top', 'right']

        grid.size_hint = (1, None)
        grid.height = generic_form.get_height()
        grid.add_widget(layout1)
        grid.add_widget(layout2)

        self.add_widget(grid)
        layout2 = MyBoxLayout()
        self.add_widget(layout2)
        btn_calc.bind(on_release=self.btn_calc_on_release)

    def btn_calc_on_release(self, _widget):
        kp = float(self.generic_form.ids.kp.text)
        w = float(self.generic_form.ids.w.text)
        l = float(self.generic_form.ids.l.text)
        vgs = float(self.generic_form.ids.vgs.text)
        vt = float(self.generic_form.ids.vt.text)
        vds = float(self.generic_form.ids.vds.text)

        ids = kp * (w / l) * ((vgs - vt) - (vds / 2)) * vds
        print(f"{ids:e}")


class Principal(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.FrmPrincipal = None

    def build(self):
        self.FrmPrincipal = FrmPrincipal()
        return self.FrmPrincipal

    def on_start(self):
        Window.size = (1024, 768)


if __name__ == '__main__':
    Principal().run()
