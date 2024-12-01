
from colorama import Fore, Style, init

init(autoreset=True)

# /////////////// Print Status
def print_status(status_code, policy_name):
    if status_code == 200:
        print(f"{Fore.GREEN}SUCCESS{Style.RESET_ALL}: {policy_name}")
    if status_code == 400:
        print(f"{Fore.RED}400 Failed to Enable{Style.RESET_ALL}: {policy_name}")
        
        
        
def print_results(policy_result, options):
    original = policy_result['original']
    modified = policy_result['modified']

    if original['status'] == True:
        print(f"{Fore.GREEN}ENABLED: {Style.RESET_ALL}{original['name']}")
    if original['status'] == False:
        print(f"{Fore.RED}DISABLED: {Style.RESET_ALL}{original['name']}")

    # Status change handling
    if options['enable'] or options['disable']:
        if original['status'] != modified['status']:
            color = Fore.GREEN if modified['status'] else Fore.RED
            status_text = "WILL ENABLE" if modified['status'] else "WILL DISABLE"
            print(f"{color}{status_text}: {original['name']}")
        else:
            color = Fore.LIGHTBLUE_EX
            status_text = "NO CHANGE"
            print(f"{color}{status_text}: {original['name']}")
    
    # Severity change handling
    if options['new_severity']:
        current_severity = severity_color(original['severity'])
        proposed_severity = severity_color(modified['severity'])
        if original['severity'] != modified['severity']:
            print(f"{Fore.GREEN}WILL CHANGE SEVERITY{Style.RESET_ALL}: {current_severity} {Style.RESET_ALL}to {proposed_severity}")
        else:
            print(f"{Fore.LIGHTBLUE_EX}NO CHANGE{Style.RESET_ALL}: {current_severity} {Style.RESET_ALL}to {proposed_severity}")
    
    # Label change handling
    label_changed = (options['new_label'] or options['remove_label']) and \
                    (original['labels'] != modified['labels'] or policy_result.get('is_last_label', False))
    
    if label_changed:
        new_labels = '[]' if policy_result.get('is_last_label', False) else modified['labels']
        print(f"{Fore.GREEN}WILL CHANGE LABELS{Style.RESET_ALL}: {Fore.LIGHTRED_EX}{original['labels']} {Style.RESET_ALL}to {Fore.GREEN}{new_labels}")
    
            
# /////////////// Print Totals  
def print_total(total_count, enabled_count, disabled_count, severity, policy_subtype):
    severity_text = severity_color(severity)
        
    print('')
    if enabled_count > 0:
        print(f"Total enabled {severity_text}{Style.RESET_ALL} policies: {enabled_count}")
    if disabled_count > 0:
            print(f"Total disabled {severity_text}{Style.RESET_ALL} policies: {disabled_count}")
    if enabled_count > 0 and disabled_count > 0:
        print(f"{Fore.CYAN}Total matched policies: {Style.RESET_ALL}{total_count}")
    
# /////////////// Print Apply    
def print_whatif_apply(apply):
    if not apply:
        print("")
        print(f"{Fore.LIGHTMAGENTA_EX}To apply config re-run the same command with: --apply")
        print(f"{Fore.LIGHTBLUE_EX}To save the existing config to a csv file re-run the same command with: --export")
        
# /////////////// Set severity color
def severity_color(severity):       
    if severity == 'critical': 
        severity_text = Fore.RED + severity + " priority" + Fore.CYAN
    if severity == 'high': 
        severity_text = Fore.LIGHTRED_EX + severity + " priority" + Fore.CYAN
    if severity == 'medium': 
        severity_text = Fore.YELLOW + severity + " priority" + Fore.CYAN
    if severity == 'low': 
        severity_text = Fore.BLUE + severity + " priority" + Fore.CYAN
    if severity == 'informational': 
        severity_text = Fore.LIGHTWHITE_EX + severity + " priority" + Fore.CYAN
    if severity == None: 
        severity_text = ""
        
    return severity_text