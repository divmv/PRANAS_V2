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
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget


import os
from datetime import datetime
import glob 

# Tab1Content uses ScreenManager to create two screens
class Tab1Content(BoxLayout):
    def __init__(self, service_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        sm = ScreenManager()
        sm.add_widget(UserInfoScreen(service_manager=service_manager, name='user'))
        sm.add_widget(AnalysisInfoScreen(service_manager=service_manager, name='analysis'))
        sm.add_widget(OldAnalysisInfoScreen(service_manager=service_manager, name='old_analysis'))
        

        self.add_widget(sm)



# Screen 1: User Info
class UserInfoScreen(Screen):
    def __init__(self, service_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.service_manager = service_manager

        self.current_input = None

        layout = BoxLayout(orientation='vertical', spacing=5, padding=5)
        
        welcome_label = Label(
            text="Choose an option:",
            font_size=20,
            size_hint=(1, 0.15),  # Small space at the top
            halign='center',
            valign='middle'
        )
        layout.add_widget(welcome_label)

        # Middle Spacer + Buttons Centered in Middle
        center_layout = BoxLayout(orientation='vertical', spacing=20, size_hint=(1, 0.7))
        center_layout.add_widget(Label(size_hint=(1, 0.5)))  # Spacer above buttons

        new_button = Button(
            text='Start New Analysis',
            font_size=25,
            size_hint=(None, None),
            size=(400, 60),
            pos_hint={'center_x': 0.5}
        )
        center_layout.add_widget(new_button)

        old_button = Button(
            text='View Old Analysis Info',
            font_size=25,
            size_hint=(None, None),
            size=(400, 60),
            pos_hint={'center_x': 0.5}
        )
        center_layout.add_widget(old_button)

        center_layout.add_widget(Label(size_hint=(1, 0.5)))  # Spacer below buttons

        new_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'analysis'))
        old_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'old_analysis'))

        layout.add_widget(center_layout)

        # Bottom (optional): Leave blank or use for additional info
        layout.add_widget(Label(size_hint=(1, 0.15)))  # Spacer at bottom

        self.add_widget(layout)

# Screen 2: Old Analysis Info
class OldAnalysisInfoScreen(Screen):
    def __init__(self, service_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.service_manager = service_manager

        self.current_input = None 

        self.vkeyboard = VKeyboard()
        self.vkeyboard.layout = 'qwerty'
        self.vkeyboard.size_hint_y = None
        self.vkeyboard.height = Window.height * 0.25
        self.vkeyboard.width = Window.width * 0.6
        self.vkeyboard.bind(on_key_up=self.on_key_up)

        layout = BoxLayout(orientation='vertical', spacing=3, padding=5)

        welcome_label2 = Label(
            text="Rerun Old Analysis",
            font_size=15,
            size_hint=(1, None), 
            height=60,
            halign='center',
            valign='middle'
        )   
        welcome_label2.bind(size=welcome_label2.setter('text_size'))
        layout.add_widget(welcome_label2)

        # layout.add_widget(Widget(size_hint_y=None, height=5)) # small space


        self.user_name_input = self._create_input(layout, 'User Name:', 'Enter username')
        layout.add_widget(Widget(size_hint_y=None, height=15)) # one more small space
        # layout.add_widget(Widget(size_hint_y=None, height=50)) # one more small space

        '''
        self.trial_number_input = self._create_input(layout, 'Trial Number:', 'Enter trial number')
        self.bacteria_name_input = self._create_input(layout, 'Bacteria Name:', 'Enter bacteria name')
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
        '''

        load = Button(
            text='Load Old Parameters',
            font_size=22,
            size_hint=(None, None),
            size=(400, 40),
            pos_hint={'center_x': 0.5},  # center it
            color=(1, 1, 1, 1),  # White text color
        )
        load.bind(on_press=self.load_old_logs)
        layout.add_widget(load)
        
        self.redirect_label = Label(text='Redirecting to Start New Analysis...', 
                            size_hint=(1, None), 
                            height=50,
                            color=(1,1,1,1),
                            bold=True,
                            opacity=0 # initially invisible
        )  

        layout.add_widget(self.redirect_label)
        # layout.add_widget(Widget(size_hint_y=None, height=20)) # one more small space

        back = Button(
            text='Back to User Info',
            font_size=20,
            size_hint=(None, None),
            size=(400, 30),
            pos_hint={'center_x': 0.5},  # center it
            color=(1, 1, 1, 1),  # White text color
        )
        
        back.bind(on_press=self.go_to_user_screen)
        layout.add_widget(back)

        self.add_widget(layout)


    def go_to_user_screen(self, instance):
        self.manager.current = 'user'

    def load_old_logs(self, instance):
        username = self.user_name_input.text.strip()
        if not username:
            print("Username is empty.")
            return

        latest_file = self.find_latest_log_file(username)
        if not latest_file:
            print(f"No logs found for user: {username}")
            return

        print(f"Loading from: {latest_file}")
        if self.load_params(latest_file):  # Fill service_manager.trialParameters
            # Show redirect message
            self.redirect_label.opacity = 1

            # Schedule the actual screen switch after 2 seconds
            from kivy.clock import Clock
            Clock.schedule_once(self._redirect_to_analysis, 2)
        '''
        # Switch to the 'analysis' screen
        self.manager.current = 'analysis'

        # Tell the AnalysisInfoScreen to refresh its fields
        screen = self.manager.get_screen('analysis')
        if hasattr(screen, 'populate_fields_from_params'):
            screen.populate_fields_from_params()
        '''
    def _redirect_to_analysis(self, dt):
        self.redirect_label.opacity = 0
        self.manager.current = 'analysis'
        analysis_screen = self.manager.get_screen('analysis')
        if hasattr(analysis_screen, 'populate_fields_from_params'):
            analysis_screen.populate_fields_from_params()

    def extract_trial_params(self, filepath):
        trial_params = {}
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        trial_params[key.strip()] = value.strip()
        except Exception as e:
            print(f"Error reading log file: {e}")
        return trial_params
    
    def find_latest_log_file(self, username):
        logs_path = os.path.join(os.getcwd(), 'logs')
        pattern = os.path.join(logs_path, f'Log_{username}_*.log')
        log_files = glob.glob(pattern)
        if not log_files:
            return None
        latest_file = max(log_files, key=os.path.getmtime)
        return latest_file

    def load_params(self, filepath):
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    if ':' not in line:
                        continue
                    key, value = line.strip().split(':', 1)
                    key = key.strip().upper()
                    value = value.strip()

                    if key == 'USER':
                        self.service_manager.trialParameters.USER = value
                    elif key == 'TRIAL':
                        self.service_manager.trialParameters.TRIAL = int(value)
                    elif key == 'UID':
                        self.service_manager.trialParameters.UID = value
                    elif key in ['DURATION', 'RECORD_DURATION']:
                        self.service_manager.trialParameters.RECORD_DURATION = int(value.split()[0])  # e.g., "5 seconds"
                    elif key == 'MODE':
                        self.service_manager.trialParameters.MODE = value
            return True
        except Exception as e:
            print(f"Error loading parameters: {e}")
            return False

    

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
            # self.current_input.focus = False
            if self.vkeyboard.parent:
                self.remove_widget(self.vkeyboard)
        else:
            self.current_input.insert_text(key)


    # when the start button is pressed, the rest of the data entered is updated to the trial parameter variables
    def start_action(self, instance):
        if self.service_manager:
            self.service_manager.trialParameters.USER = self.user_name_input.text
            self.service_manager.trialParameters.TRIAL = int(self.trial_number_input.text) if self.trial_number_input.text.isdigit() else 0
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
    def on_pre_enter(self):
        """Refresh input fields using trialParameters before the screen appears."""
        if self.service_manager:
            tp = self.service_manager.trialParameters
            self.bacteria_name_input.text = tp.UID
            self.record_duration_input.text = str(tp.RECORD_DURATION)
            self.trial_number_input.text = str(tp.TRIAL)
            self.user_name_input.text = tp.USER
            

            # Set radio buttons
            self.option1.active = tp.MODE == 'BreathEmulate'
            self.option2.active = tp.MODE == 'Static'
            self.option3.active = tp.MODE == 'Combined'
    '''
    


# Screen 3: Analysis Info
class AnalysisInfoScreen(Screen):
    def __init__(self, service_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.service_manager = service_manager

        self.current_input = None 

        self.vkeyboard = VKeyboard()
        self.vkeyboard.layout = 'qwerty'
        self.vkeyboard.size_hint_y = None
        self.vkeyboard.height = Window.height * 0.23
        self.vkeyboard.width = Window.width * 0.6
        self.vkeyboard.bind(on_key_up=self.on_key_up)

        layout = BoxLayout(orientation='vertical', spacing=3, padding=5)
        '''
        welcome_label3 = Label(
            text="New Analysis",
            font_size=15,
            size_hint=(1, 0.15),  # Small space at the top
            halign='center',
            valign='middle'
        )
        layout.add_widget(welcome_label3)
        '''
        self.user_name_input = self._create_input(layout, 'User Name:', 'Enter username')
        self.trial_number_input = self._create_input(layout, 'Trial Number:', 'Enter trial number')
        self.bacteria_name_input = self._create_input(layout, 'Bacteria Name:', 'Enter bacteria name')
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
            self.service_manager.trialParameters.USER = self.user_name_input.text
            self.service_manager.trialParameters.TRIAL = int(self.trial_number_input.text) if self.trial_number_input.text.isdigit() else 0
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
    
    def populate_fields_from_params(self):
        if not self.service_manager:
            return

        params = self.service_manager.trialParameters
        self.user_name_input.text = params.USER
        self.trial_number_input.text = str(params.TRIAL)
        self.bacteria_name_input.text = params.UID
        self.record_duration_input.text = str(params.RECORD_DURATION)

        self.option1.active = params.MODE == 'BreathEmulate'
        self.option2.active = params.MODE == 'Static'
        self.option3.active = params.MODE == 'Combined'


    