#!/usr/bin/env python3

import pandas as pd
import click
from modules.config import url, password, username
from modules.api import login, get_policies, apply_policies, get_compliance
from modules.messages import print_status, print_results, print_total, print_apply
from modules.arg_validator import MutuallyExclusiveOption, SeverityType
from modules.export import export_csv
from datetime import datetime
import json

@click.command()
@click.option('--apply', is_flag=True, help="Apply selected changes")
@click.option('--severity', type=SeverityType(), help=f"Policy severity, accepts: c: critical, h: high, m: medium, l: low, i: informational)")
@click.option('--new-severity', type=click.Choice(['critical', 'high', 'medium', 'low', 'informational']), help="Change selected policy severity")
@click.option('--policy-subtype', type=click.Choice(['run', 'build', 'run_and_build', 'audit', 'data_classification', 'dns', 'malware', 'network_event', 'network', 'ueba', 'permissions', 'identity']))
@click.option('--cloud', type=click.Choice(['aws', 'azure', 'gcp', 'alibaba', 'oci']))
@click.option('--policy-enabled', is_flag=True, help="Find enabled policies")
@click.option('--policy-disabled', is_flag=True, help="Find disabled policies")
@click.option('--enable', is_flag=True, cls=MutuallyExclusiveOption, mutually_exclusive=["disable"], help="Enable selected policies")
@click.option('--disable', is_flag=True, cls=MutuallyExclusiveOption, mutually_exclusive=["enable"], help="Disable selected policies")
@click.option('--include', multiple=True, type=str, help="Include policies by name")
@click.option('--exclude', multiple=True, type=str, help="Exclude policies by name")
@click.option('--list-compliance', is_flag=True, help="List compliance names")
@click.option('--policy-label', type=str, help="Match policies against a policy label")
@click.option('--new-label', type=str, help="Add a label to matched policies")
@click.option('--exclude-label', multiple=True, type=str, help="Exclude policies with this label")
@click.option('--compliance', type=str, help="Match policies against a compliance standard")
@click.option('--export', is_flag=True, cls=MutuallyExclusiveOption, mutually_exclusive=["apply"], help="Export results as a CSV")

def main(apply, severity, policy_subtype, cloud, policy_enabled, policy_disabled, enable, disable, include, exclude, new_severity, list_compliance, policy_label, new_label, exclude_label, compliance, export):
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    policy_status = None
    if policy_enabled: policy_status  = 'true'
    if policy_disabled: policy_status = 'false'
    
    policy_action = None
    if enable: policy_action  = 'enable'
    if disable: policy_action = 'disable'
    
    token = login(url, username, password)
    
    if list_compliance:
        compliance_standards = get_compliance(url, token)
        df = pd.DataFrame(compliance_standards)
        if include:
            df = df[df['name'].apply(lambda x: any(f in x for f in include))]
        if exclude:
            df = df[~df['name'].apply(lambda x: any(f in x for f in exclude))]
        for index, row in df.iterrows():
            compliance_name = row['name']
            print(compliance_name)
        return
        
    policies = get_policies(url, token, severity, policy_status, policy_subtype, cloud, policy_label)
    
    # Create Pandas DataFrame
    df = pd.DataFrame(policies)
    
    # column_names = df.columns.tolist()
    # print(column_names)
    
    # Filter DataFrame for policies that match applied filters
    if include:
        df = df[df['name'].str.lower().apply(lambda x: any(f.lower() in x for f in include))]
    if exclude:
        df = df[~df['name'].str.lower().apply(lambda x: any(f.lower() in x for f in exclude))]
    if exclude_label:
        df = df[~df['labels'].apply(lambda labels: 
        any(any(f.lower() in label.lower() for f in exclude_label) for label in labels)
    )]
    
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
        
        if compliance is None or (compliance_data is not None and isinstance(compliance_data, list) and any(item.get('standardName') == compliance for item in compliance_data)):

            if policy_status == True:
                enabled_count += 1
                
            if policy_status == False:
                disabled_count += 1
            
            if new_severity:
                policies[index]['severity'] = new_severity
                
            if new_label and new_label not in policies[index]['labels']:
                new_labels = policies[index]['labels'] + [new_label]
                policies[index]['labels'] = new_labels
                    
            if not apply:
                print_results(policy_name, policy_status, policy_action, policy_severity, new_severity, policy_labels, new_labels)
                
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
                if new_label:
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
    
    if enable or disable or new_severity or new_label:
        print("")
        print_apply(apply)
        print("")
        
    pass