import importlib

def read_config_file(confile):
    """Reads the configuration file and returns its contents as a list of lines."""
    with open(confile, 'r') as file:
        return file.readlines()

class ActionParser:
    def __init__(self, confile):
        self.filepath = confile
        self.actions = []
        self.imported_modules = {}

    def parse(self):
        """Parse the action file and dynamically import action modules."""
        config_lines = read_config_file(self.filepath)
        self._parse_lines(config_lines)

    def _parse_lines(self, lines, parent_action=None):
        """Process each line and allocate action objects based on modules."""
        lastword = ""
        current_action = None
        i = 0

        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue  # Skip empty lines

            words = line.split()
            word = words[0]

            # Check if this is an action and import a corresponding module
            if word == "action":
                module_name = "py_" + words[1]  # Assuming the module name follows the word 'action'
                try:
                    # Dynamically import the module
                    imported_module = importlib.import_module(module_name)
                    # Store the imported module in a dictionary
                    self.imported_modules[module_name] = imported_module
                    print(f"Successfully imported module: {module_name}")
                    # Create an instance of the action class from the module
                    current_action = imported_module.Action()  # Assuming each module has an Action class

                    if parent_action:
                        parent_action.add_child(current_action)
                    else:
                        self.actions.append(current_action)

                except ImportError as e:
                    print(f"Error importing module {module_name}: {e}")
                    current_action = None  # In case of failure, do not process further
            elif word == "end":
                return i  # End of the current action, return to parent level
            else:
                # Let the action object parse its own lines until 'end' is encountered
                current_action._generic_parse_line(line)

            i += 1

    def run_actions(self):
        """Execute all actions by calling their 'run' method."""
        for action in self.actions:
            if hasattr(action, 'run'):
                action.run()
            else:
                print(f"Module {action.__class__.__name__} does not have a 'run' method.")


# Example usage
if __name__ == "__main__":
    config_file_path = 'example_con.con'  # Replace with your config file path
    parser = ActionParser(config_file_path)
    parser.parse()
    parser.run_actions()

