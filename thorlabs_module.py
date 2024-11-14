import thorlabs_camera  # Hypothetical wrapper for Thorlabs SDK
from PIL import Image
import numpy as np

class ThorlabsCameraAction:
    def __init__(self):
        self.camera = None
        self.image_filename = 'captured_image.png'
        self.exposure_time = 50  # Default exposure time in ms
        self.gain = 1.0  # Default gain

    def setup(self, exposure_time=None, gain=None, image_filename=None):
        """Setup camera parameters and connect to the camera."""
        self.camera = thorlabs_camera.Camera()

        # Override default settings if provided
        if exposure_time is not None:
            self.exposure_time = exposure_time
        if gain is not None:
            self.gain = gain
        if image_filename is not None:
            self.image_filename = image_filename

        try:
            # Connect to the camera
            self.camera.connect()
            print("Camera connected successfully.")

            # Set up camera parameters
            self.camera.set_exposure(self.exposure_time)
            self.camera.set_gain(self.gain)
            print(f"Camera setup: exposure time = {self.exposure_time} ms, gain = {self.gain}")

        except Exception as e:
            print(f"Error during camera setup: {e}")
            if self.camera:
                self.camera.disconnect()

    def run(self):
        """Capture an image and save it as a PNG file."""
        try:
            # Capture an image
            image_data = self.camera.capture_image()

            # Convert the image data to a format suitable for saving (e.g., numpy array)
            image_array = np.array(image_data, dtype=np.uint8)

            # Save the image as a PNG file
            image = Image.fromarray(image_array)
            image.save(self.image_filename)
            print(f"Image saved as {self.image_filename}")

        except Exception as e:
            print(f"An error occurred while capturing the image: {e}")

        finally:
            # Ensure the camera is properly disconnected
            self.camera.disconnect()
            print("Camera disconnected.")

if __name__ == "__main__":
    # Example usage of ThorlabsCameraAction
    action = ThorlabsCameraAction()
    action.setup(exposure_time=100, gain=1.5, image_filename='test_image.png')
    action.run()

