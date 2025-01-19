function refresh_token = get_refresh_token()
    % Step 1: Prompt the user for the Dropbox App Key
    appKey = input('Enter your Dropbox App Key: ', 's');

    % Step 2: Start the OAuth2 flow and generate the authorization URL
    authorizeUrl = sprintf('https://www.dropbox.com/oauth2/authorize?client_id=%s&response_type=code', appKey);
    
    % Step 3: Print authorization instructions
    fprintf('\n--- Authorization Steps ---\n');
    fprintf('1. Go to the following URL:\n%s\n', authorizeUrl);
    fprintf('2. Log in to your Dropbox account and click "Allow".\n');
    fprintf('3. Copy the authorization code provided on the page.\n');

    % Step 4: Prompt for the authorization code
    authCode = input('Enter the authorization code here: ', 's');

    % Step 5: Exchange the authorization code for an access token
    tokenUrl = 'https://api.dropboxapi.com/oauth2/token';
    tokenRequestBody = sprintf('code=%s&grant_type=authorization_code&client_id=%s&client_secret=%s', ...
        authCode, appKey, 'YOUR_APP_SECRET'); % Replace 'YOUR_APP_SECRET' with your actual app secret
    
    options = weboptions('MediaType', 'application/x-www-form-urlencoded', 'RequestMethod', 'post');
    
    try
        % Get the access token
        response = webwrite(tokenUrl, tokenRequestBody, options);
        accessToken = response.access_token;
        refreshToken = response.refresh_token; % Save this securely for future use

        % Step 6: Notify the user of successful authorization
        fprintf('\n--- Authorization Successful ---\n');
        fprintf('Access Token: %s\n', accessToken);
        fprintf('Refresh Token: %s\n', refreshToken); % Save securely for future use
        
    catch exception
        fprintf('\nError during authorization: %s\n', exception.message);
    end
end