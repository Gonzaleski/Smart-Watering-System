import dropbox
import os
from dotenv import load_dotenv

load_dotenv()

class DropboxUploader:
    def __init__(self):
        self.app_key = os.getenv("DROPBOX_APP_KEY")
        self.refresh_token = os.getenv("DROPBOX_REFRESH_TOKEN")
        self.client = self.get_dropbox_client()

    def get_dropbox_client(self):
        try:
            return dropbox.Dropbox(
                oauth2_refresh_token=self.refresh_token,
                app_key=self.app_key
            )
        except dropbox.exceptions.AuthError as e:
            print(f"Authentication error: {e}")
            return None

    def upload(self, local_path):
        if local_path is None:
            print("No local path provided for upload.")
            return
        try:
            with open(local_path, "rb") as file:
                dropbox_path = f"/{os.path.basename(local_path)}"
                self.client.files_upload(file.read(), dropbox_path)
                print(f"Uploaded {local_path} to Dropbox at {dropbox_path}")
        except Exception as e:
            print(f"Error uploading to Dropbox: {e}")
