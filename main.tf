terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.94.1"
    }
  }
}

provider "aws" {
  default_tags {
    tags = {
      Owner = "dnvriend"
      Project = "terraform-amazon-managed-prometheus"
    }
  }
}

# ----

resource "aws_cloudwatch_log_group" "prometheus_log_group" {
  name_prefix = "dnvriend-"
  retention_in_days = 1
  log_group_class = "STANDARD"
  skip_destroy = false
}

resource "aws_prometheus_workspace" "prometheus_workspace" {
  alias = "dnvriend-workspace"

  logging_configuration {
    log_group_arn = "${aws_cloudwatch_log_group.prometheus_log_group.arn}:*"
  }
}


output "workspace_url" {
  value = aws_prometheus_workspace.prometheus_workspace.prometheus_endpoint
}

output "workspace_alertmanager_url" {
  value = "${aws_prometheus_workspace.prometheus_workspace.prometheus_endpoint}alertmanager"
}

output "workspace_remote_write_url" {
  value = "${aws_prometheus_workspace.prometheus_workspace.prometheus_endpoint}api/v1/remote_write"
}


