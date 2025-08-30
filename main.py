import os
from math import floor

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Line, Triangle, Point, Color, Rectangle, Ellipse, Quad, Translate
from kivy.graphics.instructions import Callback
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from sympy import diff, symbols

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


class FrmPrincipal(MyBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.saturacao = 0
        self.kn = 0
        self.w = 0
        self.l = 0
        self.vgs = 0
        self.vt = 0
        self.vds = 0
        self.lb = 0
        self.orientation = 'vertical'

        grid = GridLayout(cols=2)
        layout1 = MyBoxLayout(size_hint=(None, 1), orientation='vertical')
        layout1.width = 300
        layout1.borders = ['left', 'top', 'right']
        self.generic_form = GenericForm()
        generic_form = self.generic_form
        generic_form.add_text_field("k'n:", 'kn')
        generic_form.add_text_field("W:", 'w')
        generic_form.add_text_field("L:", 'l')
        generic_form.add_text_field("Vgs:", 'vgs')
        generic_form.add_text_field("Vt:", 'vt')
        generic_form.add_text_field("Vds:", 'vds')
        generic_form.add_text_field("Lambda:", 'lb')

        # Valores apresentados na primeira aula
        generic_form.ids.kn.text = '340e-6'
        generic_form.ids.w.text = '2e-6'
        generic_form.ids.l.text = '1e-6'
        generic_form.ids.vgs.text = '3'
        generic_form.ids.vt.text = '1'
        generic_form.ids.vds.text = '0.5'

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
        self.label_result = Label(text="Ids calc.: 0", size_hint=(None, 1), color=[0, 1, 1, 1])
        self.label_saturacao = Label(text="Saturação: (0, 0)", size_hint=(None, 1), color=[1, 1, 0, 1])
        self.label_id = Label(text="Ids: 0", size_hint=(None, 1))
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

        self.label_derivada = Label(text="----", size_hint=(None, 1), color=[1, 1, 1, 1])
        layout4 = AnchorLayout(size_hint=(1, None))
        layout4.height = 24
        layout4.add_widget(self.label_derivada)
        self.layout4 = layout4

        layout_container = MyBoxLayout(orientation='vertical')
        layout_container.add_widget(layout3)
        layout_container.add_widget(layout4)
        self.add_widget(layout_container)
        self.layout3 = layout3
        btn_calc.bind(on_release=self.btn_calc_on_release)

        self.p0x = 0
        self.p0y = 0
        self.vpx = 0
        self.result_id = 0
        self.canvas.add(Callback(self.update_form))

    def btn_calc_on_release(self, _widget):
        try:
            self.kn = float(self.generic_form.ids.kn.text)
            self.w = float(self.generic_form.ids.w.text)
            self.l = float(self.generic_form.ids.l.text)
            self.vgs = float(self.generic_form.ids.vgs.text)
            self.vt = float(self.generic_form.ids.vt.text)
            self.vds = float(self.generic_form.ids.vds.text)
            if self.generic_form.ids.lb.text.strip():
                self.lb = float(self.generic_form.ids.lb.text)
        except ValueError:
            self.kn = 0
            self.w = 0
            self.l = 0
            self.vt = 0
            self.vgs = 0

        result = self.calcular_ids(self.vds)
        self.result_id = result
        result = "{:.4e}".format(result)
        self.label_result.text = "Ids calc.: " + result
        self.vpx = 0

        if self.vgs < self.vt:  # evita tensão negativa, região de cut-off
            self.vgs = self.vt

        self.saturacao = self.calcular_ids(self.vgs - self.vt)
        self.label_saturacao.text = ("Saturação: (" + "{:.4}".format(self.vgs - self.vt) + ", "
                                     + "{:.4e}".format(self.saturacao) + ")")
        Clock.unschedule(self.gerar_grafico, all=True)
        Clock.schedule_interval(self.gerar_grafico, 1.0 / 60.0)

    def gerar_grafico(self, _arg):
        intervalo_x = 0.01
        escala_x = 200
        escala_y = 200000
        vds = 0

        px_max = self.grafico.width - 64

        if self.vpx < px_max / (escala_x * intervalo_x):
            self.vpx += 1

        sat = False
        with self.grafico.canvas.after:
            for x in range(0, floor(self.vpx)):
                r_id = self.calcular_ids(vds)
                if vds >= (self.vgs - self.vt):
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
        self.label_vds.text = "Vds: " + "{:.4}".format(vds)
        self.calcular_derivada(vds)

        if self.vgs > self.vt:
            with self.layout3.canvas.after:
                # canal n
                tx = Window.width // 2 - 1024 // 2
                ty = Window.height // 2 - 836 // 2
                Translate(tx, ty)

                # While the depth of drain end is proportional to (Vov – Vds).
                # Seadra,  Microeletronic Circuits 6th edition, Figure 5.6
                #
                # Será inversamente propocional já que o eixo y é invertido no layout 3 (self.layout3).
                vo = self.vgs - self.vt
                if (vo - vds) > 0:
                    tamanho_borda = 188 + 50 * (vds / vo)
                    tamanho_canal = 638
                else:
                    tamanho_borda = 238
                    tamanho_canal = 338 + 300 * (self.saturacao / r_id)

                Line(points=(386, 188, tamanho_canal, tamanho_borda))
                Color(rgb=[0.4, 0.4, 0.4])
                Quad(points=(387, 238, 637, 238, tamanho_canal - 1, tamanho_borda, 387, 189))
                Translate(-tx, -ty)

    def calcular_ids(self, vds):
        kn = self.kn
        w = self.w
        l = self.l
        vt = self.vt
        vgs = self.vgs
        lb = self.lb

        if vds < 0:
            vds = 0

        if vds < (vgs - vt):
            # ** potenciação em python
            # kn * (w / l) * ((vgs - vt) - (vds / 2)) * vds
            # kn * (w / l) * ((vgs - vt) * vds - 1/2 * vds) * vds
            result = kn * (w / l) * ((vgs - vt) * vds - 1 / 2 * vds ** 2) * (1 + lb * vds)
        else:
            # kn * (w / l) * ((vgs - vt) ** 2 - 1 / 2 * (vgs - vt) ** 2
            result = kn * (w / l) * 1 / 2 * (vgs - vt) ** 2 * (1 + lb * vds)

        if result < 0:
            result = 0
        return result

    def calcular_derivada(self, pvds):
        kn = self.kn
        w = self.w
        l = self.l

        vds, vt, vgs, lb = symbols('vds vt vgs lb')
        if pvds < (self.vgs - self.vt):
            ids = kn * (w / l) * ((vgs - vt) * vds - 1 / 2 * vds ** 2) * (1 + lb * vds)
        else:
            ids = kn * (w / l) * 1 / 2 * (vgs - vt) ** 2 * (1 + lb * vds)

        result = ids
        self.label_derivada.text = str(result)

    def update_form(self, _instr):
        label_width = self.grid_labels.width // 4
        for c in self.grid_labels.children:
            if isinstance(c, Label):
                c.width = label_width

        self.label_derivada.height = self.label_derivada.texture_size[1]

        self.layout3.canvas.after.clear()
        with self.layout3.canvas.after:
            tx = Window.width // 2 - 1024 // 2
            ty = Window.height // 2 - 836 // 2
            Translate(tx, ty)

            Color(rgb=[1, 1, 1])
            Rectangle(pos=[182, 80], size=[660, 160])
            Color(rgb=[0.66, 0.40, 0.17])
            Rectangle(pos=[184, 82], size=[656, 156])

            # borda n1
            Color(rgb=[1, 1, 1])
            Line(points=(204, 238, 204, 188), width=2)
            Line(circle=(224, 188, 20, 270, 180), width=2)
            Line(points=(224, 168, 364, 168), width=2)
            Line(circle=(364, 188, 20, 180, 90), width=2)
            Line(points=(384, 188, 384, 238), width=2)

            # preenchimento n1
            offset_x = 436
            Color(rgb=[0.7, 0.7, 0.7])
            Rectangle(pos=[205, 190], size=[178, 48])
            Ellipse(pos=[205, 170], size=[40, 40])
            Rectangle(pos=[226, 170], size=[137, 40])
            Ellipse(pos=[343, 170], size=[40, 40])
            Color(rgb=[1, 1, 1])
            Rectangle(pos=[244, 239], size=[94, 16])
            Rectangle(pos=[278, 192], size=[32, 32], source="images/nmais.png")

            # borda n2
            Color(rgb=[1, 1, 1])
            Line(points=(204 + offset_x, 238, 204 + offset_x, 188), width=2)
            Line(circle=(224 + offset_x, 188, 20, 270, 180), width=2)
            Line(points=(224 + offset_x, 168, 364 + offset_x, 168), width=2)
            Line(circle=(364 + offset_x, 188, 20, 180, 90), width=2)
            Line(points=(384 + offset_x, 188, 384 + offset_x, 238), width=2)

            # preenchimento n2
            offset_x = 436
            Color(rgb=[0.7, 0.7, 0.7])
            Rectangle(pos=[205 + offset_x, 190], size=[178, 48])
            Ellipse(pos=[205 + offset_x, 170], size=[40, 40])
            Rectangle(pos=[226 + offset_x, 170], size=[137, 40])
            Ellipse(pos=[343 + offset_x, 170], size=[40, 40])
            Color(rgb=[1, 1, 1])
            Rectangle(pos=[244 + offset_x, 239], size=[94, 16])
            Rectangle(pos=[278 + offset_x, 192], size=[32, 32], source="images/nmais.png")

            # parte superior
            Line(points=(360, 240, 360, 268), width=2)
            Line(points=(360, 268, 660, 268), width=2)
            Line(points=(660, 268, 660, 240), width=2)
            Rectangle(pos=[362, 254], size=[300, 12])
            for i in range(12):
                Line(points=(374 + 24 * i, 240, 388 + 24 * i, 256), width=1.4)

            # parte inferior
            Rectangle(pos=[436, 68], size=[152, 12])

            # terminais
            Line(points=(290, 256, 290, 276), width=2)
            Line(circle=(290, 283, 4), width=1.4)
            Line(points=(290, 287, 290, 307), width=2)
            Rectangle(pos=[294, 264], size=[32, 32], source="images/s.png")

            Line(points=(511, 272, 511, 292), width=2)
            Line(circle=(511, 299, 4), width=1.4)
            Line(points=(511, 305, 511, 325), width=2)
            Rectangle(pos=[515, 283], size=[32, 32], source="images/g.png")

            Line(points=(290 + offset_x, 256, 290 + offset_x, 276), width=2)
            Line(circle=(290 + offset_x, 283, 4), width=1.4)
            Line(points=(290 + offset_x, 287, 290 + offset_x, 307), width=2)
            Rectangle(pos=[294 + offset_x, 264], size=[32, 32], source="images/d.png")

            Line(points=(511, 67, 511, 47), width=2)
            Line(circle=(511, 40, 4), width=1.4)
            Line(points=(511, 36, 511, 16), width=2)
            Rectangle(pos=[515, 20], size=[32, 32], source="images/b.png")

            Translate(-tx, -ty)

        self.grafico.canvas.after.clear()
        with self.grafico.canvas.after:
            p0x = self.layout2.pos[0] + 32
            p0y = self.layout2.pos[1] + 32

            px_max = self.layout2.pos[0] + self.layout2.width - 64
            py_max = self.layout2.pos[1] + self.layout2.height - 64

            self.p0x = p0x
            self.p0y = p0y
            Line(points=[p0x, p0y, p0x, py_max], width=1)
            Line(points=[p0x, p0y, px_max, p0y], width=1)
            Triangle(points=[px_max, p0y - 3, px_max, p0y + 3, px_max + 10, p0y], width=1)
            Triangle(points=[p0x - 3, py_max, p0x + 3, py_max, p0x, py_max + 10], width=1)
            Rectangle(pos=(p0x - 30, py_max - 32), size=[28, 28], source="images/id.png")
            Rectangle(pos=(px_max - 32, p0y - 30), size=[28, 28], source="images/vds.png")


class Principal(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.FrmPrincipal = None

    def build(self):
        self.FrmPrincipal = FrmPrincipal()
        return self.FrmPrincipal

    def on_start(self):
        # Window.size = (1152, 864)
        Window.borderless = True
        Window.fullscreen = True


if __name__ == '__main__':
    Principal().run()
