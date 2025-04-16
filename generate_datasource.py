"""
This script generates Grafana datasource configurations for AWS CloudWatch and Amazon Managed Prometheus (AMP).

The script creates YAML configuration files that Grafana uses to connect to AWS services:
- CloudWatch for metrics and logs
- Amazon Managed Prometheus for Prometheus-compatible metrics

The configurations are written to the grafana/provisioning/datasources directory.

Environment Variables:
    AWS_REGION: The AWS region to use for service access
    AWS_PROFILE: The AWS profile to use for authentication

Dependencies:
    - pyyaml: For YAML file generation
    - subprocess: For executing AWS CLI commands
    - json: For parsing AWS CLI output
"""

import os
import yaml
import subprocess
import json

def generate_amazon_cloudwatch_datasource_yaml(aws_region: str, aws_profile: str) -> None:
    """Creates a Grafana datasource configuration for AWS CloudWatch.

    Args:
        aws_region (str): The AWS region to use for CloudWatch data access
        aws_profile (str): The AWS profile to use for authentication
    """
    # Template for the cloudwatch datasource configuration
    datasource_template = {
        "apiVersion": 1,
        "datasources": [
            {
                "name": "AWS CloudWatch",
                "type": "cloudwatch",
                "uid": "adtx6ipewqk1sd",
                "access": "proxy",
                "editable": True,
                "jsonData": {
                    "authType": "default",
                    "defaultRegion": aws_region,
                    "profile": aws_profile
                }
            }
        ]
    }

    # Write the YAML file
    output_path = "grafana/provisioning/datasources/cloudwatch.yml"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        yaml.dump(datasource_template, f, default_flow_style=False, sort_keys=False)


def generate_amazon_prometheus_datasource_yaml(aws_region: str, aws_profile: str, amp_workspace_url: str) -> None:
    """Creates a Grafana datasource configuration for Amazon Managed Prometheus (AMP).

    Args:
        aws_region (str): The AWS region where the AMP workspace is located
        aws_profile (str): The AWS profile to use for authentication
        amp_workspace_url (str): The URL of the AMP workspace to connect to

    """
    datasource_template = {
        "apiVersion": 1,
        "datasources": [
            {
                "name": "AWS-AMP (dta)",
                "type": "grafana-amazonprometheus-datasource",
                "uid": "adtx6ipewqk1sc",
                "access": "proxy",
                "editable": True,
                "url": amp_workspace_url,
                "isDefault": True,
                "jsonData": {
                    "sigV4Auth": True,
                    "sigV4AuthType": "default",
                    "sigV4Region": aws_region,
                    "sigV4Profile": aws_profile,
                    "manageAlerts": False,
                    "defaultEditor": "code"
                }
            }
        ]
    }

    # Write the YAML file
    output_path = "grafana/provisioning/datasources/prometheus.yml"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        yaml.dump(datasource_template, f, default_flow_style=False, sort_keys=False)

if __name__ == "__main__":
    # Get configuration from environment variables
    aws_region = os.getenv('AWS_REGION', 'us-east-1')
    aws_profile = os.getenv('AWS_PROFILE', 'default')

    # Execute tofu output command and parse JSON
    output = subprocess.check_output(['tofu', 'output', '--json'])
    amp_workspace_url = json.loads(output)['workspace_url']['value']
    
    if not amp_workspace_url:
        raise ValueError("AMP_WORKSPACE_URL environment variable is required")

    generate_amazon_prometheus_datasource_yaml(aws_region, aws_profile, amp_workspace_url)
    generate_amazon_cloudwatch_datasource_yaml(aws_region, aws_profile)
