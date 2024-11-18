"""
Generic stage action for pyScan stages to use. This way common things like scan grid construction will be easy to inherit.

Supported parameters:
    scan start step end
    axis_name name
    scan_mode [relative]/absolute
    restore true # always true if present, false if not present

Derived classes must implement:
    get_here
    go_to

Optional setup and init can supplement superclass setup by including super().setup()

"""
from py_common import Action

class Stage1D(Action):
    def __init__(self, **kwargs):
        """
        Initializes the 1D stage.
        
        Parameters:
        - axis_name (str): Name of the axis (e.g., 'X', 'Y', 'Z').
        """
        super().__init__(**kwargs)
        self.axis_name = ""
        
        # Scan logic/prealloc
        self.scan_points = []  # List of points to scan
        self.current_point_index = 0  # Index of the next point to visit
        self.initial_position = 0.0
        
        # Scan options
        self.start = 0.0
        self.step = 0.0
        self.end = 0.0
            
    def setup(self):
        """
        Setup method for the stage, called before the action is run.
        """
        # I guess I need the axis name somewhere
        self.axis_name = self.parameters.get("axis_name", "")[0]

        super().setup()
        print(f"Setting up {self.axis_name}-Axis Stage.")
        
        # Parse the scan parameters and scan mode
        scan_mode = self.parameters.get("scan_mode", ["relative"])[0]  # Default to relative mode
        scan_params = self.parameters.get("scan", None)

        if not scan_params:
            raise ValueError(f"No scan parameters provided for {self.axis_name}-Axis.")
        
        try:
            self.start = float(scan_params[0])
            self.step = float(scan_params[1])
            self.end = float(scan_params[2])
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid scan parameters for {self.axis_name}-Axis: {e}")
        
        # Maybe find where we are
        if scan_mode == "relative" or "restore" in self.parameters:
            # Get current location (only needed for relative scans or when restoring)
            self.get_here()

        # Choose the appropriate grid constructor
        if scan_mode == "relative":
            self.construct_grid_relative()
        elif scan_mode == "absolute":
            self.construct_grid_absolute()
        else:
            raise ValueError(f"Unknown scan mode '{scan_mode}' for {self.axis_name}-Axis.")

    def run(self):
        """
        Runs the stage action. Typically moves to the next point.
        """
        if not self.scan_points:
            raise ValueError("No scan points defined. Use construct_grid_relative or construct_grid_absolute.")

        next_point = self.get_next_point()
        print(f"{self.axis_name}-Axis: Moving to next point {next_point}.")
        self.go_to(next_point)

        # If there are child actions, run them as well.
        for child in self.children:
            child.run()

    def cleanup(self):
        """
        Cleanup method for the stage, called after the action is run.
        """
        if "restore" in self.parameters:
            self.go_to(self.initial_position)

        super().cleanup()
        print(f"Cleaning up {self.axis_name}-Axis Stage.")

    def construct_grid_relative(self, initial_position=self.initial_position):
        """
        Constructs a regular grid of points relative to the starting position.
        """
        num_points = int((self.end - self.start) / self.step) + 1
        self.scan_points = [initial_position + i * self.step for i in range(num_points)]
        self.current_point_index = 0  # Reset index
        print(f"{self.axis_name}-Axis Grid: {self.scan_points}")

    def construct_grid_absolute(self):
        """
        Constructs a grid using absolute positions.
        """
        self.construct_grid_relative(initial_position=0)

    def get_next_point(self):
        """
        Retrieves the next point in the scan sequence and updates the index.
        
        Returns:
        - next_point (float): The next point to scan.
        """
        if not self.scan_points:
            raise ValueError("Scan grid is empty. Construct a grid first.")
        
        next_point = self.scan_points[self.current_point_index]
        self.current_point_index = (self.current_point_index + 1) % len(self.scan_points)  # Wrap around
        return next_point

    def go_to(self, point):
        """
        Placeholder for moving the stage to a specific point. 
        
        Parameters:
        - point (float): Target position for the stage.
        """
        raise NotImplementedError("Derived classes must implement the 'go_to' method.")
    
    def get_here(self):
        """
        Placeholder for finding current co-ordinate.
        Derived classes must implement this method which fills self.initial_position
        """
        raise NotImplementedError("Derived classes must implement the 'get_here' method.")

    def move_to_next_point(self):
        """
        Moves to the next point in the scan grid.
        """
        next_point = self.get_next_point()
        print(f"Moving {self.axis_name}-Axis to: {next_point}")
        self.go_to(next_point)  # Derived class will handle actual hardware interaction
