# tab3.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class Tab3Content(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text='This is Tab 3', font_size=24))
