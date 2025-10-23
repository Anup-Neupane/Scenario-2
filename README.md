# 🚀 Jenkins CI/CD on Kubernetes with Kaniko, Trivy & ArgoCD

A comprehensive guide to setting up a complete cloud-native CI/CD pipeline using Jenkins on Kubernetes with secure container image building, vulnerability scanning, and GitOps-based deployment.

---

## 📋 Overview

This guide explains how to set up Jenkins in Kubernetes and configure a complete CI/CD pipeline that builds, tests, scans, and deploys applications securely using modern cloud-native tools:

- **Jenkins** — CI/CD orchestrator
- **Kaniko** — Secure Docker image builds in Kubernetes
- **Trivy** — Container vulnerability scanning
- **ArgoCD** — GitOps-based deployment
- **Docker Hub** — Container registry
- **GitHub** — Source code and manifests

---

## 📦 Prerequisites

Before starting, ensure you have the following:

- ✅ A running Kubernetes cluster (EKS, AKS, GKE, or Minikube)
- ✅ `kubectl` configured for the cluster
- ✅ Docker Hub account
- ✅ GitHub repository with application source code and a `deployment.yaml`
- ✅ ArgoCD set up and connected to your app repo (optional for GitOps)

---

## ⚙️ Deploy Jenkins in Kubernetes

### Step 1: Create a Namespace

```bash
kubectl create namespace jenkins
```

### Step 2: Deploy Jenkins

Navigate to your Jenkins manifest directory:

```bash
cd jenkins
kubectl apply -f deployment.yaml
```

Wait until Jenkins pods are running:

```bash
kubectl get pods -n jenkins
```

### Step 3: Access Jenkins UI

Forward the Jenkins service to your local machine:

```bash
kubectl port-forward svc/jenkins-service 8080:8080 -n jenkins
```

Then open your browser at: [http://localhost:8080](http://localhost:8080)

---

## 🔑 Jenkins Configuration

### Install Required Plugins

Once Jenkins is running, install the following plugins:

- Kubernetes
- Docker Pipeline
- GitHub Integration
- Pipeline: Stage View
- Blue Ocean (optional for visualization)

### 🔐 Configure Credentials

In **Jenkins → Manage Jenkins → Credentials → Global credentials**, add:

| ID | Type | Description |
|---|---|---|
| `docker-hub-password` | Username with password | Docker Hub username & password |
| `github-token` | Secret text | GitHub Personal Access Token (PAT) |

### ☁️ Cloud & Kubernetes Configuration

In **Jenkins → Manage Jenkins → Clouds → Kubernetes**:

1. Add a new Kubernetes Cloud
2. Set Kubernetes URL (auto-detected if Jenkins is inside cluster)
3. Set Jenkins URL to `http://jenkins-service.jenkins.svc.cluster.local:8080`
4. Save & Test Connection ✅

---

## 🧱 Docker Hub Setup

Create a new repository in Docker Hub, for example:

```
https://hub.docker.com/repository/docker/anupme/scenario-2
```

---

## 🧩 Create Jenkins Pipeline

### Step 1: Create a New Pipeline Job

1. Open Jenkins dashboard → **"New Item"** → choose **Pipeline**
2. Name it `Scenario-2-Pipeline`
3. In **Pipeline Definition**, select **Pipeline script**
4. Paste your Groovy pipeline script

### Step 2: Configure Environment Variables

Modify the top section in the pipeline as needed:

```groovy
environment {
    DOCKER_REPO = "anupme/scenario-2"  // DockerHub repo
    MY_APP_REPO = "https://github.com/Anup-Neupane/my-app.git"
    GIT_USER = "Anup-Neupane"
    TRIVY_SEVERITY = "HIGH,CRITICAL"
    TRIVY_EXIT_CODE = "0"
}
```

---

## 🧪 Pipeline Flow

| Stage | Description |
|---|---|
| **Checkout Source** | Clones app source code from GitHub |
| **Install Dependencies & Lint** | Installs Python dependencies & runs linting |
| **Run Unit Tests** | Executes unit tests & generates coverage report |
| **Build and Push Image** | Builds image using Kaniko and pushes to Docker Hub |
| **Security Scan** | Scans image using Trivy for vulnerabilities |
| **Update Deployment YAML** | Updates image tag in GitHub deployment.yaml |
| **Verify ArgoCD Sync** | Waits for ArgoCD to sync and deploy new version |

---

## 🧰 Kaniko Configuration

Kaniko is configured to build Docker images securely inside Kubernetes pods without requiring Docker daemon. The Jenkins pod template contains:

- `kaniko` for image build
- `trivy` for vulnerability scanning
- `python` for lint/test
- `git` for Git operations

---

## 🧿 Run the Pipeline

Click **Build Now** in Jenkins → monitor logs for progress.

### ✅ Successful Output Example

```
✅ PIPELINE SUCCEEDED
📦 Image: anupme/scenario-2:23
📝 Manifest Updated Successfully
🚀 ArgoCD Sync: Pending
```

---

## 🧹 Cleanup

To delete Jenkins resources:

```bash
kubectl delete namespace jenkins
```

---

## 📚 Summary

This CI/CD setup delivers:

- ✅ Secure image builds with Kaniko
- ✅ Vulnerability scanning via Trivy
- ✅ Automated deployment updates via GitOps (ArgoCD)
- ✅ Cloud-native Jenkins running inside Kubernetes

This guide provides a production-ready CI/CD pipeline that follows cloud-native best practices for security, reliability, and automation.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](../../issues).

## 👤 Author

**Anup Neupane**

- GitHub: [@Anup-Neupane](https://github.com/Anup-Neupane)

---

⭐️ If you found this helpful, please give it a star!
