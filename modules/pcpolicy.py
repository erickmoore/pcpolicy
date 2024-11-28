#!/usr/bin/env python3

import pandas as pd
import click
from modules.options import get_click_options
from modules.config import url, password, username
from modules.api import login, get_policies, apply_policies, get_compliance
from modules.messages import print_status, print_results, print_total, print_whatif_apply
from modules.export import export_csv
from modules.filter_data import filter_column
from modules.process_policy import process_policy
from datetime import datetime
import json

@click.command()

def main(**kwargs):
    timestamp     = datetime.now().strftime('%Y%m%d_%H%M%S')
    policy_status = None
    policy_action = None
    
    apply           = kwargs.get('apply', False)
    cloud           = kwargs.get('cloud')
    compliance      = kwargs.get('compliance')
    disable         = kwargs.get('disable', False)
    enable          = kwargs.get('enable', False)
    exclude         = kwargs.get('exclude')
    exclude_label   = kwargs.get('exclude_label')
    export          = kwargs.get('export', False)
    include         = kwargs.get('include')
    include_label   = kwargs.get('include_label')
    list_compliance = kwargs.get('list_compliance', False)
    matchall        = kwargs.get('matchall', False)
    new_label       = kwargs.get('new_label')
    new_severity    = kwargs.get('new_severity')
    policy_disabled = kwargs.get('policy_disabled')
    policy_enabled  = kwargs.get('policy_enabled')
    policy_subtype  = kwargs.get('policy_subtype')
    remove_label    = kwargs.get('remove_label')
    severity        = kwargs.get('severity')
        
    
    if policy_enabled: policy_status  = 'true'
    if policy_disabled: policy_status = 'false'
    
    if enable: policy_action  = 'enable'
    if disable: policy_action = 'disable'
    
    # Adjust filter match criteria
    match_function = all if matchall == True else any

    # Make API call to get auth token
    token = login(url, username, password)
    
    # Make API Call to get compliance policies if --list-compliance is selected
    if list_compliance:
        compliance_standards = get_compliance(url, token)
        df = pd.DataFrame(compliance_standards)
        if include:
            df = filter_column(df, 'name', include, match_function)
        if exclude:
            df = filter_column(df, 'name', exclude, match_function, exclude=True)
        for index, row in df.iterrows():
            compliance_name = row['name']
            print(compliance_name)
        return
    
    # Make API call to get policies passing API filters
    policies = get_policies(url, token, severity, policy_status, policy_subtype, cloud, include_label)
    
    # Create Pandas DataFrame
    df = pd.DataFrame(policies)

    # Filter data
    if include:
        df = filter_column(df, 'name', include, match_function)
    if exclude:
        df = filter_column(df, 'name', exclude, match_function, exclude=True)
    if include_label:
        df = filter_column(df, 'labels', include_label, match_function)
    if exclude_label:
        df = filter_column(df, 'labels', exclude_label, match_function, exclude=True)

    # Policy modification options
    options = {
        'apply': apply,
        'compliance': compliance,
        'enable': enable,
        'disable': disable,
        'new_severity': new_severity,
        'new_label': new_label,
        'remove_label': remove_label
    }

    # Set policy count to zero before parsing data
    processed_policies = []
    total_count     = 0
    enabled_count   = 0
    disabled_count  = 0
    
    for _, row in df.iterrows():
        policy_result = process_policy(row, options)
        
        if policy_result is None:
            continue
        
        total_count += 1
        
        # Count enabled/disabled statuses
        if policy_result['original']['status']:
            enabled_count += 1
        else:
            disabled_count += 1
        
        # Print or apply changes based on configuration
        if not apply:
            print_results(
                policy_result['original']['name'], 
                policy_result['original']['status'], 
                None,  # action 
                policy_result['original']['severity'], 
                policy_result['modified']['severity'], 
                policy_result['original']['labels'], 
                policy_result['modified']['labels'],
                policy_result.get('is_last_label', False)
            )
        
        if apply:
            for action in policy_result['actions']:
                status_code = apply_policies(url, token, action, policy_result['original']['policyId'])
                print_status(status_code, policy_result['original']['name'])
                pass
        
        processed_policies.append(policy_result)
    
    print_total(total_count, enabled_count, disabled_count, severity, policy_subtype)
    
    if enable or disable or new_severity or new_label or remove_label:
        print_whatif_apply(apply)
        
    pass

for option in get_click_options():
    main = option(main)