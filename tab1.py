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

# Tab1Content uses ScreenManager to create two screens. (makes ui more user friendly and lowk spaced)
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
            text="Welcome! Choose an option:",
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

 


class OldAnalysisInfoScreen(Screen):
    def __init__(self, service_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.service_manager = service_manager

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        layout.add_widget(Label(text='Old Analysis Logs', font_size=20, size_hint=(1, 0.1)))

        # Scrollable area for logs
        scroll_view = ScrollView(size_hint=(1, 0.8))
        self.log_grid = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.log_grid.bind(minimum_height=self.log_grid.setter('height'))
        scroll_view.add_widget(self.log_grid)
        layout.add_widget(scroll_view)

        # Back button
        back_button = Button(text='Back', size_hint=(None, None), size=(300, 40), pos_hint={'center_x': 0.5})
        back_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'user'))
        layout.add_widget(back_button)

        self.add_widget(layout)

        # Populate log entries
        self.populate_logs()

    def populate_logs(self):
        self.log_grid.clear_widgets()

        if self.service_manager and hasattr(self.service_manager, 'get_old_analysis_info'):
            old_logs = self.service_manager.get_old_analysis_info()

            for log in old_logs:
                btn_text = f"{log.get('UID', 'Unknown')} | {log.get('MODE', '')} | {log.get('SAMPLING_RATE', '')} Hz"
                btn = Button(text=btn_text, size_hint_y=None, height=40)
                btn.bind(on_press=lambda inst, log=log: self.load_old_log(log))  # bind log as default argument
                self.log_grid.add_widget(btn)
        else:
            self.log_grid.add_widget(Label(text="No log data found."))

    def load_old_log(self, log_data):
        """Load selected log into trialParameters and navigate to analysis screen."""
        if not self.service_manager:
            return

        tp = self.service_manager.trialParameters
        tp.USER = log_data.get("User", "") or log_data.get("User Name", "")
        tp.UID = log_data.get("UID", "") or log_data.get("Bacteria Name", "")
        tp.TRIAL = log_data.get("TRIAL", 0) or log_data.get("Trial Number", 0)
        tp.RECORD_DURATION = log_data.get("RECORD_DURATION", 0)
        tp.MODE = log_data.get("MODE", "")

        # Set flags so analysis screen knows it's ready
        self.service_manager.deviceFlags.CONFIGURE_FLAG = True
        self.service_manager.deviceFlags.START_FLAG = False  # Wait until user presses START

        # Optional: write logs again
        if hasattr(self.service_manager, 'logFileManage'):
            log_writer = self.service_manager.logFileManage
            log_writer.WriteLog(f'Loaded old log for UID: {tp.UID}', 0)
            log_writer.WriteLog(f'Mode: {tp.MODE}', 0)
            log_writer.WriteLog(f'Trial: {tp.TRIAL}', 0)
            log_writer.WriteLog(f'Duration: {tp.RECORD_DURATION} seconds', 0)
            log_writer.WriteLog(f'User: {tp.USER}', 0)
            log_writer.WriteLog('-----------------------------------', 0)

        # Switch to the analysis screen
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
        self.vkeyboard.height = Window.height * 0.25
        self.vkeyboard.width = Window.width * 0.6
        self.vkeyboard.bind(on_key_up=self.on_key_up)

        layout = BoxLayout(orientation='vertical', spacing=3, padding=5)

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


