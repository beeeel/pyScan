# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 16:24:05 2024

@author: chatGPT
@curator: Will Hardiman
"""

from py_common import Action

class count(Action):
    def __init__(self, filebase):
        super().__init__(filebase)
        self.parent = None
        self.count = 1  # Default count value

    def setup(self):
        """Parse parameters and set up for repeated execution."""
        super().setup()
        # Get the count parameter and ensure it is an integer
        self.count = int(self.parameters.get("count", self.count))
        print(f"Count action set to repeat {self.count} times.")

    def run(self):
        """Run the child actions the specified number of times."""
        if not self.child_actions:
            print("Count action has no child actions to repeat.")
            return

        for i in range(self.count):
            print(f"Starting iteration {i+1} of {self.count}.")
            for child in self.child_actions:
                child.run()
            print(f"Completed iteration {i+1} of {self.count}.")

    def cleanup(self):
        """Clean up after all iterations."""
        super().cleanup()
        print("Count action cleanup complete.")
