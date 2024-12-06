function validateAction(action, requiredFields)
    % Find the required fields for the current action type
    actionType = action.type;
    matchedField = find(cellfun(@(x) strcmp(x{1}, actionType), requiredFields), 1);
    
    if ~isempty(matchedField)
        % Get the required fields for the matched action type
        fieldsToCheck = requiredFields{matchedField}{2};
        
        % Validate required fields
        for field = fieldsToCheck
            if ~isfield(action.params, field{1})
                error('Config file is missing required field for %s: %s', actionType, field{1});
            end
        end
    end

    % If there are nested actions, validate them recursively
    if isfield(action, 'nestedActions')
        for nestedAction = action.nestedActions
            validateAction(nestedAction{1}, requiredFields); % Recursive call
        end
    end
end