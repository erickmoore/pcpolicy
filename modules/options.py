import click
from modules.arg_validator import MutuallyExclusiveOption, SeverityType

def get_click_options():
    return [
        click.option('--apply', is_flag=True, help="Apply selected changes"),
        click.option('--cloud', type=click.Choice(['aws', 'azure', 'gcp', 'alibaba', 'oci'])),
        click.option('--compliance', type=str, help="Match policies against a compliance standard"),
        click.option('--disable', is_flag=True, cls=MutuallyExclusiveOption, mutually_exclusive=["enable"], help="Disable selected policies"),
        click.option('--enable', is_flag=True, cls=MutuallyExclusiveOption, mutually_exclusive=["disable"], help="Enable selected policies"),
        click.option('--exclude', multiple=True, type=str, help="Exclude policies by name"),
        click.option('--exclude-label', multiple=True, type=str, help="Exclude policies with matching label name"),
        click.option('--export', is_flag=True, cls=MutuallyExclusiveOption, mutually_exclusive=["apply"], help="Export results as a CSV"),
        click.option('--include', multiple=True, type=str, help="Include policies by name"),
        click.option('--include-label', type=str, help="Include policies with matching label name"),
        click.option('--list-compliance', is_flag=True, help="List compliance names"),
        click.option('--matchall', is_flag=True, help="Match all filters instead of any filter"),
        click.option('--new-label', type=str, help="Add a label to matched policies"),
        click.option('--new-severity', type=click.Choice(['critical', 'high', 'medium', 'low', 'informational']), help="Change selected policy severity"),
        click.option('--policy-disabled', is_flag=True, help="Find disabled policies"),
        click.option('--policy-enabled', is_flag=True, help="Find enabled policies"),
        click.option('--policy-subtype', type=click.Choice(['run', 'build', 'run_and_build', 'audit', 'data_classification', 'dns', 'malware', 'network_event', 'network', 'ueba', 'permissions', 'identity'])),
        click.option('--remove-label', type=str, help="Remove label to matched policies"),
        click.option('--severity', type=SeverityType(), help=f"Policy severity, accepts: c: critical, h: high, m: medium, l: low, i: informational)"),
    ]