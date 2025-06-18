# tab1.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from DataClasses import DeviceFlags
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.vkeyboard import VKeyboard
from kivy.core.window import Window

# Tab1Content uses ScreenManager to create two screens. (makes ui more user friendly and lowk spaced)
class Tab1Content(BoxLayout):
    def __init__(self, service_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        sm = ScreenManager()
        sm.add_widget(UserInfoScreen(service_manager=service_manager, name='user'))
        sm.add_widget(AnalysisInfoScreen(service_manager=service_manager, name='analysis'))

        self.add_widget(sm)



# Screen 1: User Info
class UserInfoScreen(Screen):
    def __init__(self, service_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.service_manager = service_manager

        self.current_input = None 
        

        self.vkeyboard = VKeyboard()
        self.vkeyboard.layout = 'qwerty'
        self.vkeyboard.size_hint_y = None
        self.vkeyboard.height = Window.height * 0.3
        self.vkeyboard.width = Window.width * 0.6
        self.vkeyboard.bind(on_key_up=self.on_key_up)

        layout = BoxLayout(orientation='vertical', spacing=5, padding=5)

        self.user_name_input = self._create_input(layout, 'User Name:', 'Enter username')
        self.trial_number_input = self._create_input(layout, 'Trial Number:', 'Enter trial number')
        self.port_server_input = self._create_input(layout, 'Port Server:', 'Enter port server')
        self.ip_server_input = self._create_input(layout, 'IP Server:', 'Enter IP server')

        next_button = Button(
            text='Next: Analysis Info',
            font_size=20,
            # size_hint_y=0.5,
            size_hint=(None, None),
            size=(400, 30),
            pos_hint={'center_x': 0.5},  # center it
            color=(1, 1, 1, 1),  # White text color
        )
        next_button.bind(on_press=self.go_to_next)
        layout.add_widget(next_button)

        self.add_widget(layout)

    def _create_input(self, parent, label_text, hint_text):
        box = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        label = Label(text=label_text, size_hint=(0.3, 1))
        input_field = TextInput(hint_text=hint_text, size_hint=(0.7, 1), keyboard_mode='auto')
        input_field.bind(focus=self.on_focus)
        box.add_widget(label)
        box.add_widget(input_field)
        parent.add_widget(box)
        return input_field
        

    def on_focus(self, instance, value):
        if value:
            # Unfocus all other text inputs
            for child in self.walk(restrict=True):
                if isinstance(child, TextInput) and child != instance:
                    child.focus = False

            self.current_input = instance  # Track current input
            if self.vkeyboard.parent is None:
                self.add_widget(self.vkeyboard)
        else:
            # Remove keyboard only if no other TextInput is focused
            if not any(child.focus for child in self.walk(restrict=True) if isinstance(child, TextInput)):
                if self.vkeyboard.parent:
                    self.remove_widget(self.vkeyboard)

    def on_key_up(self, keyboard, keycode, *args):
        key = keycode
        if not self.current_input:
            return
        if key == 'backspace':
            self.current_input.do_backspace()
        elif key == 'enter':
            self.current_input.focus = False
        elif key == 'spacebar':
            self.current_input.insert_text(' ')
        elif key == 'escape':
            self.current_input.focus = False
            if self.vkeyboard.parent:
                self.remove_widget(self.vkeyboard)
        else:
            self.current_input.insert_text(key)

    # when the next button is pressed, the data entered is updated to the trial parameter variables
    def go_to_next(self, instance):
        if self.service_manager:
            self.service_manager.trialParameters.USER = self.user_name_input.text
            self.service_manager.trialParameters.TRIAL = int(self.trial_number_input.text) if self.trial_number_input.text.isdigit() else 0
            self.service_manager.trialParameters.PORT_Server = int(self.port_server_input.text) if self.port_server_input.text.isdigit() else 0
            self.service_manager.trialParameters.IP_Server = self.ip_server_input.text

        self.manager.current = 'analysis'


# Screen 2: Analysis Info
class AnalysisInfoScreen(Screen):
    def __init__(self, service_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.service_manager = service_manager

        self.current_input = None 

        self.vkeyboard = VKeyboard()
        self.vkeyboard.layout = 'qwerty'
        self.vkeyboard.size_hint_y = None
        self.vkeyboard.height = Window.height * 0.3
        self.vkeyboard.width = Window.width * 0.6
        self.vkeyboard.bind(on_key_up=self.on_key_up)

        layout = BoxLayout(orientation='vertical', spacing=3, padding=5)

        self.bacteria_name_input = self._create_input(layout, 'Bacteria Name:', 'Enter bacteria name')
        self.sampling_rate_input = self._create_input(layout, 'Sampling Rate:', 'Enter sampling rate')
        self.buffer_size_input = self._create_input(layout, 'Buffer Size:', 'Enter buffer size')
        self.record_duration_input = self._create_input(layout, 'Record Duration:', 'Enter record duration')
        
        layout.add_widget(Label(text='Analysis Type:', size_hint_y=None, height=30, font_size=14))

        radio_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), height=20, spacing=5, padding=[20, 0])
        self.option1 = CheckBox(group='analysis')
        self.option2 = CheckBox(group='analysis')
        self.option3 = CheckBox(group='analysis')

        radio_box.add_widget(Label(text='BreathEmulate', font_size=14))
        radio_box.add_widget(self.option1)
        radio_box.add_widget(Label(text='Static', font_size=14))
        radio_box.add_widget(self.option2)
        radio_box.add_widget(Label(text='Combined', font_size=14))
        radio_box.add_widget(self.option3)
        layout.add_widget(radio_box)
        

        buttons = BoxLayout(size_hint=(1, 0.2), height=40, spacing=5)

        
        start = Button(
            text='START',
            font_size=18,
            size_hint_y=0.4,
            color=(0, 0, 0, 1),  # Black text color
            background_color=(0, 1, 0, 1),  # Green background color
            background_normal=""  # Remove default background image
        )

        pause = Button(
            text='PAUSE',
            font_size=18,
            size_hint_y=0.4,
            color=(0, 0, 0, 1),  # Black text color
            background_color=(1, 0.65, 0, 1),  # Orange background color
            background_normal=""  # Remove default background image
        )

        stop = Button(
            text='STOP',
            font_size=18,
            size_hint_y=0.4,
            color=(0, 0, 0, 1),  # Black text color
            background_color=(1, 0, 0, 1),  # Red background color
            background_normal=""  # Remove default background image
        )

        start.bind(on_press=self.start_action)
        stop.bind(on_press=self.stop_action)

        buttons.add_widget(start)
        buttons.add_widget(pause)
        buttons.add_widget(stop)

        layout.add_widget(buttons)

        
        back = Button(
            text='Back to User Info',
            font_size=20,
            size_hint=(None, None),
            size=(400, 30),
            pos_hint={'center_x': 0.5},  # center it
            color=(1, 1, 1, 1),  # White text color
        )
        
        back.bind(on_press=self.go_to_user_screen)  # bind to method
        layout.add_widget(back)

        self.add_widget(layout)
        
    def go_to_user_screen(self, instance):
        self.manager.current = 'user'


    def _create_input(self, parent, label_text, hint_text):
        box = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), height=50, spacing=5)
        label = Label(text=label_text, size_hint=(0.3, 1))
        input_field = TextInput(hint_text=hint_text, size_hint=(0.7, 1), font_size=12, padding=[2,2], background_color=(1,1,1,1), keyboard_mode='auto')
        input_field.bind(focus=self.on_focus)
        box.add_widget(label)
        box.add_widget(input_field)
        parent.add_widget(box)
        return input_field
        
    def on_focus(self, instance, value):
        if value:
            # Unfocus all other text inputs
            for child in self.walk(restrict=True):
                if isinstance(child, TextInput) and child != instance:
                    child.focus = False

            self.current_input = instance  # Track current input
            if self.vkeyboard.parent is None:
                self.add_widget(self.vkeyboard)
        else:
            # Remove keyboard only if no other TextInput is focused
            if not any(child.focus for child in self.walk(restrict=True) if isinstance(child, TextInput)):
                if self.vkeyboard.parent:
                    self.remove_widget(self.vkeyboard)

    def on_key_up(self, keyboard, keycode, *args):
        key = keycode
        if not self.current_input:
            return
        if key == 'backspace':
            self.current_input.do_backspace()
        elif key == 'enter':
            self.current_input.focus = False
        elif key == 'spacebar':
            self.current_input.insert_text(' ')
        elif key == 'escape':
            self.current_input.focus = False
            if self.vkeyboard.parent:
                self.remove_widget(self.vkeyboard)
        else:
            self.current_input.insert_text(key)


    # when the start button is pressed, the rest of the data entered is updated to the trial parameter variables
    def start_action(self, instance):
        if self.service_manager:
            self.service_manager.trialParameters.SAMPLING_RATE = int(self.sampling_rate_input.text) if self.sampling_rate_input.text.isdigit() else 0
            self.service_manager.trialParameters.BUFFER_SIZE = int(self.buffer_size_input.text) if self.buffer_size_input.text.isdigit() else 0
            self.service_manager.trialParameters.RECORD_DURATION = int(self.record_duration_input.text) if self.record_duration_input.text.isdigit() else 0
            self.service_manager.trialParameters.UID = self.bacteria_name_input.text

            if self.option1.active:
                self.service_manager.trialParameters.MODE = 'BreathEmulate'
            elif self.option2.active:
                self.service_manager.trialParameters.MODE = 'Static'
            elif self.option3.active:
                self.service_manager.trialParameters.MODE = 'Combined'

            self.service_manager.deviceFlags.CONFIGURE_FLAG = True
            self.service_manager.deviceFlags.START_FLAG = True

    def stop_action(self, instance):
        if self.service_manager:
            self.service_manager.deviceFlags.START_FLAG = False
            self.service_manager.deviceFlags.STOP_FLAG = True



'''
class Tab1Content(BoxLayout):
    def __init__(self,service_manager=None, **kwargs):
            
        super().__init__(**kwargs)
        self.service_manager = service_manager
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10
        

        # Create input box for "User Name"
        self.add_widget(self.create_labeled_input('User Name:', 'Enter username'))

        # Create input box for "Enter Bacteria Name"
        self.add_widget(self.create_labeled_input('Bacteria Name:', 'Enter bacteria name'))

        # Create input box for "Trial Number"
        self.add_widget(self.create_labeled_input('Trial Number:', 'Enter trial number'))
        
        # Create input box for "Sampling Rate"
        self.add_widget(self.create_labeled_input('Sampling Rate:', 'Enter sampling rate'))
        
        # Create input box for "Buffer Size"
        self.add_widget(self.create_labeled_input('Buffer Size:', 'Enter buffer size'))
        
        # Create input box for "Record Duration"
        self.add_widget(self.create_labeled_input('Record Duration:', 'Enter record duration'))
        
        # Create input box for "Port Server"
        self.add_widget(self.create_labeled_input('Port Server:', 'Enter port server'))
        
        # Create input box for "IP Server"
        self.add_widget(self.create_labeled_input('IP Server:', 'Enter IP server'))
        
        # Create the Analysis Type label and radio buttons
        self.add_widget(Label(text='Analysis Type:', size_hint=(1, 0.1), font_size=18))

        # Create a horizontal layout for the radio buttons
        radio_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))

        self.option1 = CheckBox(group='radio', size_hint=(None, 1), width=50)
        self.option2 = CheckBox(group='radio', size_hint=(None, 1), width=50)
        self.option3 = CheckBox(group='radio', size_hint=(None, 1), width=50)

        # Add radio buttons with their labels
        radio_layout.add_widget(Label(text='BreathEmulate'))
        radio_layout.add_widget(self.option1)
        radio_layout.add_widget(Label(text='Option 2'))
        radio_layout.add_widget(self.option2)
        radio_layout.add_widget(Label(text='Option 3'))
        radio_layout.add_widget(self.option3)

        # Add the radio layout to the main layout
        self.add_widget(radio_layout)

        # Create the control buttons: Start, Pause, Stop
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=10)

        start_button = Button(
            text='START',
            font_size=20,
            size_hint_y=0.5,
            color=(0, 0, 0, 1),  # Black text color
            background_color=(0, 1, 0, 1),  # Green background color
            background_normal=""  # Remove default background image
        )

        pause_button = Button(
            text='PAUSE',
            font_size=20,
            size_hint_y=0.5,
            color=(0, 0, 0, 1),  # Black text color
            background_color=(1, 0.65, 0, 1),  # Orange background color
            background_normal=""  # Remove default background image
        )

        stop_button = Button(
            text='STOP',
            font_size=20,
            size_hint_y=0.5,
            color=(0, 0, 0, 1),  # Black text color
            background_color=(1, 0, 0, 1),  # Red background color
            background_normal=""  # Remove default background image
        )

        # Bind the Start button to the start function
        start_button.bind(on_press=self.start_action)
        
        # Bind the Start button to the stop function
        stop_button.bind(on_press=self.stop_action)

        # Add buttons to the layout
        button_layout.add_widget(start_button)
        button_layout.add_widget(pause_button)
        button_layout.add_widget(stop_button)

        # Add the button layout to the main layout
        self.add_widget(button_layout)

    def user_screen(self):
        for i in range(2):
                screen = Screen(name='Title %d' % i)
                sm.add_widget(screen)
        sm.current = "Title 2"
    
    def create_labeled_input(self, label_text, hint_text):
        """Create a horizontal layout with a label and input box."""
        layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        label = Label(text=label_text, size_hint=(0.3, 1))
        text_input = TextInput(hint_text=hint_text, size_hint=(0.7, 1))
        setattr(self, f'{label_text.lower().replace(" ", "_").replace(":", "")}_input', text_input)  # Store input reference
        layout.add_widget(label)
        layout.add_widget(text_input)
        return layout

    def start_action(self, instance):
        """Print the entered details to the console when Start is clicked."""
        print("clicked start action")
        
        
        user_name = self.user_name_input.text.strip()
        bacteria_name = self.bacteria_name_input.text.strip()
        trial_number = self.trial_number_input.text.strip()
        sampling_rate = self.sampling_rate_input.text.strip()
        buffer_size = self.buffer_size_input.text.strip()
        record_duration = self.record_duration_input.text.strip()
        port_server = self.port_server_input.text.strip()
        ip_server = self.ip_server_input.text.strip()
        
        # Determine which radio button is selected
        if self.option1.active:
            radio_value = "BreathEmulate"
        elif self.option2.active:
            radio_value = 'Option 2'
        elif self.option3.active:
            radio_value = 'Option 3'
        else:
            radio_value = 'No option selected'
            
        self.service_manager.trialParameters.USER = user_name
        self.service_manager.trialParameters.UID = bacteria_name
        self.service_manager.trialParameters.TRIAL = int(trial_number) if trial_number.isdigit() else 0
        self.service_manager.trialParameters.SAMPLING_RATE = int(sampling_rate) if sampling_rate.isdigit() else 0
        self.service_manager.trialParameters.BUFFER_SIZE = int(buffer_size) if buffer_size.isdigit() else 0
        self.service_manager.trialParameters.RECORD_DURATION = int(record_duration) if record_duration.isdigit() else 0
        self.service_manager.trialParameters.PORT_Server = int(port_server) if port_server.isdigit() else 0
        self.service_manager.trialParameters.IP_Server = ip_server
        self.service_manager.trialParameters.MODE = radio_value

        # Set the START_FLAG
        self.service_manager.deviceFlags.CONFIGURE_FLAG = True
        self.service_manager.deviceFlags.START_FLAG = True
        
        # print(f"[START] User: {user_name}, UID: {bacteria_name}, Trial: {trial_number}, Mode: {radio_value}, Sampling Rate: {sampling_rate}")

    def stop_action(self, instance):
        """Print the entered details to the console when Stop is clicked."""
        print("clicked stop action")
        # Set the STOP_FLAG
        self.service_manager.deviceFlags.STOP_FLAG = True
'''

