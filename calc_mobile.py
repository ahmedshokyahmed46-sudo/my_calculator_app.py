from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class Calculator(App):

    def build(self):
        layout = GridLayout(
            cols=4,
            spacing=5,
            padding=10
        )

        self.display = TextInput(
            text="0",
            readonly=True,
            halign="right",
            font_size=32
        )

        layout.add_widget(self.display)

        buttons = [
            "7", "8", "9", "÷",
            "4", "5", "6", "×",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        ]

        for number in buttons:
            button = Button(
                text=number,
                font_size=25
            )
            button.bind(on_press=self.button_pressed)
            layout.add_widget(button)

        clear = Button(
            text="مسح",
            font_size=25
        )
        clear.bind(on_press=self.clear)
        layout.add_widget(clear)

        return layout

    def button_pressed(self, instance):
        value = instance.text

        if value == "=":
            try:
                expression = self.display.text
                expression = expression.replace("×", "*")
                expression = expression.replace("÷", "/")
                result = eval(expression)
                self.display.text = str(result)
            except:
                self.display.text = "خطأ"

        else:
            if self.display.text == "0":
                self.display.text = value
            else:
                self.display.text += value

    def clear(self, instance):
        self.display.text = "0"


Calculator().run()
