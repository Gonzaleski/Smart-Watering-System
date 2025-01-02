from dropbox import DropboxOAuth2FlowNoRedirect
import sys

# Prompting the user to enter their Dropbox App Key via the terminal
APP_KEY = input("Enter your Dropbox App Key: ").strip()

# Initializing the Dropbox OAuth2 flow with PKCE (Proof Key for Code Exchange) for added security
# token_access_type='offline' ensures that a refresh token is issued
auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, use_pkce=True, token_access_type='offline')

# Generate the authorization URL where the user will allow access to their Dropbox account
authorize_url = auth_flow.start()

# Printing the instructions for the user to complete the authorization process
print("\n--- Authorization Steps ---")
print("1. Go to the following URL:")
print(authorize_url)
print("2. Log in to your Dropbox account and click 'Allow'.")
print("3. Copy the authorization code provided on the page.\n")

# Prompt the user to enter the authorization code from the Dropbox authorization page
auth_code = input("Enter the authorization code here: ").strip()

# Try to complete the OAuth2 process and fetch the tokens
try:
    # Finish the authorization process and retrieve the OAuth result
    oauth_result = auth_flow.finish(auth_code)
    
    # Print the access token and refresh token
    print("\n--- Authorization Successful ---")
    print("Access Token:", oauth_result.access_token)
    print("Refresh Token:", oauth_result.refresh_token)  # Save this securely for future use
except Exception as e:
    # Handle errors during the authorization process
    print(f"\nError during authorization: {e}")
