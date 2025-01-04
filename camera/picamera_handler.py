import os
import datetime
from picamera2 import Picamera2

# Class to handle Picamera2 operations
class PicameraHandler:
    def __init__(self, save_dir):
        """
        Initialize the PicameraHandler class.
        
        :param save_dir: Directory where images will be saved
        """
        self.save_dir = save_dir  # Directory to save the images
        self.picam2 = Picamera2()  # Initialize the Picamera2 instance
        # Configure the camera for still image capture with specific resolution
        self.picam2.configure(self.picam2.create_still_configuration(main={"size": (3280, 2464)}))

    def take_picture(self):
        """
        Capture a still image using Picamera2.
        
        :return: The file path of the saved image, or None if an error occurs
        """
        try:
            # Generate a timestamped filename for the image
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"image_{timestamp}.jpg"  # Name the file with the timestamp
            filepath = os.path.join(self.save_dir, filename)  # Full path to save the image
            
            # Start the camera
            self.picam2.start()
            # Capture the image and save it to the specified file path
            self.picam2.capture_file(filepath)
            # Stop the camera after capturing the image
            self.picam2.stop()
            
            # Print a success message with the saved file name
            print(f"Picture saved locally as {filename}")
            return filepath  # Return the path of the saved image
        except Exception as e:
            # Handle any exceptions that occur during the image capture process
            print("Error taking picture:", e)
            return None  # Return None if an error occurs
