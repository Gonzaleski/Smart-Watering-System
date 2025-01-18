% ThingSpeakSender.m
classdef ThingSpeakSender
    properties
        APIKey
        BaseURL
    end
    
    methods
        function obj = ThingSpeakSender(apiKey)
            obj.APIKey = apiKey;
            obj.BaseURL = 'https://api.thingspeak.com/update';
        end
        
        function response = sendData(obj, field1, field2, field3, field4)
            % Create payload
            data = struct('api_key', obj.APIKey, 'field1', field1, 'field2', field2, 'field3', field3, 'field4', field4);
            
            % Send POST request
            response = webwrite(obj.BaseURL, data);
        end
    end
end