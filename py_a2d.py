# Example action in py_a2d.py
class a2dAction:
    def __init__(self):
        self.parameters = {}

    def _generic_parse_line(self, line):
        """Generic parsing method to store lines in the parameters dictionary."""
        parts = line.split()
        key = parts[0]
        value = parts[1:]
        self.parameters[key] = value

    def run(self):
        """Process the stored parameters and execute the action."""
        channels = list(map(int, self.parameters.get('channels', [])))
        rate = int(self.parameters.get('rate', [0])[0])
        range_val = float(self.parameters.get('range', [0])[0])
        samples = int(self.parameters.get('samples', [0])[0])

        print(f"Running A2D Action: channels={channels}, rate={rate}, range={range_val}, samples={samples}")
