# PC Policy

## Overview

`pcpolicy` is a command line utility that allows for bulk updating of Prisma Cloud policies. It supports applying enable/disable actions, changing policy severities, and filtering policies based on various criteria.

## Requirements

This script currently uses environment variables to authenticate against Prisma Cloud. In the future this may be changed to another method, but currently it is required to have the following 3 settings added as environment variables on the machine where you run the script.

 | name |  setting  | type | description |
 |----|-----------|------|-------------|
 | PRISMA_CLOUD_URL | Prisma Cloud Base URL | `string` | Your Prisma Cloud app stack URL in the format: https://app.prismacloud.io 
 | PRISMA_CLOUD_IDENTITY | Prisma Cloud Identity | `string` | Username or access key with the ability to view and modify policy.
 | PRISMA_CLOUD_SECRET | Prisma Cloud Secret | `string` | Password for username or access key above

## Installation

To install `pcpolicy`, you need to have Python 3 and pip installed on your machine. You can install `pcpolicy` using the following commands:

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

- `--apply`: Apply selected changes.
- `--severity`: Specify the policy severity (required) to one of `[c: critical, h: high, m: medium, l: low, i: informational]`.
- `--new-severity`: Change the selected policy severity to one of `['critical', 'high', 'medium', 'low', 'informational']`.
- `--policy-subtype`: Filter policies by subtype (`['run', 'build', 'run_and_build', 'audit', 'data_classification', 'dns', 'malware', 'network_event', 'network', 'ueba', 'permissions', 'identity']`).
- `--cloud`: Filter policies by cloud provider (`['aws', 'azure', 'gcp', 'alibaba', 'oci']`).
- `--list-compliance`: List all compliance standard names.
- `--compliance`: Find policies associated with a compliance standard.
- `--policy-enabled`: Find enabled policies.
- `--policy-disabled`: Find disabled policies.
- `--enable`: Enable the selected policies (mutually exclusive with `--disable`).
- `--disable`: Disable the selected policies (mutually exclusive with `--enable`).
- `--include`: Include policies by name (multiple values allowed).
- `--exclude`: Exclude policies by name (multiple values allowed).
- `--export`: Export results as a CSV.

<br>

> [!IMPORTANT]
> All options that make changes to policy require `--apply` to be added to the command.
> This is done to prevent accidental modification of policies.

<br>

---

### Examples

##### List disabled policies with severity `high`

```sh
pcpolicy --severity high --policy-disabled
```

##### Enable policies with severity `medium` of type `build`

```sh
pcpolicy --severity medium  --policy-subtype build --enable --apply
```

##### Change the severity of AWS policies with severity `high` to `medium`

```sh
pcpolicy --cloud aws --severity high --new-severity medium --apply
```

##### List policies for `Azure` cloud with `run` subtype

```sh
pcpolicy --severity critical --cloud azure --policy-subtype run
```

##### Find all disabled medium (m) severity runtime policies that include the word 'public'

```sh
pcpolicy --severity m --policy-disabled --policy-subtype run --include public
```

##### List all compliance standards that include the word 'PCI'

```sh
pcpolicy --list-compliance --include PCI
```

##### List all disabled policies for the 'PCI DSS v4.0' compliance standard

```sh
pcpolicy --compliance 'PCI DSS v4.0' --policy-disabled
```

<br>

---

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss any changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.