import os
from py_common import Action  # Import the Action superclass
import nidaqmx
import numpy as np

class A2D(Action):
    def __init__(self, confile_name):
        super().__init__(confile_name)
        self.channels = []
        self.range = 10.0       # Default voltage range (e.g., ±10V)
        self.sample_rate = 10000  # Default rate in Hz
        self.num_samples = 1000   # Default number of samples
        self.data = None         # To hold acquired data
        self.task = None         # DAQ task handle (initialized in setup)

    def setup_daq(self):
        """Set up the DAQ card task for analog input according to specified parameters."""
        self.task = nidaqmx.Task()  # Create a DAQ task
        for channel in self.channels:
            # Configure each channel in the DAQ task
            self.task.ai_channels.add_ai_voltage_chan(
                f"Dev1/ai{channel}",
                min_val=-self.range,
                max_val=self.range
            )
        # Configure sample timing for the task
        self.task.timing.cfg_samp_clk_timing(
            rate=self.sample_rate,
            samps_per_chan=self.num_samples
        )

    def setup(self):
        """Main setup method that configures the DAQ, file handles, and any child actions."""
        super().setup()  # Call the superclass setup first
        print(f"Setting up A2D with channels {self.channels}, range {self.range} V, "
              f"sample rate {self.sample_rate} Hz, samples {self.num_samples}.")
        
        # Set up the DAQ card task
        self.setup_daq()

        # Create and open files for each channel, using a unique filename
        for channel in self.channels:
            filename = f"{self.confile_name}_channel{channel}.bin"
            if os.path.exists(filename):
                raise FileExistsError(f"File {filename} already exists. Please remove it or change configuration.")
            # Open file for writing binary data and store the handle
            self.data_file_handles[channel] = open(filename, 'wb')
            print(f"Data for channel {channel} will be saved to {filename}.")

        # Call setup on each child action
        for child_action in self.child_actions:
            child_action.setup()
            
    def acquire_data(self):
        """Acquire data from the DAQ card and store it in `self.data`."""
        self.data = self.task.read(number_of_samples_per_channel=self.num_samples)

    def save_data(self, filename="data.bin"):
        """Save acquired data to a binary file."""
        if self.data is not None:
            np.array(self.data).tofile(filename)  # Save data as binary
            print(f"Data saved to {filename}")
        else:
            print("No data to save.")

    def run(self):
        """Run the A2D acquisition and then run any child actions."""
        print("Running A2D data acquisition...")
        self.acquire_data()
        self.save_data()
        # Run any child actions sequentially after data acquisition
        self.run_children()

    def cleanup(self):
        """Close DAQ resources, file handles, and perform cleanup."""
        if self.task:
            self.task.close()  # Close the DAQ task
            print("DAQ task closed.")
        
        # Close all file handles
        for file_handle in self.data_file_handles.values():
            file_handle.close()
        print("All data files have been closed.")

        # Call superclass cleanup
        super().cleanup()