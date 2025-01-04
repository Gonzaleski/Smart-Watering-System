import dropbox
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Class to handle Dropbox file uploads
class DropboxUploader:
    def __init__(self):
        """
        Initialize the DropboxUploader class.
        
        Loads the Dropbox app key and refresh token from environment variables
        and creates a Dropbox client for API interactions.
        """
        self.app_key = os.getenv("DROPBOX_APP_KEY")  # Get the Dropbox app key from environment
        self.refresh_token = os.getenv("DROPBOX_REFRESH_TOKEN")  # Get the refresh token
        self.client = self.get_dropbox_client()  # Initialize the Dropbox client

    def get_dropbox_client(self):
        """
        Create and authenticate a Dropbox client using the app key and refresh token.
        
        :return: Authenticated Dropbox client or None if authentication fails
        """
        try:
            # Return an authenticated Dropbox client
            return dropbox.Dropbox(
                oauth2_refresh_token=self.refresh_token,
                app_key=self.app_key
            )
        except dropbox.exceptions.AuthError as e:
            # Print an error message if authentication fails
            print(f"Authentication error: {e}")
            return None

    def upload(self, local_path):
        """
        Upload a file to Dropbox.
        
        :param local_path: The path of the file to upload
        """
        if local_path is None:
            # Check if the local file path is provided
            print("No local path provided for upload.")
            return
        try:
            # Open the local file in binary read mode
            with open(local_path, "rb") as file:
                # Define the path on Dropbox where the file will be uploaded
                dropbox_path = f"/{os.path.basename(local_path)}"
                # Upload the file to Dropbox
                self.client.files_upload(file.read(), dropbox_path)
                # Print a success message after upload
                print(f"Uploaded {local_path} to Dropbox at {dropbox_path}")
        except Exception as e:
            # Handle any exceptions that occur during the upload process
            print(f"Error uploading to Dropbox: {e}")
