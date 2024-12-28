import os
import datetime
from picamera2 import Picamera2

class PicameraHandler:
    def __init__(self, save_dir):
        self.save_dir = save_dir
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_still_configuration(main={"size": (3280, 2464)}))

    def take_picture(self):
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"image_{timestamp}.jpg"
            filepath = os.path.join(self.save_dir, filename)
            self.picam2.start()
            self.picam2.capture_file(filepath)
            self.picam2.stop()
            print(f"Picture saved locally as {filename}")
            return filepath
        except Exception as e:
            print("Error taking picture:", e)
            return None
