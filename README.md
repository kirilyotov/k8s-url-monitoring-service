# URL Monitoring Service

A Python service that monitors external URLs and exposes metrics in Prometheus format.

## Features

- Monitors the status of external URLs
- Measures response time in milliseconds
- Exposes metrics in Prometheus format
- Packaged as a Docker container
- Deployable to Kubernetes using Helm

## Metrics

The service exposes the following metrics:

- `sample_external_url_up{url="<url>"}`: 1 if the URL is up (status code 200), 0 otherwise
- `sample_external_url_response_ms{url="<url>"}`: Response time in milliseconds

## Prerequisites

- Docker
- Kubernetes cluster
- Helm 3
- kubectl configured to access your cluster

## Deployment Steps

## 1. Build and Push the Docker Image or use the pre-built image `ghcr.io/kirilyotov/health-monitoring:latest`

## 2. Deploy the Prometheus Operator to Kubernetes

```bash
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo update
    helm install prometheus prometheus-community/kube-prometheus-stack
```

## 3. Deploy the URL Monitoring Service to Kubernetes

```bash
    helm install url-monitoring ./url-monitoring
```
