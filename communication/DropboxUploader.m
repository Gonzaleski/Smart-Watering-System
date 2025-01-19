classdef DropboxUploader
    properties
        appKey
        refreshToken
        client
    end

    methods
        function obj = DropboxUploader(appKey, refreshToken)
            obj.appKey = appKey;  % Get the Dropbox app key
            obj.refreshToken = refreshToken;  % Get the refresh token
            obj.client = obj.get_dropbox_client();  % Initialize the Dropbox client
        end

        function client = get_dropbox_client(obj)
            try
                % Return an authenticated Dropbox client
                client = dropbox.Dropbox( ...
                    'oauth2_refresh_token', obj.refreshToken, ...
                    'app_key', obj.appKey);
            catch ME
                warning(ME.identifier, 'Error during Dropbox authentication: %s', ME.message);
                client = [];
            end
        end

        function upload(obj, localPath)
            if isempty(localPath)
                fprintf('No local path provided for upload.\n');
                return;
            end
            try
                % Open the local file in binary read mode
                fileID = fopen(localPath, 'rb');
                data = fread(fileID, '*uint8');
                fclose(fileID);

                % Define the path on Dropbox where the file will be uploaded
                dropboxPath = strcat('/', erase(localPath, ' '));  % Remove spaces
                % Upload the file to Dropbox
                obj.client.files_upload(data, dropboxPath);
                fprintf('Uploaded %s to Dropbox at %s\n', localPath, dropboxPath);
            catch ME
                fprintf('Error uploading to Dropbox: %s\n', ME.message);
            end
        end
    end
end
