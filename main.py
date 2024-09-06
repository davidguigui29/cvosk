from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from vosk import Model, KaldiRecognizer
import json
import pyaudio
import threading

class VoskApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Initializing...")
        self.start_button = Button(text='Start Recognition')
        self.start_button.bind(on_press=self.start_recognition)
        self.stop_button = Button(text="Stop Recognition")
        self.stop_button.bind(on_press=self.stop_recognition)
        self.stop_button.disabled = True  # Initially disabled

        layout.add_widget(self.label)
        layout.add_widget(self.start_button)
        layout.add_widget(self.stop_button)

        return layout

    def start_recognition(self, instance):
        if hasattr(self, 'thread') and self.thread.is_alive():
            print("Recognition already running.")
            return

        self.model = Model("model-en-us")
        self.rec = KaldiRecognizer(self.model, 16000)

        # PyAudio configuration
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )

        self.stop_thread_event = threading.Event()
        self.thread = threading.Thread(target=self.record_and_recognize)
        self.thread.start()

        # Update button states
        self.start_button.disabled = True
        self.stop_button.disabled = False

    def record_and_recognize(self):
        while not self.stop_thread_event.is_set():
            buffer = self.stream.read(1024, exception_on_overflow=False)
            if self.rec.AcceptWaveform(buffer):
                result = json.loads(self.rec.Result())
                print(f"Here is the result: {result}")
                self.update_label(result.get('text', ''))

    def update_label(self, text):
        # Use Clock.schedule_once to update the UI from the main thread
        Clock.schedule_once(lambda dt: setattr(self.label, 'text', text))

    def stop_recognition(self, instance):
        if hasattr(self, 'thread') and self.thread.is_alive():
            self.stop_thread_event.set()
            self.thread.join()
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()

            # Update button states
            self.start_button.disabled = False
            self.stop_button.disabled = True
        else:
            print("Recognition is not running.")

if __name__ == '__main__':
    VoskApp().run()
