function [dataArray, time] = load_a2d(action, configFileName, chunkMultiplier)
    numChannels = numel(action.params.channels);
    numSamples = action.params.samples;
    numChunks = chunkMultiplier; % Total chunks determined by parent actions

    % Preallocate the data array
    dataArray = zeros(numSamples, numChannels, numChunks);

    % Load binary files
    for i = 1:numChannels
        binaryFileName = sprintf('%s_channel%s.bin', ...
                                 configFileName(1:end-4), ...
                                 action.params.channels{i});
        if ~isfile(binaryFileName)
            error('Binary file not found: %s', binaryFileName);
        end

        % Load binary data
        rawData = binaryToDouble(binaryFileName);

        % Reshape and store
        reshapedData = reshape(rawData, numSamples, numChunks);
        dataArray(:, i, :) = reshapedData;
    end

    % Create the time vector (for a single chunk)
    time = (0:(numSamples - 1)) / action.params.rate;
end
