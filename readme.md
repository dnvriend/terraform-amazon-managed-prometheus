# terraform-amazon-managed-prometheus
A study project demonstrating the integration of Amazon Managed Prometheus (AMP) with Grafana and various AWS data sources.

## Overview

This project sets up a complete monitoring stack using:
- Amazon Managed Prometheus (AMP) for Prometheus-compatible metrics storage
- Grafana for visualization and dashboarding
- AWS CloudWatch integration for additional metrics and logs
- Terraform for infrastructure as code

## Prerequisites

- Python 3.13 or higher
- Terraform (or OpenTofu)
- AWS CLI configured with appropriate credentials
- Docker and Docker Compose

## Makefile Targets

The project includes a Makefile with the following targets:

- `help`: Shows all available targets and their descriptions
- `up`: Starts the Docker containers (requires `generate-datasources` first)
- `down`: Stops the Docker containers
- `restart`: Restarts the Docker containers (down followed by up)
- `logs`: Shows the Grafana container logs in follow mode
- `init`: Initializes the Terraform/OpenTofu configuration
- `apply`: Deploys the Amazon Managed Prometheus workspace
- `destroy`: Removes the Amazon Managed Prometheus workspace
- `generate-datasources`: Generates datasource configurations using Python
- `clean`: Removes the Grafana directory


## Resources
- https://github.com/aws/amazon-managed-service-for-prometheus-roadmap
- https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-onboard-query-standalone-grafana.html
- https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/
- https://grafana.com/docs/grafana/latest/explore/simplified-exploration/metrics/
- https://grafana.com/docs/grafana/latest/administration/provisioning/#datasources
