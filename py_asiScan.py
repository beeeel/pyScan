# Example action in py_asiScan.py
class asiScanAction:
    def __init__(self):
        self.parameters = {}
        self.child_actions = []

    def _generic_parse_line(self, line):
        """Generic parsing method to store lines in the parameters dictionary."""
        parts = line.split()
        key = parts[0]
        value = parts[1:]
        self.parameters[key] = value

    def add_child(self, child_action):
        """Add child actions."""
        self.child_actions.append(child_action)

    def run(self):
        """Process the stored parameters and execute the action."""
        axis = int(self.parameters.get('axis', [0])[0])
        scan_values = list(map(float, self.parameters.get('scan', [])))
        restore = 'restore' in self.parameters
        save = 'save' in self.parameters

        print(f"Running asiScan Action: axis={axis}, scan={scan_values}, restore={restore}, save={save}")

        # Simulate scanning over the defined range
        scan_start, scan_end, step_size = scan_values
        current_position = scan_start

        while current_position <= scan_end:
            print(f"Moving to position {current_position} on axis {axis}")

            # Execute each child action at this position
            for child_action in self.child_actions:
                child_action.run()

            current_position += step_size

        if restore:
            print(f"Restoring position on axis {axis}.")

        if save:
            print("Saving scan data.")
