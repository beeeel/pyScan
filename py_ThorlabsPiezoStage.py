# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 13:40:49 2024

@author: chatGPT
@curator: Will Hardiman
"""

from py_common import Stage1D
from pylablib.devices import Thorlabs

class ThorlabsPiezoStage(Stage1D):
    """
    Class to control a Thorlabs PFM450 piezo stage using the pylablib library.
    Inherits from Stage1D.
    """

    def __init__(self, filebase):
        super().__init__(filebase)
        self.device = None  # Placeholder for the Thorlabs device connection
        self.serial_number = None  # Serial number for the target device

    def setup(self):
        """Set up the Thorlabs Piezo Stage connection."""
        super().setup()  # Call parent setup to parse parameters

        # Get the list of connected Kinesis devices
        devices = Thorlabs.list_kinesis_devices()
        piezo_devices = [dev for dev in devices if "Piezo Controller" in dev[1]]

        # Check for serial number in the parameters
        self.serial_number = self.parameters.get("serial_number", None)

        if not piezo_devices:
            raise RuntimeError("No Thorlabs piezo devices found.")
        elif len(piezo_devices) == 1 and not self.serial_number:
            # Automatically use the single piezo device
            self.serial_number = piezo_devices[0][0]
            print(f"Auto-detected piezo device: {self.serial_number}")
        elif self.serial_number not in [dev[0] for dev in piezo_devices]:
            # If a serial number is specified, validate it
            raise ValueError(f"Specified serial number {self.serial_number} not found.")
        
        # Connect to the piezo device
        self.device = Thorlabs.KinesisPiezo(self.serial_number)
        print(f"Connected to Thorlabs Piezo Controller: {self.serial_number}")

    def go_to(self, point):
        """Move the piezo stage to the specified position."""
        if not self.device:
            raise RuntimeError("Piezo device not initialized.")
        print(f"Moving {self.axis_name}-axis to {point} microns.")
        self.device.move_to(point)

    def get_here(self):
        """Get the current position of the piezo stage."""
        if not self.device:
            raise RuntimeError("Piezo device not initialized.")
        self.initial_position = self.device.get_position()
        print(f"Current {self.axis_name}-axis position: {self.initial_position} microns.")
        return self.initial_position

    def cleanup(self):
        """Clean up the device connection."""
        if self.device:
            self.device.close()
            print(f"Closed connection to piezo device: {self.serial_number}")
        super().cleanup()  # Call parent cleanup
