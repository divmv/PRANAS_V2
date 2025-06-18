# tab2.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class Tab2Content(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Create the label and button
        self.label = Label(text='Press the button', font_size=24)
        self.button = Button(text='Show Lab Name', size_hint=(1, 0.2))

        # Bind the button to the function that updates the label
        self.button.bind(on_press=self.show_lab_name)

        # Add the widgets to the layout
        self.add_widget(self.label)
        self.add_widget(self.button)

    def show_lab_name(self, instance):
        """Update the label to display 'DICE Lab'."""
        self.label.text = 'DICE Lab'
