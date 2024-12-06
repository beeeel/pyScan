"""
pyScan.py

Project Description:
---------------------
pyScan is a versatile and extensible framework for configuring and running experimental data acquisition and control 
routines. It reads user-defined "con" configuration files, initializes hardware resources, and executes nested sequences 
of actions such as analog-to-digital conversion (A2D), stage movements, delays, and more.

The framework is designed to be modular, allowing users to easily add new hardware or functionality by implementing 
custom action classes.

How to Use:
-----------
1. Prepare a configuration file (".con") specifying the desired sequence of actions, hardware parameters, and settings.
   - Example format:
     ```
     action A2D
         rate 10000
         samples 5000
     end
     ```

2. Run the program from the command line or within an IDE:
   - Command line:
     ```
     python pyScan.py <confile>
     ```
   - From Spyder:
     ```
     runfile('<path-to-pyScan.py>', args='<confile>')
     ```

3. Logs and data files will be saved in the working directory or an optional dedicated folder (to be implemented).

Known Bugs/Flaws/Limitations:
-----------------------------
1. **Beep Action Limitation**: The current implementation of the "beep" action does not preserve the exact order of 
   "beep" and "boop" commands from the configuration file due to dictionary-based parameter parsing.
2. **File Handling**: No user interaction to handle existing files (overwrite/append/rename). Planned improvement.
3. **Stage Precision**: Movements are subject to hardware-specific precision limits. Users must ensure compatibility.
4. **Error Handling**: Exceptions are caught and logged, but some actions may not gracefully recover from critical errors.
5. **Logging**: Console output is not yet logged to a file (planned improvement).
6. **Cross-platform Issues**: Some features, like hardware detection, may behave differently on Linux vs. Windows.
7. **Repeated actions**: Unknown behaviour for repeated A2D actions, probably the system cannot deal with it.

Authors:
--------
- Framework Author: ChatGPT (OpenAI)
- Project Curator: Will Hardiman (OPG, University of Nottingham) [bill.hardiman1995@gmail.com]
"""

import importlib
import argparse
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
                        current_action.parent = parent_action
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

            elif word!= '#':
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
    # Create argument parser
    parser = argparse.ArgumentParser(description="Run a microscope scan based on a configuration file.")
    parser.add_argument(
            "confile",
            type=str,
            nargs="?",
            default="trapped_bead_2.con",
            help="Path to the .con configuration file (default: default.con)."
        )
    # Parse arguments
    args = parser.parse_args()

    # Create an ActionParser instance and run the experiment
    try:
        parser = ActionParser(args.confile)
        parser.parse()
        parser.setup_actions()
        parser.run_actions()
    finally:
        parser.cleanup_actions()
