import os
from py_common import Action  # Import the Action superclass
import nidaqmx
from nidaqmx.constants import AcquisitionType, TerminalConfiguration
import numpy as np

class A2D(Action):
    def __init__(self, confile_name):
        super().__init__(confile_name)
        self.channels = []
        self.range = 10.0       # Default voltage range (e.g., ±10V)
        self.sample_rate = 10000  # Default rate in Hz
        self.num_samples = 1000   # Default number of samples
        self.data = []         # To hold acquired data
        self.task = None         # DAQ task handle (initialized in setup)
        self.device = "Dev1"
        self.data_file_handles = []
        self.parent = None

    def setup_daq(self):
        """Set up the DAQ card task for analog input according to specified parameters."""
        try:
            self.task = nidaqmx.Task()
            # Add channels
            for channel in self.channels:
                self.task.ai_channels.add_ai_voltage_chan(
                    f"{self.device}/{channel}",
                    terminal_config=TerminalConfiguration.DEFAULT,
                    min_val=-self.range,
                    max_val=self.range
                )
            # Configure timing
            self.task.timing.cfg_samp_clk_timing(
                rate=self.sample_rate,
                sample_mode=AcquisitionType.FINITE,
                samps_per_chan=self.num_samples
            )
            print(f"DAQ task configured with channels: {self.channels}")
        except nidaqmx.DaqError as e:
            print(f"Error during DAQ setup: {e}")
            raise

    def setup(self):
        """Main setup method that configures the DAQ, file handles, and any child actions."""
        super().setup()  # Call the superclass setup first
        
        # Extract relevant parameters
        self.sample_rate = int(self.parameters.get("rate", self.sample_rate))
        self.num_samples = int(self.parameters.get("samples", self.num_samples))
        self.channels    = self.parameters.get("channels", [])
        self.range       = float(self.parameters.get("range", self.range))
        self.device      = self.parameters.get("device", self.device)
        
        if len(self.channels) == 1:
            self.channels = [self.channels]
        
        # Set up the DAQ card task
        print(f"Setting up A2D with channels {self.channels}, range {self.range} V, "
              f"sample rate {self.sample_rate} Hz, samples {self.num_samples}.")
        self.setup_daq()

        # Create and open files for each channel, using a unique filename
        for channel in self.channels:
            filename = f"{self.confile_name}_channel{channel}.bin"
            if os.path.exists(filename):
                raise FileExistsError(f"File {filename} already exists. Please remove it or change configuration.")
            # Open file for writing binary data and store the handle
            self.data_file_handles.append(open(filename, 'wb'))
            print(f"Data for channel {channel} will be saved to {filename}.")

        # Call setup on each child action
        for child_action in self.child_actions:
            child_action.setup()
            
    def acquire_data2(self):
        """Acquire data from the DAQ card and store it in `self.data`."""
        # Read data from the task
        self.data = self.task.read(number_of_samples_per_channel=self.num_samples)
        print(f"Data acquired for channels: {self.channels}")

            
    def acquire_data(self):
        """Acquire data from the DAQ card and store it in `self.data`."""
        data = None  # Initialize as None; we'll define its structure after the first read
        total_samples = 0  # Track the total number of samples read

        while total_samples < self.num_samples:
            # Calculate how many samples are still needed
            samples_to_read = min(1000, self.num_samples - total_samples)
    
            try:
                # Read a chunk of data
                chunk = self.task.read(number_of_samples_per_channel=samples_to_read, timeout=5)
                
                # Initialize the data structure on the first iteration
                if data is None:
                    if isinstance(chunk, list):  # Multi-channel data: list of lists
                        data = [[] for _ in chunk]  # Create one sublist per channel
                    else:  # Single channel data: a single list
                        data = []
    
                # Append data from the chunk to the appropriate channel
                if isinstance(chunk, list):  # Multi-channel
                    for i, ch_data in enumerate(chunk):
                        data[i].extend(ch_data)
                else:  # Single channel
                    data.extend(chunk)
    
                total_samples += samples_to_read  # Update the total count of acquired samples
    
            except Exception as e:
                print(f"Error during data acquisition: {e}")
                break
    
        # Convert `data` to a consistent structure (list of lists for multi-channel, single list for single channel)
        if isinstance(data, list) and isinstance(data[0], list):  # Multi-channel
            self.data = [np.array(ch, dtype=np.float64) for ch in data]
        else:  # Single channel
            self.data = np.array(data, dtype=np.float64)
    
    def print_data(self):
        """Print the mean voltage for each channel from the acquired data."""
        if self.data is not None:
            if isinstance(self.data[0], list) or isinstance(self.data[0], np.ndarray):
                # Multi-channel data
                for i, channel_data in enumerate(self.data):
                    mean_voltage = np.mean(channel_data)
                    print(f"Channel {self.channels[i]} mean voltage: {mean_voltage:.6f} V")
            else:
                # Single-channel data
                mean_voltage = np.mean(self.data)
                print(f"Channel {self.channels[0]} mean voltage: {mean_voltage:.6f} V")
        else:
            print("No data available to print.")

    def save_data(self):
        """Write acquired data to the already-open binary file handles."""
        if self.data is not None:
            # Handle both single-channel and multi-channel data
            if isinstance(self.data[0], list) or isinstance(self.data[0], np.ndarray):
                # Multi-channel data
                for i, channel_data in enumerate(self.data):
                    file_handle = self.data_file_handles[i]
                    # Write data directly to the file handle
                    np.array(channel_data, dtype=np.float64).tofile(file_handle)
                    print(f"Data for {self.channels[i]} written to file.")
            else:
                # Single-channel data
                file_handle = self.data_file_handles[0]
                np.array(self.data, dtype=np.float64).tofile(file_handle)
                print(f"Data for {self.channels[0]} written to file.")
        else:
            print("No data to save.")

    def run(self):
        """Run the A2D acquisition and then run any child actions."""
        print("Running A2D data acquisition...")
        self.acquire_data()
        self.save_data()
        if self.parameters.get("print", "false").lower() in ["true", "1", "yes"]:
            self.print_data()
        # Run any child actions sequentially after data acquisition
        self.run_children()

    def cleanup(self):
        """Close DAQ resources, file handles, and perform cleanup."""
        if self.task:
            self.task.close()  # Close the DAQ task
            print("DAQ task closed.")
        
        # Close all file handles
        for file_handle in self.data_file_handles:
            file_handle.close()
        print("All data files have been closed.")

        # Call superclass cleanup
        super().cleanup()