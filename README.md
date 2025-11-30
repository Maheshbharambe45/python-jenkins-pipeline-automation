# 🚀 Python CI/CD with Jenkins, Docker & Minikube on AWS

This project demonstrates an end-to-end **CI/CD pipeline** 

# 🔧 Prerequisites

## 1️⃣ EC2 Instance Requirements

Ubuntu 20.04 or 22.04 EC2 Instance (t2.medium or higher recommended) <br>
Minimum 20GB EBS storage (required for Docker + Minikube)<br>
#### Security Group must allow:<br>

Port 22 → SSH<br>
Port 8080 → Jenkins UI (if hosted on same EC2)<br>
Port 30050 → Kubernetes NodePort Service (for Flask app)<br>

![Website Screenshot](assets/Screenshot%202025-11-30%20102820.png)


## 2️⃣ Tools Installed on EC2

On your EC2 instance (Jenkins + Minikube host), you should have:<br>

Docker<br>
Minikube (running with Docker/containerd)<br>
kubectl<br>
containerd or Docker runtime enabled<br>
Python 3 + pip<br>
Git<br>


## 3️⃣ Jenkins Server Requirements

### Jenkins can run:

On the same EC2 instance  <br>
Or another server that has network access to EC2 <br>

### Jenkins must have:

Pipeline and Git plugins enabled <br>
Python 3 available (for python3 -m pytest) <br>
Git installed (for SCM checkout) <br>



## 4️⃣ Jenkins Credentials Needed

You must configure two credentials inside Jenkins:

### 🔐 Docker Hub Credentials

ID: docker-crediantials <br>
Type: Username + Password <br>  
Used in Push Image stage of Jenkinsfile <br>


## 🔄 GitHub Auto-Build (Webhook)

This pipeline uses a GitHub Webhook so that every push to the repository automatically triggers a Jenkins build.

Steps to Enable Webhook

```bash
Go to your GitHub repo → Settings → Webhooks → Add Webhook
```

![Website Screenshot](assets/Screenshot%202025-11-30%20102922.png)

## ✅ Jenkins Pipeline Build Successful

![Website Screenshot](assets/Screenshot%202025-11-30%20102900.png)


## ☸️ Verify Pods on EC2 (Minikube)

```bash
kubectl get pods -o wide
kubectl get svc
```
![Website Screenshot](assets/Screenshot%202025-11-30%20102910.png)


## 🌐 Accessing the Application

Then open in browser:

```bash
http://<EC2_PUBLIC_IP>:30050/
```

Port Forward to Access Application
```bash
kubectl port-forward --address 0.0.0.0 svc/python-cicd-service 3000:5000

http://<EC2_PUBLIC_IP>:3000/
```
![Website Screenshot](assets/Screenshot%202025-11-30%20102832.png)
