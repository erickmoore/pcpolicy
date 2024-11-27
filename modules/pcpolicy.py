#!/usr/bin/env python3

import pandas as pd
import click
from modules.options import get_click_options
from modules.config import url, password, username
from modules.api import login, get_policies, apply_policies, get_compliance
from modules.messages import print_status, print_results, print_total, print_apply
from modules.export import export_csv
from modules.filter_data import filter_column
from datetime import datetime
import json

@click.command()

def main(**kwargs):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
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
        
    policy_status = None
    if policy_enabled: policy_status  = 'true'
    if policy_disabled: policy_status = 'false'
    
    policy_action = None
    if enable: policy_action  = 'enable'
    if disable: policy_action = 'disable'
    
    match_function = all if matchall == True else any

    token = login(url, username, password)
    
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

    # Set policy count to zero before parsing data
    total_count     = 0
    enabled_count   = 0
    disabled_count  = 0
    
    # Loop through policies from Pandas DataFrame
    for index, row in df.iterrows():
        policy_name     = row.get('name', None)
        policy_id       = row.get('policyId', None)
        policy_status   = row.get('enabled', None)
        policy_severity = row.get('severity', None)
        compliance_data = row.get('complianceMetadata', None)
        policy_labels   = row.get('labels', None)
        
        total_count += 1
        new_labels  = []
        last_label  = False
        
        if compliance is None or (compliance_data is not None and isinstance(compliance_data, list) and match_function(item.get('standardName') == compliance for item in compliance_data)):

            if policy_status == True:
                enabled_count += 1
                
            if policy_status == False:
                disabled_count += 1
            
            if new_severity:
                policies[index]['severity'] = new_severity
                
            if new_label and new_label not in policies[index]['labels']:
                new_labels = policies[index]['labels'] + [new_label]
                policies[index]['labels'] = new_labels
                
            if remove_label and remove_label in policies[index]['labels']:
                new_labels = [label for label in policies[index]['labels'] if label != remove_label]
                policies[index]['labels'] = new_labels
                if new_labels == []:
                    last_label = True
                
            if not apply:
                print_results(policy_name, policy_status, policy_action, policy_severity, new_severity, policy_labels, new_labels, last_label)
                
                if export:
                    filename = f"before_change_{timestamp}.csv"
                    export_csv(filename, [policy_name, policy_id, policy_status, policy_severity, policy_labels])
            
            if apply:
                if enable:
                    action      = "enable"
                    status_code = apply_policies(url, token, policy_action, policy_id)
                if disable:
                    action      = "disable"
                    status_code = apply_policies(url, token, policy_action, policy_id)
                if new_severity:
                    action      = "severity"
                    payload     = json.dumps(policies[index])
                    status_code = apply_policies(url, token, policy_action, policy_id, payload)
                if new_label or remove_label:
                    action      = "label"
                    payload     = json.dumps(policies[index])
                    status_code = apply_policies(url, token, policy_action, policy_id, payload)
                
                if status_code == 200:
                    if action == "enable":
                        policy_status = "true"
                    if action == "disable":
                        policy_status = "false"
                    if action == "severity":
                        policy_severity = new_severity               
                    if action == "label":
                        policy_labels = new_labels                

                    filename = f"success_{action}_{timestamp}.csv"
                    export_csv(filename, [policy_name, policy_id, policy_status, policy_severity, policy_labels])
                    print_status(status_code, policy_name)
                    
                if status_code == 400:
                    filename = f"failed_{action}_{timestamp}.csv"
                    export_csv(filename, [policy_name, policy_id, policy_status, policy_severity, policy_labels])
                    print_status(status_code, policy_name)
            
    print_total(total_count, enabled_count, disabled_count, severity, policy_subtype)
    
    if enable or disable or new_severity or new_label or remove_label:
        print("")
        print_apply(apply)
        print("")
        
    pass

for option in get_click_options():
    main = option(main)