# FlowManager.py

from DataClasses import TrialParameters

class FlowManager:
    """
    This class retrieves input data from the GUI's Tab1Content and stores it in TrialParameters.
    """

    def __init__(self, tab1_content,currentService):
        """
        Initialize with a reference to the GUI's Tab1Content.
        """
        self.tab1_content = tab1_content  # Reference to the Tab1Content instance
        self.currentService=currentService

    def update_trial_parameters(self):
        """Fetch input data from Tab1Content and store it in TrialParameters."""
        # Set the values from the GUI inputs to TrialParameters
        self.currentService.trialParameters.USER = self.tab1_content.user_name_input.text
        self.currentService.trialParameters.UID = self.tab1_content.bacteria_name_input.text
        self.currentService.trialParameters.TRIAL = int(self.tab1_content.trial_number_input.text)

        # Determine which analysis type is selected from the radio buttons
        if self.tab1_content.option1.active:
            self.currentService.trialParameters.MODE = "BreathEmulate"
        elif self.tab1_content.option2.active:
            self.currentService.trialParameters.MODE = "Static"
        elif self.tab1_content.option3.active:
           self.currentService.trialParameters.MODE = 'Combined'
        else:
            self.currentService.trialParameters.MODE = 'No option selected'

        # Log the fetched parameters (can be replaced with actual logging)
        print("Trial Parameters Updated:")
        print(f"USER (User Name): {self.trialParameters.USER}")
        print(f"UID (Bacteria Name): {self.trialParameters.UID}")
        print(f"Trial Number: {self.trialParameters.TRIAL}")
        print(f"Analysis Type: {self.trialParameters.MODE}")

    def get_trial_parameters(self):
        """Return the current trial parameters."""
        return self.trialParameters
