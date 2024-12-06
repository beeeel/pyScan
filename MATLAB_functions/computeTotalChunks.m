function totalChunks = computeTotalChunks(action)
    if strcmp(action.type, 'A2D')
        totalChunks = 1; % Single chunk for A2D unless modified by parents
    elseif strcmp(action.type, 'count')
        totalChunks = action.params.count * sum(cellfun(@computeTotalChunks, action.nestedActions));
    elseif strcmp(action.type, 'scan')
        scanSteps = numel(action.params.scan(1):action.params.scan(3):action.params.scan(2));
        totalChunks = scanSteps * sum(cellfun(@computeTotalChunks, action.nestedActions));
    else
        totalChunks = 0; % Default for other actions
    end
end
