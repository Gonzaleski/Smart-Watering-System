% Define channel ID for the soil moisture data
channelID = channel_id;

% Provide the ThingSpeak Alerts API Key (starts with 'TAK')
alertApiKey = 'alert_api_key';

% Set the URL for ThingSpeak Alerts API
alertUrl = "https://api.thingspeak.com/alerts/send";

% Add the required header for the Alerts API
options = weboptions("HeaderFields", ["ThingSpeak-Alerts-API-Key", alertApiKey]);

% Set the email subject
alertSubject = "Soil Moisture Alert";

% Read recent soil moisture data (Field 1) from the past 2 hours
moistureData = thingSpeakRead(channelID, 'NumDays', 30, 'Fields', 1);

% Check if data was retrieved successfully
if isempty(moistureData)
    fprintf("No data read from ThingSpeak. Skipping email notification.\n");
else
    % Get the most recent value of soil moisture
    lastValue = moistureData(end);

    % Check if the value is abnormal (below 30 or above 70)
    if lastValue < 30
        alertBody = sprintf("Soil moisture is too low (%.2f). Please water the plant.", lastValue);
    elseif lastValue > 70
        alertBody = sprintf("Soil moisture is too high (%.2f). Avoid overwatering.", lastValue);
    else
        % Value is normal; do not send any alert
        fprintf("Soil moisture is normal (%.2f). No alert sent.\n", lastValue);
        return; % Exit the script
    end

    % Send the alert if the value is abnormal
    try
        webwrite(alertUrl, "body", alertBody, "subject", alertSubject, options);
        fprintf("Alert sent successfully: %s\n", alertBody);
    catch someException
        fprintf("Failed to send alert: %s\n", someException.message);
    end
end

