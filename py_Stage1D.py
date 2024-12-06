# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 14:28:04 2024

@author: ezzwh
"""

class Stage1D:
    def __init__(self, axis_name="X"):
        """
        Initializes the 1D stage.
        
        Parameters:
        - axis_name (str): Name of the axis (e.g., 'X', 'Y', 'Z').
        """
        self.axis_name = axis_name
        self.scan_points = []  # List of points to scan
        self.current_point_index = 0  # Index of the next point to visit

    def construct_grid_relative(self, start=0, step=1, num_points=10):
        """
        Constructs a regular grid of points relative to the starting position.
        
        Parameters:
        - start (float): The starting position of the grid.
        - step (float): Step size between points.
        - num_points (int): Number of points in the grid.
        """
        self.scan_points = [start + i * step for i in range(num_points)]
        self.current_point_index = 0  # Reset index
        print(f"{self.axis_name}-Axis Grid (Relative): {self.scan_points}")

    def construct_grid_absolute(self, points):
        """
        Constructs a grid using absolute positions.
        
        Parameters:
        - points (list of float): List of absolute positions to scan.
        """
        self.scan_points = points
        self.current_point_index = 0  # Reset index
        print(f"{self.axis_name}-Axis Grid (Absolute): {self.scan_points}")

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

    def move_to_next_point(self):
        """
        Moves to the next point in the scan grid.
        """
        next_point = self.get_next_point()
        print(f"Moving {self.axis_name}-Axis to: {next_point}")
        self.go_to(next_point)  # Derived class will handle actual hardware interaction
