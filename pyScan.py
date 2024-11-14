import importlib
#from py_common import Action

def read_config_file(confile):
    """Reads the configuration file and returns its contents as a list of lines."""
    with open(confile, 'r') as file:
        return file.readlines()

class ActionParser:
    def __init__(self, confile):
        self.confile = confile
        self.filebase = confile.split(".")[0]  # Get the base name without extension
        self.actions = []
        self.imported_modules = {}

    def parse(self):
        with open(self.confile, 'r') as file:
            config_lines = file.readlines()

        parent_action = None
        current_action = None

        for line in config_lines:
            words = line.strip().split()
            if not words:
                continue  # Skip empty lines

            word = words[0]

            if word == "action":
                module_name = "py_" + words[1]  # Assuming the module name follows the word 'action'
                class_name = words[1]           # Use the action name directly for the class name
                try:
                    # Store the imported module in a dictionary if not already imported
                    if module_name not in self.imported_modules:
                        # Dynamically import the module
                        imported_module = importlib.import_module(module_name)
                        # Store it
                        self.imported_modules[module_name] = imported_module
                        print(f"Successfully imported module: {module_name}")

                    # Get the specific class (e.g., A2D or asiScan) from the module and instantiate it
                    action_class = getattr(imported_module, class_name)
                    current_action = action_class(self.filebase)  # Pass filebase to the action instance

                    # Add current_action as a child if inside another action, otherwise add it to main actions
                    if parent_action:
                        parent_action.add_child_action(current_action)
                    else:
                        self.actions.append(current_action)

                    # Update parent_action to allow nested actions if required
                    parent_action = current_action

                except (ImportError, AttributeError) as e:
                    print(f"Error importing or instantiating {class_name} from {module_name}: {e}")

            elif word == "end":
                # Move up one level in the action hierarchy if 'end' is encountered
                if parent_action:
                    parent_action = parent_action.parent if hasattr(parent_action, 'parent') else None

            else:
                # Let the current action parse its specific line
                if current_action:
                    current_action.parse_line(words)

    def setup_actions(self):
        """Set up all actions in sequence."""
        print("Starting setup of actions...")
        for action in self.actions:
            action.setup()
        print("Setup of actions completed.")

    def run_actions(self):
        """Run all actions in sequence."""
        print("Starting execution of actions...")
        for action in self.actions:
            action.run()
        print("Execution of actions completed.")

    def cleanup_actions(self):
        """Clean up all actions in sequence."""
        print("Starting cleanup of actions...")
        for action in self.actions:
            action.cleanup()
        print("Cleanup of actions completed.")


# Example usage
if __name__ == "__main__":
    config_file_path = 'example.con'  # Replace with your config file path
    parser = ActionParser(config_file_path)
    parser.parse()
    parser.setup_actions()
    parser.run_actions()
    parser.cleanup_actions()

