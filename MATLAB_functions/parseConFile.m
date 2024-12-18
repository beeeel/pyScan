function metadata = parseConFile(conFileName)
% Parse the config file and handle nested actions
    fid = fopen(conFileName, 'r');
    if fid == -1
        error('Could not open the config file: %s', conFileName);
    end
    
    % Initialize metadata
    metadata = struct();
    metadata.numChunks = 1; % Default to 1 chunk unless specified
    actionStack = {}; % Stack to track nested actions
    
    try
        while ~feof(fid)
            line = strtrim(fgets(fid));
            if startsWith(line, 'action')
                % Start a new action
                actionType = sscanf(line, 'action %s');
                actionStack{end+1} = struct('type', actionType, 'params', struct(), 'numChunks', 1);
            elseif startsWith(line, 'end')
                % End the current action
                completedAction = actionStack{end};
                actionStack(end) = []; % Pop the stack
                
                if isempty(actionStack)
                    % Top-level action
                    metadata.action = completedAction;
                else
                    % Nested action
                    parentAction = actionStack{end};
                    if ~isfield(parentAction, 'nestedActions')
                        parentAction.nestedActions = {};
                    end
                    parentAction.nestedActions{end+1} = completedAction;
                    parentAction.numChunks = parentAction.numChunks * completedAction.numChunks;
                    actionStack{end} = parentAction;
                end
            elseif ~isempty(actionStack)
                % Parse parameters for the current action
                currentAction = actionStack{end};
                
                if startsWith(line, 'count')
                    currentAction.params.count = sscanf(line, 'count %d');
                    currentAction.numChunks = currentAction.params.count;
                elseif startsWith(line, 'scan')
                    scanParams = sscanf(line, 'scan %f %f %f');
                    startPos = scanParams(1);
                    endPos = scanParams(2);
                    stepSize = scanParams(3);
                    currentAction.params.scan = [startPos, endPos, stepSize];
                    currentAction.numChunks = numel(startPos:stepSize:endPos);
                elseif startsWith(line, 'channels')
                    tmp = strsplit(line,{'channels' ' '});
                    currentAction.params.channels = tmp(2:end);
                elseif startsWith(line, 'samples')
                    currentAction.params.samples = sscanf(line, 'samples %i');
                elseif startsWith(line, 'rate')
                    currentAction.params.rate = sscanf(line, 'rate %i');
                end
                
                actionStack{end} = currentAction;
            end
        end
        
        % Validate the final structure
        if isempty(metadata.action)
            error('No valid action found in the config file.');
        end
    catch ME
        fclose(fid);
        rethrow(ME);
    end
    fclose(fid);
end
