from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Ellipse
from kivy.metrics import dp
from kivy.core.window import Window


Window.clearcolor = (0, 0, 0, 1)


class CircleButton(Button):

    def __init__(self, button_color=(0.08, 0.08, 0.09, 1),
                 text_color=(1, 1, 1, 1), **kwargs):

        super().__init__(**kwargs)

        self.button_color = button_color
        self.text_color = text_color

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)

        self.color = text_color
        self.font_size = dp(30)

        with self.canvas.before:
            self.circle_color = Color(*self.button_color)
            self.circle = Ellipse()

        self.bind(pos=self.update_circle)
        self.bind(size=self.update_circle)
        self.bind(state=self.update_color)

    def update_circle(self, *args):

        size = min(self.width, self.height)

        self.circle.size = (size, size)

        self.circle.pos = (
            self.center_x - size / 2,
            self.center_y - size / 2
        )

    def update_color(self, *args):

        if self.state == "down":
            self.circle_color.rgba = (
                min(self.button_color[0] + 0.12, 1),
                min(self.button_color[1] + 0.12, 1),
                min(self.button_color[2] + 0.12, 1),
                1
            )
        else:
            self.circle_color.rgba = self.button_color


class Calculator(App):

    def build(self):

        root = BoxLayout(
            orientation="vertical",
            padding=[dp(18), dp(15), dp(18), dp(15)],
            spacing=dp(8)
        )

        # =========================
        # الشريط العلوي
        # =========================

        top = BoxLayout(
            size_hint_y=None,
            height=dp(45),
            spacing=dp(10)
        )

        history = Label(
            text="◷",
            font_size=dp(30),
            color=(0.8, 0.8, 0.8, 1)
        )

        top.add_widget(history)

        top.add_widget(Label())

        ruler = Label(
            text="▱",
            font_size=dp(30),
            color=(0.8, 0.8, 0.8, 1)
        )

        check = Label(
            text="☑",
            font_size=dp(29),
            color=(0.8, 0.8, 0.8, 1)
        )

        top.add_widget(ruler)
        top.add_widget(check)

        root.add_widget(top)

        # =========================
        # شاشة الحاسبة
        # =========================

        self.display = TextInput(
            text="",
            readonly=True,
            multiline=False,
            halign="right",
            font_size=dp(42),
            background_color=(0, 0, 0, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0, 0, 0, 0),
            padding=[dp(10), dp(10)],
            size_hint_y=0.38
        )

        root.add_widget(self.display)

        # =========================
        # الأزرار
        # =========================

        buttons_grid = GridLayout(
            cols=4,
            rows=5,
            spacing=dp(8),
            size_hint_y=0.62
        )

        buttons = [
            ("C", "clear"),
            ("⌫", "delete"),
            ("%", "operator"),
            ("÷", "operator"),

            ("7", "number"),
            ("8", "number"),
            ("9", "number"),
            ("×", "operator"),

            ("4", "number"),
            ("5", "number"),
            ("6", "number"),
            ("−", "operator"),

            ("1", "number"),
            ("2", "number"),
            ("3", "number"),
            ("+", "operator"),

            ("()", "number"),
            ("0", "number"),
            (".", "number"),
            ("=", "equal")
        ]

        for text, kind in buttons:

            if kind == "clear":
                bg = (0.09, 0.09, 0.10, 1)
                fg = (1, 0.35, 0.38, 1)

            elif kind == "delete":
                bg = (0.09, 0.09, 0.10, 1)
                fg = (1, 0.35, 0.38, 1)

            elif kind == "operator":
                bg = (0.14, 0.14, 0.15, 1)
                fg = (1, 1, 1, 1)

            elif kind == "equal":
                bg = (0.04, 0.55, 0.48, 1)
                fg = (1, 1, 1, 1)

            else:
                bg = (0.08, 0.08, 0.09, 1)
                fg = (1, 1, 1, 1)

            button = CircleButton(
                text=text,
                button_color=bg,
                text_color=fg
            )

            if text in ["C", "⌫"]:
                button.font_size = dp(28)

            elif text in ["÷", "×", "−", "+"]:
                button.font_size = dp(32)

            elif text == "=":
                button.font_size = dp(32)

            else:
                button.font_size = dp(30)

            button.bind(on_release=self.button_pressed)

            buttons_grid.add_widget(button)

        root.add_widget(buttons_grid)

        return root

    # =========================
    # التعامل مع الأزرار
    # =========================

    def button_pressed(self, button):

        value = button.text

        # مسح
        if value == "C":
            self.display.text = ""

        # حذف
        elif value == "⌫":
            self.display.text = self.display.text[:-1]

        # نسبة
        elif value == "%":

            try:
                number = float(self.display.text)
                result = number / 100

                if result.is_integer():
                    result = int(result)

                self.display.text = str(result)

            except:
                self.display.text = "Error"

        # يساوي
        elif value == "=":
            self.calculate()

        # أقواس
        elif value == "()":

            if self.display.text == "":
                self.display.text = "("

            elif self.display.text.count("(") > self.display.text.count(")"):
                self.display.text += ")"

            else:
                self.display.text += "("

        # العمليات
        elif value in ["+", "−", "×", "÷"]:

            if self.display.text == "":
                return

            self.display.text += value

        # الأرقام
        else:

            self.display.text += value

    # =========================
    # الحساب
    # =========================

    def calculate(self):

        try:

            expression = self.display.text

            expression = expression.replace("×", "*")
            expression = expression.replace("÷", "/")
            expression = expression.replace("−", "-")

            result = eval(
                expression,
                {"__builtins__": None},
                {}
            )

            if isinstance(result, float) and result.is_integer():
                result = int(result)

            self.display.text = str(result)

        except:

            self.display.text = "Error"


Calculator().run()
