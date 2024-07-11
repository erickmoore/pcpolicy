from click import Option, UsageError
import click

class MutuallyExclusiveOption(Option):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop('mutually_exclusive', []))
        help = kwargs.get('help', '')
        if self.mutually_exclusive:
            ex_str = ', '.join(self.mutually_exclusive)
            kwargs['help'] = help + (
                ' NOTE: This argument is mutually exclusive with '
                ' arguments: [' + ex_str + '].'
            )
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(
                    self.name,
                    ', '.join(self.mutually_exclusive)
                )
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(
            ctx,
            opts,
            args
        )
        
class SeverityType(click.ParamType):
    name = "severity"
    
    def __init__(self):
        self.abbreviations = {
            'c': 'critical',
            'h': 'high',
            'm': 'medium',
            'l': 'low',
            'i': 'informational'
        }

    def convert(self, value, param, ctx):
        # Try to fetch from abbreviation dictionary
        if value in self.abbreviations:
            return self.abbreviations[value]
        # Check if it is already a valid severity level
        if value in self.abbreviations.values():
            return value
        self.fail(f"{value!r} is not a valid severity level", param, ctx)
