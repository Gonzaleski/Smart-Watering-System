function imagePath = takePicture()
    % Set the directory where the images will be saved
    saveDir = '/home/aradskn/Pictures';
    
    % Ensure the save directory exists
    if ~exist(saveDir, 'dir')
        mkdir(saveDir);  % Create the directory if it doesn't exist
    end
    
    % Create a Raspberry Pi object
    rpi = raspi();  % Connect to the Raspberry Pi
    
    % Create a video input object for the camera
    cam = cameraboard(rpi);  % Use the camera board connected to the Raspberry Pi
    
    % Capture a still image
    try
        img = snapshot(cam);  % Take a snapshot from the camera
        % Generate a timestamped filename for the image
        timestamp = datestr(now, 'yyyymmdd_HHMMSS');
        filename = sprintf('image_%s.jpg', timestamp);  % Name the file with the timestamp
        imagePath = fullfile(saveDir, filename);  % Full path to save the image
        
        % Save the image to the specified file path
        imwrite(img, imagePath);  % Save the captured image
        
        % Print a success message with the saved file name
        fprintf('Picture saved locally as %s\n', filename);
    catch ME
        % Handle any exceptions that occur during the image capture process
        warning(ME.identifier, '%s', ME.message);
        imagePath = '';  % Return empty if an error occurs
    end
end
