import os
from math import floor

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Line, Triangle, Point, Color, Rectangle
from kivy.graphics.instructions import Callback
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from functions import text_color
from genericForm import GenericForm
from myButton import MyButtonBorder
from myLayout import MyBoxLayout, MyStackLayout

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

        self.kp = 0
        self.w = 0
        self.l = 0
        self.vgs = 0
        self.vt = 0
        self.vds = 0
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

        layout2 = MyStackLayout()
        layout2.padding = 16
        layout2.spacing = 16
        layout2.borders = ['top', 'right']

        grid_labels = GridLayout(cols=5, size_hint=(1, None))
        self.label_result = Label(text="Ids calc: 0", size_hint=(None, 1))
        self.label_saturacao = Label(text="Saturação: (0, 0)",  size_hint=(None, 1))
        self.label_id = Label(text="Ids: 0",  size_hint=(None, 1))
        self.label_vds = Label(text="Vds: 0", size_hint=(None, 1))
        grid_labels.height = self.label_result.texture_size[1]
        grid_labels.add_widget(self.label_result)
        grid_labels.add_widget(self.label_saturacao)
        grid_labels.add_widget(self.label_id)
        grid_labels.add_widget(self.label_vds)
        self.grid_labels = grid_labels

        self.grafico = BoxLayout()
        self.grafico.size_hint = (1, None)
        layout2.add_widget(grid_labels)
        layout2.add_widget(self.grafico)

        grid.size_hint = (1, None)
        grid.height = generic_form.get_height()
        grid.add_widget(layout1)
        grid.add_widget(layout2)
        self.layout2 = layout2

        self.add_widget(grid)
        layout3 = BoxLayout()
        layout_container = MyBoxLayout()
        layout_container.add_widget(layout3)
        self.add_widget(layout_container)
        self.layout3 = layout3
        btn_calc.bind(on_release=self.btn_calc_on_release)

        self.p0x = 0
        self.p0y = 0
        self.vpx = 0
        self.result_id = 0
        self.canvas.add(Callback(self.update_form))

    def btn_calc_on_release(self, _widget):
        self.kp = float(self.generic_form.ids.kp.text)
        self.w = float(self.generic_form.ids.w.text)
        self.l = float(self.generic_form.ids.l.text)
        self.vgs = float(self.generic_form.ids.vgs.text)
        self.vt = float(self.generic_form.ids.vt.text)
        self.vds = float(self.generic_form.ids.vds.text)

        result = self.calcular_ids(self.vds)
        self.result_id = result
        result = "{:.4e}".format(result)
        self.label_result.text = "Ids calc: " + result
        self.vpx = 0
        self.label_saturacao.text = ("Saturação: (" + "{:.4}".format(self.vgs - self.vt) + ", "
                                + "{:.4e}".format(self.calcular_ids(self.vgs - self.vt)) + ")")
        Clock.unschedule(self.gerar_grafico, all=True)
        Clock.schedule_interval(self.gerar_grafico, 1.0 / 60.0)

    def gerar_grafico(self, _arg):
        intervalo_x = 0.01
        escala_x = 100
        escala_y = 200000
        vds = 0

        if self.vpx < 640 * 1 / (escala_x * intervalo_x):
            self.vpx += 1

        sat = False
        with self.grafico.canvas.after:
            for x in range(0, floor(self.vpx)):
                r_id = self.calcular_ids(vds)
                r_sat = self.calcular_ids(self.vgs - self.vt)
                if vds >= (self.vgs - self.vt):
                    r_id = r_sat
                    if not sat:
                        Color(rgba=[1, 1, 0, 0.8])
                        Point(points=[self.p0x + vds * escala_x, self.p0y + r_id * escala_y], pointsize=6)
                        sat = True

                result = r_id * escala_y
                Color(rgba=text_color)
                Point(points=[self.p0x + vds * escala_x, self.p0y + result])

                if round(vds, 4) == round(self.vds, 4):
                    Color(rgba=[0, 1, 1, 0.8])
                    Point(points=[self.p0x + vds * escala_x, self.p0y + result], pointsize=6)

                vds += intervalo_x

        self.label_id.text = "Ids: " + "{:.4e}".format(r_id)
        self.label_vds.text = "Vds: " + "{:.4}". format(vds)

    def calcular_ids(self, vds):
        kp = self.kp
        w = self.w
        l = self.l
        vgs = self.vgs
        vt = self.vt

        result = kp * (w / l) * ((vgs - vt) - (vds / 2)) * vds
        return result

    def calcular_id(self, vds):
        kp = self.kp
        w = self.w
        l = self.l
        vgs = self.vgs
        vt = self.vt

        result = kp * (w / l) * ((vgs - vt) * vds - 1/2 * vds ** 2)
        return result

    def update_form(self, _instr):
        label_width = self.grid_labels.width // 4
        self.label_result.width = label_width
        self.label_saturacao.width = label_width
        self.label_id.width = label_width
        self.label_vds.width = label_width

        self.layout3.canvas.after.clear()
        print(self.layout3.pos)
        with self.layout3.canvas.after:
            Color(rgb=[1, 1, 1])
            Rectangle(pos=[182, 80], size=[660, 160])
            Color(rgb=[0.66, 0.40, 0.17])
            Rectangle(pos=[184, 82], size=[656, 156])

        self.grafico.canvas.after.clear()
        with self.grafico.canvas.after:
            p0x = self.layout2.pos[0] + 32
            p0y = self.layout2.pos[1] + 32
            self.p0x = p0x
            self.p0y = p0y
            Line(points=[p0x, p0y, p0x, p0y + 340], width=1)
            Line(points=[p0x, p0y, p0x + 640, p0y], width=1)
            Triangle(points=[p0x + 635, p0y - 3, p0x + 635, p0y + 3, p0x + 648, p0y], width=1)
            Triangle(points=[p0x - 3, p0y + 335, p0x + 3, p0y + 335, p0x, p0y + 348], width=1)


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
