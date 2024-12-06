function result = processAction(action, result, configFileName, context)
    % Default chunk multiplier
    chunkMultiplier = context.chunkMultiplier; 
    
    switch action.type
        case 'A2D'
            % Call A2D loader and include cumulative chunk multiplier
            [data, time] = load_a2d(action, configFileName, chunkMultiplier);
            if isempty(result.data)
                result.data = data;
                result.time = time;
            else
                result.data = cat(3, result.data, data);
            end
            
        case 'sleep'
            % Handle sleep (record metadata or timing)
            % result.additionalInfo{end+1} = handle_sleep(action);

        case 'count'
            % Update context with the repetition count
            newContext = context;
            newContext.chunkMultiplier = chunkMultiplier * action.params.count;

            % Process nested actions
            for nestedAction = action.nestedActions
                result = processAction(nestedAction{1}, result, configFileName, newContext);
            end

        case 'scan'
            % Compute the number of scan steps
            scanSteps = numel(action.params.scan(1):action.params.scan(3):action.params.scan(2));
            newContext = context;
            newContext.chunkMultiplier = chunkMultiplier * scanSteps;

            % Process nested actions
            for nestedAction = action.nestedActions
                result = processAction(nestedAction{1}, result, configFileName, newContext);
            end

        otherwise
            warning('Unknown action type: %s', action.type);
    end
end
