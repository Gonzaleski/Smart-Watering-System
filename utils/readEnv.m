function envVars = readEnv(filePath)
    % Reads a .env file and returns a structure with key-value pairs
    if nargin < 1
        filePath = '.env'; % Default file path
    end

    % Initialize the structure to hold environment variables
    envVars = struct();

    % Open and read the .env file
    if isfile(filePath)
        fid = fopen(filePath, 'r');
        while ~feof(fid)
            line = fgetl(fid); % Read line as a character array
            line = strtrim(line); % Remove whitespace from both ends
            if startsWith(line, '#') || isempty(line)
                continue; % Skip comments and empty lines
            end
            keyValue = regexp(line, '=', 'split'); % Split using '='
            if numel(keyValue) == 2
                key = strtrim(keyValue{1});
                value = strtrim(keyValue{2});
                envVars.(key) = value; % Add key-value pair to the structure
            end
        end
        fclose(fid);
    else
        error('Environment file "%s" not found.', filePath);
    end
end
