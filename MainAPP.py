# MainAPP.py

from kivy.app import App
from ServiceManager import ServiceManager
from first_UI import HeaderFooterLayout
from tab1 import Tab1Content

class PranasApp(App):
    def build(self):
        # Create the Tab1Content UI and ServiceManager
        service_manager = ServiceManager(gui=None)  # Initialize ServiceManager
        layout = HeaderFooterLayout(service_manager)  # Pass ServiceManager to Tab1Content
        
        # Update the ServiceManager with the Tab1Content as the GUI
        service_manager.gui = layout

        return layout

if __name__ == '__main__':
    PranasApp().run()
