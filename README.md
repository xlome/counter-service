# Counter Service Application

## Overview

This Nano Service is a simple Python web application designed to demonstrate web development, deployment, and CI/CD principles.
It increments a counter stored in a local database each time it receives a POST request and returns the current count with a GET request.
The application uses a SQLite database for demonstration purposes, with data persistently stored on the local file system of the provided EC2 instance.

##### CI/CD Pipeline

The project integrates a CI/CD pipeline built with Azure Pipelines that automates the building, pushing, and deployment processes:

1. **Build and Push**: The pipeline triggers on commits to the main branch, building the Docker image and pushing it to Docker Hub's container registry.
2. **Deploy**: Deploys the container to a specified EC2 host using Ansible, pulling the latest image from Docker Hub.
3. **Health Check**: After deployment, the pipeline performs a simple health check to ensure the service is running as expected (In real life we should also report this issue and/or rollback to a previous stable version)

#### Production Considerations Implemented in This Task
- Docker service starts automatically when the instance starts
- Automatic Container Restarts and health checks
- Configuration Management: Ensuring the EC2 instance is set up with the necessary software and configurations required for the service to run.
- Infrastructure as Code: To create a new instance of the service or deploy it to a new environment, we can add another host to Ansible configuration (with respective changes in the pipeline). -
- Azure Secret Variables and Secure Files: Integrated Azure Pipelines' secret variables and secure file features to securely manage and utilize sensitive information, such as PEM keys for SSH access.

#### Suggestions for Production Enhancement

- Database: For real-world applications, we should use a cloud-hosted database service to keep the data persistent, we can also utilize a faster DB such as Redis in case timing is crucial.
- Monitoring and Alerts: Integrating the service with monitoring tools (e.g., Prometheus, Datadog) and setting up alerting based on metrics can help quickly identify and respond to crashes or degradation in service performance.
- Scalability: Orchestration tools like Kubernetes can help manage the service's lifecycle, including automated deployments, scaling, and self-healing after crashes.

Note - On CentOS hosts, we need to adjust SELinux policies to allow Docker containers access to necessary resources (should not be required when not mounting a volume, for a db in this case).