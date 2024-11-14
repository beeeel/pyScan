"""
Some common methods used by pyScan. Currently just the Action superclass.
"""

class Action:
    def __init__(self, confile_name=""):
        self.confile_name = confile_name  # Store the name of the .con file
        # Dictionary to store parsed parameters from configuration lines
        self.parameters = {}
        # List to hold child actions, for nested configurations
        self.child_actions = []

    def parse_line(self, words):
        """Parse a line from the config file, storing key-value pairs in the parameters dictionary."""
        if not words:
            return

        key = words[0]
        value = words[1:]  # Everything after the key is treated as a list of values
        # Store the value in the dictionary, as a list if multiple items, or a single value otherwise
        self.parameters[key] = value[0] if len(value) == 1 else value

    def add_child_action(self, action):
        """Add a child action to be managed and executed in sequence."""
        self.child_actions.append(action)

    def setup(self):
        """Setup resources for this action and all child actions."""
        print(f"Setting up action: {self.__class__.__name__}")
        
        # Setup all child actions recursively
        for child_action in self.child_actions:
            child_action.setup()

    def run(self):
        """Placeholder for the main run method, intended to be overridden."""
        print(f"Running placeholder for action: {self.__class__.__name__}")
        
        self.run_children()

    def run_children(self):
        """Execute each child action's run method in sequence."""
        for child_action in self.child_actions:
            child_action.run()

    def cleanup(self):
        """Release resources and cleanup for this action and all child actions."""
        print(f"Cleaning up action: {self.__class__.__name__}")
        
        # Cleanup all child actions recursively
        for child_action in self.child_actions:
            child_action.cleanup()
