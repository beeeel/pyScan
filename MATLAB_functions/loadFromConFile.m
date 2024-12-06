function result = loadFromConFile(configFileName)
%% Parse the con file and load data 
% Input:
%   configFileName - Name of the config file (e.g., 'example.con')
% Output:
%   result - A struct containing metadata, time stamps, and data

% Parse the configuration file
metadata = parseConFile(configFileName);

% Extract the primary action
primaryAction = metadata.action;

% Initialize result
result = struct();
result.metadata = metadata;
result.data = [];
result.time = [];
result.additionalInfo = {}; % Store outputs of other actions like sleep

% Initialize context
context = struct('chunkMultiplier', 1); % Start with a default multiplier of 1

% Traverse actions and process
result = processAction(primaryAction, result, configFileName, context);



% % Parse the configuration file
% metadata = parseConFile(configFileName);
% 
% % Extract the primary action
% primaryAction = metadata.action;
% 
% % Define required fields for various action types
% requiredFields = {
%     {'A2D', {'channels', 'samples', 'rate'}}, 
%     {'scan', {'scan', 'axis'}}, 
%     {'count', {'count'}}
% };
% 
% % Validate all actions recursively
% validateAction(primaryAction, requiredFields);
% 
% % Compute numChunks
% numChunks = primaryAction.numChunks;
% 
% % Extract other metadata parameters
% numChannels = numel(primaryAction.params.channels);
% numSamples = primaryAction.params.samples;
% rate = primaryAction.params.rate;
% 
% % Preallocate the data array
% dataArray = zeros(numSamples, numChannels, numChunks);
% 
% % Process binary files (similar as before)
% for i = 1:numChannels
%     binaryFileName = sprintf('%s_channel%s.bin', ...
%                              configFileName(1:end-4), ...
%                              primaryAction.params.channels{i});
%     if ~isfile(binaryFileName)
%         error('Binary file not found: %s', binaryFileName);
%     end
% 
%     % Load binary data
%     rawData = binaryToDouble(binaryFileName);
% 
%     % Reshape and assign data
%     reshapedData = reshape(rawData, numSamples, numChunks);
%     dataArray(:, i, :) = reshapedData;
% end
% 
% % Create the result struct
% result = struct();
% result.metadata = metadata;
% result.time = (0:(numSamples - 1)) / rate; % Time vector
% result.data = dataArray; % Single 3D array

end
