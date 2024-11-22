# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 17:19:33 2024

@author: chatGPT
@curator: Will Hardiman
"""

import time
from py_common import Action

class sleep(Action):
    def __init__(self, filebase=None):
        """
        Initialize the Sleep action.
        :param filebase: The base name of the con file, if needed for context.
        """
        super().__init__(filebase)
        self.parent = None
        self.sleep_time = 0  # Total sleep time in seconds

    def setup(self):
        """
        Setup the Sleep action by calculating the total sleep time.
        """
        super().setup()
        # Extract user-specified times
        hours = float(self.parameters.get("hours", 0))
        minutes = float(self.parameters.get("minutes", 0))
        seconds = float(self.parameters.get("seconds", 0))
        
        # Convert to total seconds
        self.sleep_time = int(hours * 3600 + minutes * 60 + seconds)
        print(f"Sleep action set up to wait for {self.sleep_time} seconds.")

    def run(self):
        """
        Execute the Sleep action by pausing for the calculated duration.
        """
        if self.sleep_time > 0:
            print(f"Sleeping for {self.sleep_time} seconds...")
            time.sleep(self.sleep_time)
            print("Sleep completed.")
        else:
            print("Sleep time is zero or invalid. Skipping sleep.")
            
        self.run_children()

    def cleanup(self):
        """
        Cleanup resources after the Sleep action. No specific cleanup is needed for Sleep.
        """
        print("Sleep action cleanup complete.")
        super().cleanup()
