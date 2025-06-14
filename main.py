# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
import threading
import time
from kivy.clock import Clock
import winsound
from morse import morse_to_text
from morse import text_to_morse
from morse import text_to_morse, morse_to_text  # Now includes morse_to_text

Window.size = (400, 600)  # Optional: Set window size for desktop


class FlashWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.color = Color(1, 1, 1, 1)  # Default white
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def flash(self, r, g, b, duration):
        def do_flash(*args):
            self.color.rgb = (r, g, b)
            self.canvas.ask_update()
            Clock.schedule_once(reset_flash, duration)

        def reset_flash(*args):
            self.color.rgb = (1, 1, 1)
            self.canvas.ask_update()

        Clock.schedule_once(do_flash)


class MorseBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 20

        # Flash area
        self.flash_area = FlashWidget(size_hint=(1, 1))
        self.add_widget(self.flash_area)

        self.clear_widgets()  # optional if widgets are being reset

        # Add full-screen flash first so it covers everything
        self.add_widget(self.flash_area)

        # Input box
        self.input = TextInput(
            hint_text="Enter message...",
            font_size=24,
            multiline=False,
            size_hint=(1, 0.15)
        )

        # Morse output label
        self.output = Label(
            text="Morse Code will appear here",
            font_size=20,
            size_hint=(1, 0.2)
        )

        # Send button
        self.send_button = Button(
            text="Send as Morse",
            font_size=24,
            size_hint=(1, 0.15)
        )
        self.send_button.bind(on_press=self.send_morse)

        

        # --- RECEIVER SECTION ---
        self.receiver_label = Label(
            text="Receiver (Tap Morse Input):",
            font_size=22,
            size_hint=(1, 0.1)
        )
        self.receiver_input = TextInput(
            hint_text="Your Morse: . - . / ...",
            font_size=20,
            multiline=False,
            size_hint=(1, 0.1)
        )

        self.receiver_output = Label(
            text="Decoded message will appear here.",
            font_size=20,
            size_hint=(1, 0.15)
        )

        receiver_controls = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=10)
        dot_btn = Button(text="Dot (.)", on_press=lambda x: self.append_morse('.'))
        dash_btn = Button(text="Dash (-)", on_press=lambda x: self.append_morse('-'))
        space_btn = Button(text="Space", on_press=lambda x: self.append_morse(' '))
        slash_btn = Button(text="Slash (/)", on_press=lambda x: self.append_morse('/'))

        receiver_controls.add_widget(dot_btn)
        receiver_controls.add_widget(dash_btn)
        receiver_controls.add_widget(space_btn)
        receiver_controls.add_widget(slash_btn)

        translate_btn = Button(
            text="Translate Morse to Text",
            font_size=20,
            size_hint=(1, 0.1)
        )
        translate_btn.bind(on_press=self.translate_morse)

        # Add widgets
        self.add_widget(self.receiver_label)
        self.add_widget(self.receiver_input)
        self.add_widget(receiver_controls)
        self.add_widget(translate_btn)
        self.add_widget(self.receiver_output)

        # Add widgets
        self.add_widget(self.input)
        self.add_widget(self.output)
        self.add_widget(self.send_button)

    def append_morse(self, symbol):
        self.receiver_input.text += symbol

    def translate_morse(self, instance):
        code = self.receiver_input.text.strip()
        if not code:
            self.receiver_output.text = "Enter Morse to decode."
            return
        try:
            message = morse_to_text(code)
            self.receiver_output.text = f"Decoded: {message}"
        except:
            self.receiver_output.text = "Invalid Morse input."

    def send_morse(self, instance):
        message = self.input.text.strip()
        if not message:
            self.output.text = "Please enter a message."
            return
        morse_code = text_to_morse(message)
        self.output.text = f"Morse: {morse_code}"
        threading.Thread(target=self.play_morse_beep, args=(morse_code,), daemon=True).start()

    def play_morse_beep(self, code):
        for symbol in code:
            if symbol == '.':
                Clock.schedule_once(lambda dt: self.flash_area.flash(1, 1, 1, 0.2))  # White for dot
                winsound.Beep(1000, 200)
            elif symbol == '-':
                Clock.schedule_once(lambda dt: self.flash_area.flash(1, 0, 0, 0.5))  # Red for dash
                winsound.Beep(1000, 500)
            elif symbol == ' ':
                Clock.schedule_once(lambda dt: self.flash_area.flash(0, 1, 0, 0.3))  # Green for space
                time.sleep(0.3)
            elif symbol == '/':
                Clock.schedule_once(lambda dt: self.flash_area.flash(1, 1, 0, 0.7))  # Yellow for slash
                time.sleep(0.7)
            time.sleep(0.2)


class MorseApp(App):
    def build(self):
        return MorseBox()


if __name__ == '__main__':
    MorseApp().run()
