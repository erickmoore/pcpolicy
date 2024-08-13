
from colorama import Fore, Style, init

init(autoreset=True)

# /////////////// Print Status
def print_status(status_code, policy_name):
    if status_code == 200:
        print(f"{Fore.GREEN}SUCCESS{Style.RESET_ALL}: {policy_name}")
    if status_code == 400:
        print(f"{Fore.RED}400 Failed to Enable{Style.RESET_ALL}: {policy_name}")
        
# /////////////// Print Results        
def print_results(policy_name, policy_status, policy_action, policy_severity, new_severity):
    if policy_status == True:
        if policy_action == 'enable':
            print(f"{Fore.YELLOW}NO CHANGE: {Style.RESET_ALL}{policy_name}")
        if policy_action =='disable':
            print(f"{Fore.RED}WILL DISABLE: {Style.RESET_ALL}{policy_name}")
        if not policy_action:   
         print(f"{Fore.GREEN}ENABLED: {Style.RESET_ALL}{policy_name}")
        
    if policy_status == False:
        if policy_action == 'disable':
            print(f"{Fore.YELLOW}NO CHANGE: {Style.RESET_ALL}{policy_name}")
        if policy_action =='enable':
            print(f"{Fore.GREEN}WILL ENABLE: {Style.RESET_ALL}{policy_name}")
        if not policy_action:   
         print(f"{Fore.LIGHTRED_EX}DISABLED: {Style.RESET_ALL}{policy_name}")
         
    if new_severity:
        current_severity = severity_color(policy_severity)
        proposed_severity = severity_color(new_severity)
        print(f"{Fore.LIGHTRED_EX}WILL CHANGE{Style.RESET_ALL}: {current_severity}{Style.RESET_ALL} to {proposed_severity}")
        
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
def print_apply(apply):
    if not apply:
        print(f"{Fore.LIGHTMAGENTA_EX}To apply config re-run the same command with: --apply")
        
# /////////////// Set severity color
def severity_color(severity):
    if severity == 'critical': 
        severity_text = Fore.RED + severity + " priority" + Fore.CYAN
    if severity == 'high': 
        severity_text = Fore.LIGHTRED_EX + severity + " priority" + Fore.CYAN
    if severity == 'medium': 
        severity_text = Fore.LIGHTYELLOW_EX + severity + " priority" + Fore.CYAN
    if severity == 'low': 
        severity_text = Fore.YELLOW + severity + " priority" + Fore.CYAN
    if severity == 'informational': 
        severity_text = Fore.BLUE + severity + " priority" + Fore.CYAN
    if severity == None: 
        severity_text = ""
        
    return severity_text