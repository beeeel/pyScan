import platform
import serial
from py_stage1D import Stage1D

class AsiScan(Stage1D):
    def __init__(self, axis_name="X", port=None, baudrate=9600, timeout=1, **kwargs):
        """
        Initializes the ASI MS-2000 stage as a 1D stage with platform-specific default ports.
        
        Parameters:
        - axis_name (str): The axis to control ('X' or 'Y').
        - port (str): Serial port to communicate with the stage (overrides default).
        - baudrate (int): Baud rate for serial communication.
        - timeout (float): Timeout for serial communication in seconds.
        """
        super().__init__(axis_name=axis_name, **kwargs)

        # Platform-specific default ports
        if port is None:
            system = platform.system()
            if system == "Windows":
                self.port = "COM4"  # Default for Windows
            elif system == "Linux":
                self.port = "/dev/ttyUSB0"  # Default for Linux
            elif system == "Darwin":  # macOS
                self.port = "/dev/cu.usbserial"
            else:
                raise ValueError(f"Unsupported platform: {system}")
        else:
            self.port = port  # Override with user-specified port

        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None

    def setup(self):
        """
        Setup method for the ASI MS-2000 stage.
        Establishes the shared serial connection and queries the stage status.
        """
        super().setup()

        if "port" in self.parameters:
            port = self.parameters.get("port", None)
            if port is not None:
                self.port = port

        print(f"Setting up ASI MS-2000 {self.axis_name}-Axis Stage on port {self.port}.")

        # Get a shared serial connection
        self.serial_connection = SerialConnectionManager.get_connection(
            port=self.port, baudrate=self.baudrate, timeout=self.timeout
        )

        # Query the stage to confirm it's responsive
        try:
            self.serial_connection.write(b"WHERE\r")
            response = self.serial_connection.readline().decode().strip()
            print(f"Stage response: {response}")
        except serial.SerialException as e:
            raise RuntimeError(f"Error communicating with stage: {e}")

    def cleanup(self):
        """
        Cleanup method for the ASI MS-2000 stage.
        Closes the shared serial connection (if no other actions need it).
        """
        SerialConnectionManager.close_connection(self.port)
        super().cleanup()

    def go_to(self, point):
        """
        Moves the stage to a specified point on the given axis.

        Parameters:
        - point (float): The target position in mm.
        """
        if not self.serial_connection or not self.serial_connection.is_open:
            raise RuntimeError("Serial connection is not established.")

        # Construct and send the MOVE command
        command = f"MOVE {self.axis_name}={point:.6f}\r"
        self.serial_connection.write(command.encode())
        response = self.serial_connection.readline().decode().strip()
        print(f"Move response: {response}")

    def get_here(self):
        """
        Retrieves the current position of the stage on the specified axis
        and updates self.initial_position.
        """
        if not self.serial_connection or not self.serial_connection.is_open:
            raise RuntimeError("Serial connection is not established.")

        # Construct and send the WHERE command
        command = f"WHERE {self.axis_name}\r"
        self.serial_connection.write(command.encode())
        response = self.serial_connection.readline().decode().strip()

        try:
            # Parse the response to extract the position
            position = float(response.split('=')[1])
            self.initial_position = position
            print(f"{self.axis_name}-Axis Current Position: {self.initial_position} mm")
        except (IndexError, ValueError):
            raise RuntimeError(f"Failed to parse position from response: {response}")

