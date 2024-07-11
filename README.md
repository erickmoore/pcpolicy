# PCPOLICY

## Overview

PCPOLICY is a command line utility that allows for bulk updating of Prisma Cloud policies. It supports applying enable/disable actions, changing policy severities, and filtering policies based on various criteria.

## Installation

To install PCPOLICY, you need to have Python 3 and pip installed on your machine. You can install PCPOLICY using the following commands:

```sh
# Install build tools
python3 -m pip install --upgrade build

# Build the package
python3 -m build

# Install the package
pip install .
```

## Usage

After installing the package, you can use the `pcpolicy` command line tool to manage your Prisma Cloud policies.

### Basic Command Structure

```sh
pcpolicy [OPTIONS]
```

### Options

- `--apply`: Apply enable/disable for the selected policies.
- `--severity`: Specify the policy severity (required).
- `--new-severity`: Change the selected policy severity to one of `['critical', 'high', 'medium', 'low', 'informational']`.
- `--policy-subtype`: Filter policies by subtype (`['run', 'build', 'run_and_build', 'audit', 'data_classification', 'dns', 'malware', 'network_event', 'network', 'ueba', 'permissions', 'identity']`).
- `--cloud`: Filter policies by cloud provider (`['aws', 'azure', 'gcp', 'alibaba', 'oci']`).
- `--policy-enabled`: Find enabled policies.
- `--policy-disabled`: Find disabled policies.
- `--enable`: Enable the selected policies (mutually exclusive with `--disable`).
- `--disable`: Disable the selected policies (mutually exclusive with `--enable`).
- `--include`: Include policies by name (multiple values allowed).
- `--exclude`: Exclude policies by name (multiple values allowed).

### Examples

#### List policies with severity `high`

```sh
pcpolicy --severity high
```

#### Enable policies with severity `medium` and label `identity`

```sh
pcpolicy --severity medium --label identity --enable --apply
```

#### Change the severity of AWS policies with severity `high` to `medium`

```sh
pcpolicy --cloud aws --severity high --new-severity medium --apply
```

#### List policies for `aws` cloud with `run` subtype

```sh
pcpolicy --severity critical --cloud aws --policy-subtype run
```

#### Include and exclude specific policies by name

```sh
pcpolicy --severity high --include PolicyName1 --exclude PolicyName2
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss any changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.