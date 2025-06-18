# main.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Line, Color

from tab1 import Tab1Content
from tab2 import Tab2Content
from tab3 import Tab3Content

from ServiceManager import ServiceManager

class HeaderFooterLayout(BoxLayout):
    def __init__(self, service_manager,**kwargs):
        super().__init__(**kwargs)
        self.service_manager = service_manager
        self.orientation = 'vertical'

        # Create and add the header
        header = self.create_header()
        self.add_widget(header)

        # self.tab1_content = Tab1Content(service_manager)
        # self.add_widget(self.tab1_content)
        # Create and add the body with tabs and the reset button
        body = self.create_body()
        self.add_widget(body)

        # Create and add the footer
        footer = self.create_footer()
        self.add_widget(footer)

    def create_header(self):
        """Create the header layout with an image and text."""
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=10)

        with header.canvas.after:
            Color(1, 0, 0, 1)  # Red color
            self.header_line = Line(points=[0, 0, header.width, 0], width=2)

        header.bind(size=self.update_header_line, pos=self.update_header_line)

        header.add_widget(Image(source='Images/icon.ico', size_hint=(0.1, 1)))

        header.add_widget(Label(
            text='Personal Respiratory Analyzing System',
            font_size=40, bold=True, halign='left', color=(0, 1, 0, 1)
        ))

        return header

    def create_body(self):
        """Create the body layout with a reset button and tabs."""
        body = BoxLayout(orientation='horizontal', size_hint=(1, 0.8), padding=10, spacing=10)

        # Create the left column with the reset button and tabs
        left_column = BoxLayout(orientation='vertical', size_hint_x=0.6)

        # Add the reset button at the top of the left column
        reset_button = Button(
            text='Reset Tabs',
            size_hint=(1, 0.1),
            background_color=(1, 0, 0, 1)  # Red color
        )
        reset_button.bind(on_press=self.reset_tabs)

        # Add the reset button to the left column
        left_column.add_widget(reset_button)

        # Add the TabbedPanel below the reset button
        self.tab_panel = self.create_tabs()
        left_column.add_widget(self.tab_panel)

        # Create the right column content split into two rows with a separator
        right_column = self.create_right_column()

        # Add the left and right columns to the body
        body.add_widget(left_column)

        with body.canvas.after:
            Color(1, 1, 1, 1)  # White color
            self.separator_line = Line(width=2)

        body.add_widget(right_column)

        body.bind(size=self.update_body_separator, pos=self.update_body_separator)

        return body

    def create_tabs(self):
        """Create a TabbedPanel with three tabs."""
        tab_panel = TabbedPanel(do_default_tab=False)  # Disable default tab

        # Create Tab 1
        self.tab1 = TabbedPanelItem(text='Tab 1')
        self.tab1.content = Tab1Content(self.service_manager)
        tab_panel.add_widget(self.tab1)

        # Create Tab 2
        self.tab2 = TabbedPanelItem(text='Tab 2')
        self.tab2.content = Tab2Content()
        tab_panel.add_widget(self.tab2)

        # Create Tab 3
        self.tab3 = TabbedPanelItem(text='Tab 3')
        self.tab3.content = Tab3Content()
        tab_panel.add_widget(self.tab3)

        return tab_panel

    def create_right_column(self):
        """Create the right column split into two rows with a line separator."""
        right_column = BoxLayout(orientation='vertical', size_hint_x=0.4, spacing=10)

        # Create two rows
        row1 = Label(text='SIGNAL', font_size=24, size_hint=(1, 0.5),color=(1,1,0,1))
        row2 = Label(text='METRICS', font_size=24, size_hint=(1, 0.5),color=(1,1,0,1))

        # Add the first row
        right_column.add_widget(row1)

        # Draw a separator line between the two rows
        with right_column.canvas.after:
            Color(1, 1, 1, 1)  # Red color for the line
            self.row_separator = Line(points=[0, right_column.height / 2, right_column.width, right_column.height / 2], width=2)

        # Bind size and position to update the separator dynamically
        right_column.bind(size=self.update_row_separator, pos=self.update_row_separator)

        # Add the second row
        right_column.add_widget(row2)

        return right_column

    def update_row_separator(self, instance, value):
        """Update the separator line between the rows."""
        self.row_separator.points = [
            instance.x, instance.center_y,  # Start at the center
            instance.right, instance.center_y  # End at the center
        ]

    def reset_tabs(self, instance):
        """Reset the content of all tabs to their initial state."""
        current_tab = self.tab_panel.current_tab
        self.tab1.content = Tab1Content(self.service_manager)
        self.tab2.content = Tab2Content()
        self.tab3.content = Tab3Content()

    def create_footer(self):
        """Create the footer layout with images and text."""
        footer = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=10)

        with footer.canvas.before:
            Color(1, 0, 0, 1)  # Red color
            self.footer_line = Line(points=[0, footer.height, footer.width, footer.height], width=2)

        footer.bind(size=self.update_footer_line, pos=self.update_footer_line)

        footer.add_widget(Image(source='Images/ugalogo.png', size_hint=(0.1, 1)))

        footer.add_widget(Label(
            text='Developed at Design Informatics and Computational Engineering Lab,\n'
                 'University of Georgia, Athens, GA, USA',
            font_size=16, halign='center'
        ))

        footer.add_widget(Image(source='Images/dicelogo.jpg', size_hint=(0.1, 1)))

        return footer

    def update_header_line(self, instance, value):
        """Update the header line dynamically."""
        self.header_line.points = [instance.x, instance.y, instance.right, instance.y]

    def update_footer_line(self, instance, value):
        """Update the footer line dynamically."""
        self.footer_line.points = [instance.x, instance.top, instance.right, instance.top]

    def update_body_separator(self, instance, value):
        """Update the separator line dynamically between columns."""
        separator_x = instance.width * 0.6  # 60% of the body's width
        self.separator_line.points = [separator_x, instance.y, separator_x, instance.top]

service_manager = ServiceManager(gui=None)

class PranasApp(App):
        def build(self):
                return HeaderFooterLayout(service_manager)

if __name__ == '__main__':
    PranasApp().run()
