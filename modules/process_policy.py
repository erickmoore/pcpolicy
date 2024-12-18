import copy

def process_policy(row, options):
    """
    Process a single policy with given options.
    
    Args:
        row (dict): Policy data from DataFrame
        options (dict): Configuration options for processing
    
    Returns:
        dict: Updated policy information and processing results
    """
    
    # Extract policy details
    policy_details = {
        'name': row.get('name'),
        'policyId': row.get('policyId'),
        'status': row.get('enabled'),
        'severity': row.get('severity'),
        'labels': row.get('labels', []),
        'compliance': row.get('complianceMetadata', [])
    }
    
    is_last_label = False
        
    if options['compliance'] is not None:
        compliance_metadata = policy_details['compliance']
        if not isinstance(compliance_metadata, list):
            compliance_metadata = [compliance_metadata] if compliance_metadata is not None else []

        if not any(
            item.get('standardName') == options['compliance'] 
            for item in compliance_metadata
            if isinstance(item, dict)
        ):
            return None        
    
    # Create a copy of the policy to modify
    modified_policy = copy.deepcopy(policy_details)
    
    # Apply severity change
    if options['new_severity']:
        modified_policy['severity'] = options['new_severity']
        
    # Apply enable change
    if options['enable']:
        modified_policy['status'] = True
        
    # Apply enable change
    if options['disable']:
        modified_policy['status'] = False
    
    # Manage labels
    if options['new_label'] and options['new_label'] not in modified_policy['labels']:
        modified_policy['labels'].append(options['new_label'])
        
    if options['remove_label'] and options['remove_label'] in modified_policy['labels']:
        modified_policy['labels'] = [
            label for label in modified_policy['labels'] 
            if label != options['remove_label']
        ]
        is_last_label = len(modified_policy['labels']) == 0
        
    # Prepare processing result
    result = {
        'original': policy_details,
        'modified': modified_policy,
        'actions': [],
        'is_last_label': is_last_label
    }
    
    # Determine actions
    if options['enable'] and not policy_details['status']:
        result['actions'].append('enable')
    
    if options['disable'] and policy_details['status']:
        result['actions'].append('disable')
    
    if options['new_severity'] or options['new_label'] or options['remove_label']:
        result['actions'].append('update')
    
    return result