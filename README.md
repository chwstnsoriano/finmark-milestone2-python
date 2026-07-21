# FinMark Terminal Assessment — Scalable and Resilient Prototype

FinMark is a working software-development prototype for a secure, scalable, and resilient business-service platform. It supports customer service orders and employee operations for FinMark Corporation, which provides financial analysis, marketing analytics, business intelligence, and consulting services to clients in retail, e-commerce, healthcare, and manufacturing.

The prototype began as a local FastAPI application and was extended with an independent Order Service, PostgreSQL persistence, Docker containerization, NGINX load balancing, Kubernetes orchestration, health probes, automatic Pod replacement, fallback behavior, audit logs, event records, role-based access control, and automated tests.

> **Current verified result:** `27 passed, 1 warning`
>
> **Current project branch:** `feature/docker-kubernetes-scaling`
>
> **Recommended test environment:** Windows 11, PowerShell, Docker Desktop using Linux containers, Docker Desktop Kubernetes using a `kubeadm` cluster.

---

## Table of Contents

1. [Project Problem and Goal](#project-problem-and-goal)
2. [What Is Implemented](#what-is-implemented)
3. [Architecture](#architecture)
4. [Technology Stack](#technology-stack)
5. [Repository Structure](#repository-structure)
6. [Choose a Run Mode](#choose-a-run-mode)
7. [Required Software Installation](#required-software-installation)
8. [Download the Project](#download-the-project)
9. [Mode A — Run with Local Python](#mode-a--run-with-local-python)
10. [Mode B — Run with Docker Compose](#mode-b--run-with-docker-compose)
11. [Docker Compose Demonstration](#docker-compose-demonstration)
12. [Mode C — Run with Kubernetes](#mode-c--run-with-kubernetes)
13. [Kubernetes Demonstration](#kubernetes-demonstration)
14. [Functional Application Demo](#functional-application-demo)
15. [API Endpoints](#api-endpoints)
16. [Automated Testing](#automated-testing)
17. [Stopping, Restarting, and Resetting](#stopping-restarting-and-resetting)
18. [Troubleshooting](#troubleshooting)
19. [Security Notes](#security-notes)
20. [Current Limitations](#current-limitations)
21. [Suggested Professor Demo Flow](#suggested-professor-demo-flow)
22. [Official Installation References](#official-installation-references)

---

## Project Problem and Goal

FinMark currently handles approximately 500 online service orders per day, but the expected demand may increase to 3,000 orders per day. Increased usage creates a greater risk of crashes, failed requests, order-processing interruptions, and data loss.

The prototype addresses this problem by demonstrating:

- safer request validation and error handling;
- customer and employee role separation;
- an independent Order Service;
- persistent PostgreSQL order storage;
- multiple Order Service replicas;
- load balancing across healthy replicas;
- fallback behavior when the external Order Service is unavailable;
- Kubernetes self-healing after a Pod is deleted;
- database persistence after a PostgreSQL Pod replacement;
- automated application testing.

This is a local academic prototype rather than a public production deployment.

---

## What Is Implemented

### Application features

- User registration and login
- Password hashing
- JWT authentication
- Role-based access control
- Customer and employee workflows
- Customer service-order placement
- Employee dashboard
- Orders, services, payments, reports, and monitoring pages
- Database-backed dashboard metrics
- Audit-log storage
- Event-bus simulation
- API request timing headers
- Basic in-memory rate limiting
- Health and resilience endpoints
- Local fallback behavior
- Pytest automated tests

### Scaling and resilience features

- Root FinMark FastAPI application
- Independent FastAPI Order Service
- PostgreSQL database for external service orders
- Local SQLite mirror and fallback storage
- Dockerfiles for both Python applications
- Docker Compose multi-container environment
- Three Docker Order Service replicas
- NGINX reverse proxy and load balancer
- Health checks for Docker services
- Kubernetes namespace and Services
- Kubernetes Deployment with three Order Service Pods
- Kubernetes StatefulSet for PostgreSQL
- PersistentVolumeClaim for PostgreSQL data
- Startup, readiness, and liveness probes
- Kubernetes automatic Pod replacement
- Kubernetes Service traffic distribution
- Secret template with the real local Secret excluded from Git

---

## Architecture

### Application-level architecture

```mermaid
flowchart LR
    U[Customer or Employee] --> A[FinMark FastAPI Application]
    A --> S[Local SQLite Database]
    A --> O[External Order Service]
    O --> P[(PostgreSQL Order Database)]
    A --> F[Local SQLite Fallback]
    A --> L[Audit Logs and Event Records]
```

The FinMark application uses SQLite for authentication, service catalog data, local order mirrors, payment records, audit logs, and event records. Customer orders are sent to the external Order Service when it is available. The Order Service stores its authoritative records in PostgreSQL. When the external service cannot be reached, the root application can use its local SQLite fallback.

### Docker Compose architecture

```mermaid
flowchart LR
    B[Browser or API Client] --> F[FinMark App :8000]
    F --> N[NGINX Load Balancer :8001]
    N --> O1[Order Service Replica 1]
    N --> O2[Order Service Replica 2]
    N --> O3[Order Service Replica 3]
    O1 --> D[(PostgreSQL)]
    O2 --> D
    O3 --> D
    D --> V[Docker Named Volume]
```

### Kubernetes architecture

```mermaid
flowchart LR
    B[Browser or API Client] --> FS[FinMark NodePort Service :30080]
    FS --> FP[FinMark App Pod]
    FP --> OS[Order Service ClusterIP]
    OS --> O1[Order Service Pod 1]
    OS --> O2[Order Service Pod 2]
    OS --> O3[Order Service Pod 3]
    O1 --> DS[PostgreSQL Service]
    O2 --> DS
    O3 --> DS
    DS --> DB[PostgreSQL StatefulSet Pod]
    DB --> PVC[PersistentVolumeClaim]
```

In Kubernetes, the `order-service` Deployment requests three replicas. If one Pod is deleted or becomes unhealthy, Kubernetes creates a replacement. The Service sends traffic only to ready backend Pods.

---

## Technology Stack

| Area | Technology |
|---|---|
| Backend | Python, FastAPI, Uvicorn |
| Validation/API models | Pydantic |
| Local database | SQLite |
| External Order Service database | PostgreSQL 18 Alpine |
| Authentication | JWT and password hashing |
| Frontend | HTML, CSS, Bootstrap, JavaScript |
| Containers | Docker and Docker Compose |
| Docker load balancer | NGINX Alpine |
| Orchestration | Kubernetes through Docker Desktop |
| Kubernetes storage | Docker Desktop `hostpath` StorageClass and PVC |
| Testing | Pytest and FastAPI TestClient |
| Development tools | VS Code, Git, GitHub, Postman, PowerShell |

---

## Repository Structure

```text
finmark-milestone2-python/
├── app/                                # Main FinMark FastAPI application
│   ├── services/                       # Application service layer
│   ├── static/                         # CSS and JavaScript
│   ├── templates/                      # HTML templates
│   ├── config.py
│   ├── database.py
│   └── main.py
├── services/
│   └── order_service/                  # Independent Order Service
│       ├── app/
│       ├── Dockerfile
│       └── requirements.txt
├── infrastructure/
│   └── nginx/
│       └── order-service.conf          # Docker load-balancer configuration
├── k8s/
│   ├── finmark-stack.yaml              # Kubernetes workloads and Services
│   ├── finmark-secrets.example.yaml    # Safe Secret template committed to Git
│   └── finmark-secrets.yaml            # Local real Secret; ignored by Git
├── tests/
│   └── test_app.py
├── compose.yaml
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Choose a Run Mode

Use one of the following modes.

| Mode | Purpose | Difficulty | Main URL |
|---|---|---:|---|
| Local Python | Fastest way to inspect the basic application and run tests | Beginner | `http://127.0.0.1:8000` |
| Docker Compose | Recommended container and load-balancing demonstration | Beginner–Intermediate | `http://127.0.0.1:8000` |
| Kubernetes | Recommended self-healing and orchestration demonstration | Intermediate | `http://127.0.0.1:30080` |

For a clean demonstration, run only one application mode at a time. Local Python and Docker Compose both use port `8000`.

---

# Required Software Installation

The detailed installation steps below are written for Windows and PowerShell.

## 1. Install Git

1. Download **Git for Windows** from the official Git website.
2. Run the installer.
3. The default options are acceptable for this project.
4. Close and reopen PowerShell after installation.
5. Verify:

```powershell
git --version
```

A version number must appear.

## 2. Install Python

The project was tested using **Python 3.14.6**. A current Python 3.14 installation is recommended for reproducing the verified environment.

1. Install Python from the official Python website or Python Install Manager.
2. Open a new PowerShell window.
3. Verify:

```powershell
python --version
python -m pip --version
```

Expected general result:

```text
Python 3.14.x
pip ...
```

A virtual environment will be created later so the project's packages do not interfere with packages from other Python projects.

## 3. Install WSL 2 for Docker Desktop

Docker Desktop on Windows normally uses the WSL 2 backend.

Open **PowerShell as Administrator** and run:

```powershell
wsl --install
```

Restart Windows if requested.

After restarting, verify:

```powershell
wsl --version
wsl --status
```

Update WSL when needed:

```powershell
wsl --update
```

Hardware virtualization must also be enabled in the computer's BIOS or UEFI settings. Docker Desktop may show a virtualization error when it is disabled.

## 4. Install Docker Desktop

1. Download **Docker Desktop for Windows** from Docker's official documentation.
2. Run the installer.
3. Use the **WSL 2 backend** when prompted.
4. Start Docker Desktop.
5. Accept the Docker agreement when prompted.
6. Wait until Docker Desktop reports that the engine is running.
7. Confirm that Docker is using **Linux containers**, which is the default and is required by this project.

Verify in PowerShell:

```powershell
docker version
docker compose version
docker info --format '{{.OSType}}'
```

Expected final value:

```text
linux
```

If `docker version` shows only Client information and a server connection error, Docker Desktop is not running yet.

## 5. Enable Kubernetes in Docker Desktop

This project uses locally built images with `imagePullPolicy: Never`. For the easiest reproduction, create a Docker Desktop Kubernetes cluster using **kubeadm**.

1. Open Docker Desktop.
2. Select **Kubernetes** in the left menu.
3. Select **Create cluster**.
4. Choose **kubeadm**.
5. Create a single-node cluster.
6. Wait until Kubernetes reports that it is running.

`kubeadm` is recommended for this repository because it works with Docker Desktop's Docker image store. The newer `kind` provisioner requires the containerd image store for this local-image workflow.

Verify:

```powershell
kubectl version --client
kubectl config get-contexts
kubectl config use-context docker-desktop
kubectl get nodes -o wide
kubectl get storageclass
```

Required results:

- context: `docker-desktop`
- node status: `Ready`
- a default StorageClass such as `hostpath`

---

# Download the Project

## Clone from GitHub

Open PowerShell in the folder where the project should be downloaded:

```powershell
git clone https://github.com/chwstnsoriano/finmark-milestone2-python.git
cd finmark-milestone2-python
git checkout feature/docker-kubernetes-scaling
git pull
```

Verify the branch:

```powershell
git branch --show-current
```

Expected:

```text
feature/docker-kubernetes-scaling
```

> If this branch is merged into `main` later, use the branch specified by the project owner or professor.

## Existing group member copy

A group member who already cloned the repository should run:

```powershell
cd "PATH\TO\finmark-milestone2-python"
git checkout feature/docker-kubernetes-scaling
git pull
```

---

# Mode A — Run with Local Python

This mode runs only the main FinMark application. Because the external Order Service is not started, orders use the application's local fallback behavior.

## 1. Create a virtual environment

From the project root:

```powershell
python -m venv .venv
```

## 2. Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

When activation succeeds, the prompt begins with:

```text
(.venv)
```

If PowerShell blocks script execution, run this once for the current Windows account:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Close PowerShell, open it again, return to the project, and activate the environment.

## 3. Install packages

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 4. Run automated tests

```powershell
python -m pytest
```

Expected:

```text
27 passed, 1 warning
```

## 5. Start the application

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open:

- Application: `http://127.0.0.1:8000`
- Swagger API documentation: `http://127.0.0.1:8000/docs`
- Health endpoint: `http://127.0.0.1:8000/api/system/health`

Stop the server with:

```text
Ctrl + C
```

---

# Mode B — Run with Docker Compose

Docker Compose is the recommended way to demonstrate containerization, PostgreSQL, three Order Service replicas, NGINX load balancing, and application fallback.

## Docker services

| Service | Purpose | Host access |
|---|---|---|
| `finmark-app` | Main FinMark application | `http://127.0.0.1:8000` |
| `order-lb` | NGINX load balancer | `http://127.0.0.1:8001` |
| `order-service` | Three internal FastAPI replicas | Internal Docker network |
| `order-db` | PostgreSQL database | Host port `5433` |

## 1. Make sure Kubernetes is not required for this mode

Kubernetes may stay enabled in Docker Desktop, but no Kubernetes deployment is needed for this section.

## 2. Start the complete Docker stack

From the repository root:

```powershell
docker compose up -d --build --scale order-service=3
```

Meaning:

- `up` creates and starts the services;
- `-d` runs them in the background;
- `--build` rebuilds the application images;
- `--scale order-service=3` creates three Order Service containers.

Wait for startup:

```powershell
Start-Sleep -Seconds 20
```

## 3. Check container health

```powershell
docker compose ps
```

Expected running containers:

- one FinMark application;
- one PostgreSQL database;
- one NGINX load balancer;
- three Order Service replicas.

All should eventually show `healthy`.

## 4. Test Docker endpoints

Main application health:

```powershell
Invoke-RestMethod `
    -Uri http://127.0.0.1:8000/api/system/health |
ConvertTo-Json -Depth 10
```

Load-balancer health:

```powershell
Invoke-RestMethod `
    -Uri http://127.0.0.1:8001/lb-health |
ConvertTo-Json -Depth 10
```

Order Service readiness through NGINX:

```powershell
Invoke-RestMethod `
    -Uri http://127.0.0.1:8001/health/ready |
ConvertTo-Json -Depth 10
```

Open the application:

```text
http://127.0.0.1:8000
```

---

# Docker Compose Demonstration

## Demo 1 — Prove that three replicas are running

```powershell
docker compose ps order-service
```

Expected: three Order Service containers.

## Demo 2 — Prove NGINX load balancing

Run 12 independent requests:

```powershell
$dockerInstances = 1..12 | ForEach-Object {
    $response = Invoke-RestMethod `
        -Uri http://127.0.0.1:8001/instance `
        -DisableKeepAlive

    [PSCustomObject]@{
        Request  = $_
        Instance = $response.instance_id
    }
}

$dockerInstances | Format-Table -AutoSize
```

Count the requests per replica:

```powershell
$dockerInstances.Instance |
Group-Object |
Sort-Object Name |
Select-Object Count, Name |
Format-Table -AutoSize
```

Expected: three different instance IDs. NGINX should distribute requests across the three replicas.

## Demo 3 — Place a real order through the scaled system

```powershell
$dockerOrderEmail = (
    "docker-demo-" +
    (Get-Date -Format "yyyyMMddHHmmss") +
    "@test.com"
)

$dockerOrderBody = @{
    customer_name  = "Docker Demo Customer"
    customer_email = $dockerOrderEmail
    client_type    = "retail"
    service_id     = 1
    order_notes    = "Order created during the Docker load-balancing demo."
} | ConvertTo-Json

$dockerOrder = Invoke-RestMethod `
    -Method Post `
    -Uri http://127.0.0.1:8000/api/orders/place `
    -ContentType "application/json" `
    -Body $dockerOrderBody `
    -DisableKeepAlive

$dockerOrder | ConvertTo-Json -Depth 10
```

Expected important fields:

```text
source: External PostgreSQL Order Service
handled_by_instance: one Order Service replica
```

## Demo 4 — Stop one replica and prove continued availability

Select one running Order Service container:

```powershell
$stoppedOrderContainer = (
    docker compose ps -q order-service |
    Select-Object -First 1
)

Write-Host "Stopping container:" $stoppedOrderContainer
docker stop $stoppedOrderContainer
```

Check that two replicas remain available:

```powershell
docker compose ps order-service
```

Send requests through NGINX:

```powershell
$dockerFailureRequests = 1..12 | ForEach-Object {
    try {
        $response = Invoke-RestMethod `
            -Uri http://127.0.0.1:8001/instance `
            -DisableKeepAlive `
            -TimeoutSec 5

        [PSCustomObject]@{
            Request  = $_
            Result   = "Success"
            Instance = $response.instance_id
        }
    }
    catch {
        [PSCustomObject]@{
            Request  = $_
            Result   = "Failed"
            Instance = ""
        }
    }
}

$dockerFailureRequests | Format-Table -AutoSize
```

Expected: requests continue through the remaining replicas.

Restart the stopped container:

```powershell
docker start $stoppedOrderContainer
Start-Sleep -Seconds 10
docker compose ps order-service
```

## Demo 5 — Prove local fallback when every external replica is unavailable

Stop all Order Service replicas:

```powershell
docker compose stop order-service
```

Create an order:

```powershell
$fallbackEmail = (
    "fallback-demo-" +
    (Get-Date -Format "yyyyMMddHHmmss") +
    "@test.com"
)

$fallbackBody = @{
    customer_name  = "Fallback Demo Customer"
    customer_email = $fallbackEmail
    client_type    = "healthcare"
    service_id     = 2
    order_notes    = "Testing local fallback while the external Order Service is down."
} | ConvertTo-Json

$fallbackOrder = Invoke-RestMethod `
    -Method Post `
    -Uri http://127.0.0.1:8000/api/orders/place `
    -ContentType "application/json" `
    -Body $fallbackBody `
    -DisableKeepAlive

$fallbackOrder | ConvertTo-Json -Depth 10
```

Expected source: local SQLite fallback rather than the external PostgreSQL Order Service.

Restore all three replicas:

```powershell
docker compose up -d --scale order-service=3
Start-Sleep -Seconds 15
docker compose ps
```

## Demo 6 — View NGINX routing logs

```powershell
docker compose logs order-lb --tail 50
```

The `upstream=` values show which internal Order Service address handled each request.

## Stop Docker Compose without deleting data

```powershell
docker compose down
```

This removes the containers and network but keeps the PostgreSQL named volume.

Do **not** use the following command unless a complete database reset is intended:

```powershell
docker compose down -v
```

The `-v` option deletes the named database volume and stored Docker orders.

---

# Mode C — Run with Kubernetes

This mode demonstrates three Order Service Pods, Kubernetes Service distribution, health probes, self-healing, and PostgreSQL persistent storage.

## Important Kubernetes prerequisites

Before continuing, verify:

```powershell
docker version
kubectl config use-context docker-desktop
kubectl get nodes
kubectl get storageclass
```

Required:

- Docker Desktop is running;
- context is `docker-desktop`;
- node is `Ready`;
- `hostpath` or another default StorageClass exists.

Stop the Compose environment first to keep the demonstration easy to understand:

```powershell
docker compose down
```

## 1. Build the two local Kubernetes images

From the project root:

```powershell
docker build -t finmark-app:k8s-v1 .

docker build `
    -t finmark-order-service:k8s-v1 `
    .\services\order_service
```

Verify:

```powershell
docker image ls `
    --format "table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}" |
Select-String "k8s-v1"
```

Expected images:

```text
finmark-app             k8s-v1
finmark-order-service   k8s-v1
```

## 2. Create the namespace

```powershell
kubectl create namespace finmark `
    --dry-run=client `
    -o yaml |
kubectl apply -f -
```

Verify:

```powershell
kubectl get namespace finmark
```

## 3. Create the local Kubernetes Secret

The repository contains a safe example file. Copy it to the ignored local Secret file:

```powershell
Copy-Item `
    .\k8s\finmark-secrets.example.yaml `
    .\k8s\finmark-secrets.yaml
```

Open it:

```powershell
notepad .\k8s\finmark-secrets.yaml
```

Replace all placeholder values. A local demonstration example is:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: finmark-secrets
  namespace: finmark
type: Opaque
stringData:
  POSTGRES_DB: finmark_orders
  POSTGRES_USER: finmark_order
  POSTGRES_PASSWORD: finmark-demo-password-2026
  DATABASE_URL: postgresql://finmark_order:finmark-demo-password-2026@order-db:5432/finmark_orders
  SECRET_KEY: finmark-local-demo-jwt-secret-key-change-this
  PASSWORD_SALT: finmark-local-demo-password-salt-change-this
  TOKEN_ALGORITHM: HS256
```

Important:

- `POSTGRES_PASSWORD` and the password inside `DATABASE_URL` must match exactly.
- Use a password without spaces or URL-special characters for the local demonstration.
- Do not commit `k8s/finmark-secrets.yaml`.

Confirm that no placeholders remain:

```powershell
Select-String `
    -Path .\k8s\finmark-secrets.yaml `
    -Pattern "replace-with"
```

Expected: no output.

Confirm Git ignores the real Secret:

```powershell
git check-ignore -v .\k8s\finmark-secrets.yaml
```

Expected: a `.gitignore` rule is displayed.

## 4. Validate the Kubernetes files

```powershell
kubectl apply `
    --dry-run=client `
    -f .\k8s\finmark-secrets.yaml

kubectl apply `
    --dry-run=client `
    -f .\k8s\finmark-stack.yaml
```

There must be no YAML or validation error.

## 5. Deploy the stack

Apply the Secret first:

```powershell
kubectl apply -f .\k8s\finmark-secrets.yaml
```

Apply the workloads and Services:

```powershell
kubectl apply -f .\k8s\finmark-stack.yaml
```

## 6. Watch startup

```powershell
kubectl get pods -n finmark --watch
```

Wait until all five Pods show `1/1 Running`:

- one FinMark application Pod;
- one PostgreSQL Pod named `order-db-0`;
- three Order Service Pods.

Press `Ctrl + C` after they are ready.

Formal rollout checks:

```powershell
kubectl rollout status `
    statefulset/order-db `
    -n finmark `
    --timeout=180s

kubectl rollout status `
    deployment/order-service `
    -n finmark `
    --timeout=180s

kubectl rollout status `
    deployment/finmark-app `
    -n finmark `
    --timeout=180s
```

## 7. Verify resources and storage

```powershell
kubectl get all -n finmark -o wide
kubectl get pvc -n finmark
kubectl get endpointslice `
    -n finmark `
    -l kubernetes.io/service-name=order-service `
    -o wide
```

Required results:

- FinMark Deployment: `1/1`
- Order Service Deployment: `3/3`
- PostgreSQL StatefulSet: `1/1`
- PVC status: `Bound`
- Order Service EndpointSlice: three endpoint IP addresses

## 8. Open the Kubernetes application

- FinMark application: `http://127.0.0.1:30080`
- FinMark health: `http://127.0.0.1:30080/api/system/health`
- Order Service demo endpoint: `http://127.0.0.1:30081/instance`
- Order Service readiness: `http://127.0.0.1:30081/health/ready`

Test in PowerShell:

```powershell
Invoke-RestMethod `
    -Uri http://127.0.0.1:30080/api/system/health |
ConvertTo-Json -Depth 10

Invoke-RestMethod `
    -Uri http://127.0.0.1:30081/health/ready |
ConvertTo-Json -Depth 10
```

Expected:

```text
overall_status: healthy
status: ready
database: connected
```

---

# Kubernetes Demonstration

## Demo 1 — Prove traffic reaches three Pods

```powershell
$kubernetesInstances = 1..15 | ForEach-Object {
    $response = Invoke-RestMethod `
        -Uri http://127.0.0.1:30081/instance `
        -DisableKeepAlive

    [PSCustomObject]@{
        Request  = $_
        Instance = $response.instance_id
    }
}

$kubernetesInstances | Format-Table -AutoSize
```

Count unique Pods:

```powershell
$uniqueKubernetesPods = @(
    $kubernetesInstances.Instance |
    Sort-Object -Unique
)

$uniqueKubernetesPods
Write-Host "Unique Kubernetes Order Service Pods:" $uniqueKubernetesPods.Count
```

Expected count:

```text
3
```

Kubernetes Service distribution is not required to appear in a perfectly repeating order. The important result is that requests reach all ready replicas.

## Demo 2 — Kubernetes self-healing

Record the three current Pods:

```powershell
$beforePods = @(
    kubectl get pods `
        -n finmark `
        -l app=order-service `
        -o name |
    ForEach-Object {
        $_ -replace '^pod/', ''
    }
)

$beforePods
```

Select and delete one:

```powershell
$deletedPod = $beforePods | Select-Object -First 1
Write-Host "Deleting Pod:" $deletedPod

kubectl delete pod `
    $deletedPod `
    -n finmark `
    --wait=false
```

Immediately test availability:

```powershell
$selfHealingRequests = 1..20 | ForEach-Object {
    try {
        $response = Invoke-RestMethod `
            -Uri http://127.0.0.1:30081/instance `
            -DisableKeepAlive `
            -TimeoutSec 5

        [PSCustomObject]@{
            Request  = $_
            Result   = "Success"
            Instance = $response.instance_id
        }
    }
    catch {
        [PSCustomObject]@{
            Request  = $_
            Result   = "Failed"
            Instance = ""
        }
    }

    Start-Sleep -Milliseconds 300
}

$selfHealingRequests | Format-Table -AutoSize
```

Count failures:

```powershell
$failedRequests = @(
    $selfHealingRequests |
    Where-Object { $_.Result -eq "Failed" }
).Count

Write-Host "Failed requests during recovery:" $failedRequests
```

Target:

```text
Failed requests during recovery: 0
```

Wait for Kubernetes to restore three replicas:

```powershell
kubectl rollout status `
    deployment/order-service `
    -n finmark `
    --timeout=180s

kubectl get pods `
    -n finmark `
    -l app=order-service `
    -o wide
```

Compare the old and new Pod lists:

```powershell
$afterPods = @(
    kubectl get pods `
        -n finmark `
        -l app=order-service `
        -o name |
    ForEach-Object {
        $_ -replace '^pod/', ''
    }
)

Compare-Object `
    -ReferenceObject $beforePods `
    -DifferenceObject $afterPods
```

Expected:

- the deleted Pod appears with `<=`;
- a new replacement Pod appears with `=>`;
- the Deployment is again `3/3`.

## Demo 3 — Place a real order during or after recovery

```powershell
$k8sOrderEmail = (
    "k8s-demo-" +
    (Get-Date -Format "yyyyMMddHHmmss") +
    "@test.com"
)

$k8sOrderBody = @{
    customer_name  = "Kubernetes Demo Customer"
    customer_email = $k8sOrderEmail
    client_type    = "manufacturing"
    service_id     = 4
    order_notes    = "Order created during the Kubernetes self-healing demonstration."
} | ConvertTo-Json

$k8sOrder = Invoke-RestMethod `
    -Method Post `
    -Uri http://127.0.0.1:30080/api/orders/place `
    -ContentType "application/json" `
    -Body $k8sOrderBody `
    -DisableKeepAlive

$k8sOrder | ConvertTo-Json -Depth 10
```

Expected:

```text
source: External PostgreSQL Order Service
handled_by_instance: a healthy Order Service Pod
```

Confirm it is stored:

```powershell
$storedOrders = Invoke-RestMethod `
    -Uri http://127.0.0.1:30081/orders `
    -DisableKeepAlive

$storedOrders.orders |
Where-Object {
    $_.customer_email -eq $k8sOrderEmail
} |
ConvertTo-Json -Depth 10
```

## Demo 4 — PostgreSQL persistence after Pod replacement

Record the number of stored external orders:

```powershell
$ordersBeforeDatabaseRestart = Invoke-RestMethod `
    -Uri http://127.0.0.1:30081/orders `
    -DisableKeepAlive

$beforeOrderCount = $ordersBeforeDatabaseRestart.count
Write-Host "Orders before database Pod deletion:" $beforeOrderCount
```

Delete the PostgreSQL Pod:

```powershell
kubectl delete pod order-db-0 -n finmark --wait=false
```

The StatefulSet recreates a Pod with the same name and reconnects the PVC.

Wait:

```powershell
kubectl wait `
    -n finmark `
    --for=condition=Ready `
    pod/order-db-0 `
    --timeout=180s

kubectl wait `
    -n finmark `
    --for=condition=Ready `
    pod `
    -l app=order-service `
    --timeout=180s
```

Check the order count again:

```powershell
$ordersAfterDatabaseRestart = Invoke-RestMethod `
    -Uri http://127.0.0.1:30081/orders `
    -DisableKeepAlive

$afterOrderCount = $ordersAfterDatabaseRestart.count

Write-Host "Orders before database restart:" $beforeOrderCount
Write-Host "Orders after database restart:" $afterOrderCount

if ($afterOrderCount -eq $beforeOrderCount) {
    Write-Host "PASS: PostgreSQL data survived the Pod replacement."
}
else {
    Write-Host "FAIL: The order count changed unexpectedly."
}
```

Expected:

```text
PASS: PostgreSQL data survived the Pod replacement.
```

## Demo 5 — Confirm the replacement Pod receives traffic

```powershell
$postHealingInstances = 1..30 | ForEach-Object {
    $response = Invoke-RestMethod `
        -Uri http://127.0.0.1:30081/instance `
        -DisableKeepAlive

    $response.instance_id
}

$postHealingInstances |
Sort-Object -Unique
```

Expected: three current Pod names, including the newly created replacement.

---

# Functional Application Demo

The following application flow can be demonstrated in Local Python, Docker Compose, or Kubernetes mode. Use the URL that belongs to the selected mode.

## Customer flow

1. Open the application.
2. Select **Register**.
3. Register a user with the `customer` role.
4. Log in using the new email and password.
5. Confirm that the customer is redirected to the service-order page.
6. Select a client type.
7. Select one of the FinMark services.
8. Submit the order.
9. Confirm the success message.

Customer users are blocked from protected employee dashboard APIs.

## Employee flow

1. Register or log in using an employee role such as `admin`, `coo`, `finance`, `operations`, or `staff`.
2. Confirm that the employee is redirected to the dashboard.
3. Open the following pages:
   - Dashboard
   - Orders
   - Services
   - Payments
   - Reports
   - Monitoring
4. Show that submitted customer orders affect the displayed records and summaries.
5. Open the Monitoring page to show audit logs, event records, service status, request timing, and resilience information.

## FinMark service catalog

- Financial Analysis
- Marketing Analytics
- Business Intelligence
- Consulting Services

---

# API Endpoints

## Main FinMark application

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/api/auth/register` | Register a user |
| `POST` | `/api/auth/login` | Authenticate and create JWT token |
| `GET` | `/api/dashboard/summary` | Protected dashboard summary |
| `GET` | `/api/services/catalog` | List FinMark services |
| `POST` | `/api/orders/place` | Place customer service order |
| `GET` | `/api/orders/list` | List local application orders |
| `GET` | `/api/orders/summary` | Order summary |
| `GET` | `/api/payments/summary` | Payment summary |
| `GET` | `/api/products/summary` | Service catalog summary |
| `GET` | `/api/financials/summary` | Financial summary |
| `GET` | `/api/audit-logs` | Audit records |
| `GET` | `/api/events` | Simulated event-bus records |
| `GET` | `/api/system/services` | Service status |
| `GET` | `/api/system/health` | Health report |
| `GET` | `/api/system/resilience` | Resilience configuration |

## Independent Order Service

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health/live` | Liveness check |
| `GET` | `/health/ready` | Readiness and database check |
| `GET` | `/instance` | Return the handling replica or Pod name |
| `POST` | `/orders` | Create an external PostgreSQL order |
| `GET` | `/orders` | List external PostgreSQL orders |

### Endpoint ports by mode

| Mode | FinMark | Order Service or load balancer |
|---|---|---|
| Local Python | `127.0.0.1:8000` | Not started |
| Docker Compose | `127.0.0.1:8000` | `127.0.0.1:8001` |
| Kubernetes | `127.0.0.1:30080` | `127.0.0.1:30081` |

---

# Automated Testing

Activate the virtual environment first:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies when needed:

```powershell
python -m pip install -r requirements.txt
```

Run tests:

```powershell
python -m pytest
```

Verified result:

```text
27 passed, 1 warning
```

The current warning comes from Starlette/FastAPI TestClient dependency behavior. It does not cause a test failure.

The tests cover areas such as:

- health checks;
- registration and login validation;
- JWT-protected routes;
- role-based access control;
- service catalog;
- order placement;
- order listing;
- audit logs;
- event records;
- customer dashboard restrictions;
- system resilience information;
- API Gateway-style response headers.

---

# Stopping, Restarting, and Resetting

## Docker Compose

### Stop and preserve the database volume

```powershell
docker compose down
```

### Restart with three Order Service replicas

```powershell
docker compose up -d --scale order-service=3
```

Use the explicit `--scale order-service=3` option whenever the Compose containers are recreated. A plain `docker compose up -d` may create only one Order Service replica.

### Complete Docker data reset

```powershell
docker compose down -v
```

Warning: this deletes Docker PostgreSQL data.

## Kubernetes

### Check current resources

```powershell
kubectl get all -n finmark
kubectl get pvc -n finmark
```

### Remove the Kubernetes deployment and its local data

```powershell
kubectl delete namespace finmark
```

Warning: deleting the namespace also deletes the namespaced PVC and the Kubernetes demonstration data.

### Deploy again after a namespace reset

```powershell
kubectl create namespace finmark
kubectl apply -f .\k8s\finmark-secrets.yaml
kubectl apply -f .\k8s\finmark-stack.yaml
```

### Stop the Docker Desktop Kubernetes cluster

Use the Kubernetes view in Docker Desktop and stop the cluster. Stopping the cluster is different from deleting the `finmark` namespace.

---

# Troubleshooting

## `docker` command is not recognized

Close and reopen PowerShell after installing Docker Desktop. Confirm Docker Desktop is installed and running.

```powershell
docker version
```

## Docker cannot connect to the engine

Start Docker Desktop and wait until the engine is running.

```powershell
docker desktop status
```

If supported by the installed Docker Desktop version:

```powershell
docker desktop start
```

## WSL error or Docker Desktop cannot start

Open PowerShell as Administrator:

```powershell
wsl --update
wsl --shutdown
```

Restart Docker Desktop. Confirm virtualization is enabled in BIOS/UEFI.

## PowerShell will not activate `.venv`

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Open a new PowerShell window and activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Port 8000, 8001, 30080, or 30081 is already in use

Check which process is using the port:

```powershell
Get-NetTCPConnection -State Listen |
Where-Object {
    $_.LocalPort -in 8000, 8001, 30080, 30081
} |
Format-Table -AutoSize
```

Stop the previous local Python server, Compose stack, or Kubernetes port-forward process.

## Docker Compose starts only one Order Service replica

Run:

```powershell
docker compose up -d --scale order-service=3
```

Verify:

```powershell
docker compose ps order-service
```

## A Docker container is unhealthy

```powershell
docker compose ps
docker compose logs order-db --tail 100
docker compose logs order-service --tail 100
docker compose logs order-lb --tail 100
docker compose logs finmark-app --tail 100
```

## `kubectl` is not recognized

Docker Desktop normally installs `kubectl` when Kubernetes is enabled. Restart PowerShell after creating the cluster. If it is still unavailable, follow the official Kubernetes Windows `kubectl` installation instructions.

## `kubectl` uses the wrong context

```powershell
kubectl config get-contexts
kubectl config use-context docker-desktop
```

## Kubernetes node is not ready

```powershell
kubectl get nodes -o wide
kubectl cluster-info
```

Restart the Kubernetes cluster from Docker Desktop.

## Kubernetes Pod shows `ImagePullBackOff` or `ErrImageNeverPull`

The local images were not built, the wrong image tags were used, or the cluster does not have access to Docker's local image store.

Build again:

```powershell
docker build -t finmark-app:k8s-v1 .
docker build -t finmark-order-service:k8s-v1 .\services\order_service
```

Verify that the Docker Desktop cluster was created with `kubeadm` for this workflow.

Restart the Deployments:

```powershell
kubectl rollout restart deployment/finmark-app -n finmark
kubectl rollout restart deployment/order-service -n finmark
```

## Kubernetes Pod shows `CrashLoopBackOff`

Inspect the Pod:

```powershell
kubectl get pods -n finmark
kubectl describe pod POD_NAME -n finmark
kubectl logs POD_NAME -n finmark --tail 100
kubectl logs POD_NAME -n finmark --previous --tail 100
```

For Order Service failures, check PostgreSQL first:

```powershell
kubectl get pod order-db-0 -n finmark
kubectl logs order-db-0 -n finmark --tail 100
```

## Order Service cannot connect to PostgreSQL

Open `k8s/finmark-secrets.yaml` and verify:

- `POSTGRES_PASSWORD` is correct;
- the password inside `DATABASE_URL` is identical;
- host is `order-db`;
- port is `5432`;
- database is `finmark_orders`;
- username is `finmark_order`.

Reapply the Secret and restart affected workloads:

```powershell
kubectl apply -f .\k8s\finmark-secrets.yaml
kubectl rollout restart statefulset/order-db -n finmark
kubectl rollout restart deployment/order-service -n finmark
```

## Kubernetes resources are running but NodePort does not open

Use port forwarding in separate PowerShell windows.

FinMark:

```powershell
kubectl port-forward `
    service/finmark-app `
    8000:8000 `
    -n finmark
```

Order Service:

```powershell
kubectl port-forward `
    service/order-service-demo `
    8001:8001 `
    -n finmark
```

Then open `http://127.0.0.1:8000` and test `http://127.0.0.1:8001/instance`.

## Start again from a clean Kubernetes namespace

Warning: this deletes Kubernetes demonstration data.

```powershell
kubectl delete namespace finmark --ignore-not-found
kubectl create namespace finmark
kubectl apply -f .\k8s\finmark-secrets.yaml
kubectl apply -f .\k8s\finmark-stack.yaml
```

---

# Security Notes

- Passwords are hashed rather than stored as plain text.
- JWT tokens protect authenticated routes.
- Role-based access control separates customers from employee dashboards.
- Input validation rejects missing or invalid fields.
- The real Kubernetes Secret file is excluded by `.gitignore`.
- `k8s/finmark-secrets.example.yaml` contains placeholders only.
- Demo credentials and local Secrets must not be reused in production.
- Kubernetes Secrets are not a complete production secret-management solution by themselves.
- The prototype does not provide public HTTPS, WAF, DDoS protection, or managed cloud identity.

Before committing changes, verify that the local Secret is ignored:

```powershell
git check-ignore -v .\k8s\finmark-secrets.yaml
git ls-files k8s/finmark-secrets.yaml
```

The second command should return no output.

---

# Current Limitations

- This is a local academic prototype.
- The root application still uses SQLite for authentication, catalog, payments, local mirrors, audit logs, and event records.
- PostgreSQL is currently dedicated to the external Order Service only.
- The payment process is simulated.
- The event bus is simulated using a database table.
- The cache is in memory rather than Redis.
- Rate limiting is in memory and resets when the application restarts.
- Docker NGINX load balancing is local and does not include HTTPS.
- Kubernetes uses a single Docker Desktop node rather than a production multi-node cloud cluster.
- Kubernetes NodePort Services are intended for local demonstration.
- The Kubernetes PostgreSQL deployment is a single StatefulSet replica rather than a highly available managed database.
- No real payment gateway, message broker, email service, CDN, WAF, or DDoS protection is connected.
- Monitoring does not yet use Prometheus, Grafana, or centralized logs.

---

# Future Improvements

- Replace remaining SQLite components with appropriate service databases.
- Add Redis-backed distributed caching and rate limiting.
- Replace the simulated event bus with RabbitMQ, Kafka, or another message broker.
- Add real payment-gateway integration.
- Add email notifications and order-status tracking.
- Add customer order history.
- Add employee role-specific dashboards.
- Add MFA and stronger production identity controls.
- Publish versioned images to a container registry.
- Add Kubernetes resource requests and limits.
- Add Horizontal Pod Autoscaling.
- Add Ingress and HTTPS.
- Add Prometheus, Grafana, centralized logging, and alerting.
- Deploy to a managed cloud Kubernetes environment.
- Use a managed highly available PostgreSQL service.
- Add CI/CD for test, image-build, vulnerability-scan, and deployment stages.

---

# Suggested Demo Flow

The following sequence provides a clear end-to-end presentation.

## Part 1 — Automated quality check

```powershell
.\.venv\Scripts\Activate.ps1
python -m pytest
```

Show:

```text
27 passed, 1 warning
```

## Part 2 — Docker Compose scaling

```powershell
docker compose up -d --build --scale order-service=3
Start-Sleep -Seconds 20
docker compose ps
```

Show:

- one FinMark app;
- one PostgreSQL database;
- one NGINX load balancer;
- three Order Service replicas.

Run the 12-request `/instance` test and show three instance IDs.

## Part 3 — Docker failure tolerance

Stop one Order Service container, repeat requests, and show that the remaining replicas continue serving. Restart the stopped replica afterward.

## Part 4 — Functional application

Open `http://127.0.0.1:8000`:

1. register a customer;
2. log in;
3. submit a service order;
4. log in as an employee;
5. show dashboard, orders, payments, reports, and monitoring;
6. show `/api/system/health`.

Stop Docker before Kubernetes:

```powershell
docker compose down
```

## Part 5 — Kubernetes deployment

```powershell
kubectl apply -f .\k8s\finmark-secrets.yaml
kubectl apply -f .\k8s\finmark-stack.yaml
kubectl get all -n finmark -o wide
kubectl get pvc -n finmark
```

Show:

- FinMark `1/1`;
- Order Service `3/3`;
- PostgreSQL `1/1`;
- PVC `Bound`;
- three Service endpoints.

## Part 6 — Kubernetes load balancing

Run the 15-request `/instance` test against port `30081` and show three unique Pod names.

## Part 7 — Kubernetes self-healing

Delete one Order Service Pod, show requests continuing, wait for the replacement, and compare the old and new Pod names.

## Part 8 — PostgreSQL persistence

Create an order, delete `order-db-0`, wait for it to become ready, and show that the order count and stored order remain available.

## Part 9 — Final status

```powershell
Invoke-RestMethod `
    -Uri http://127.0.0.1:30080/api/system/health |
ConvertTo-Json -Depth 10

kubectl get all -n finmark -o wide
```

Conclude with:

- the system remained available during an Order Service Pod replacement;
- Kubernetes automatically restored the requested three replicas;
- PostgreSQL data survived database Pod replacement through the PVC;
- all automated tests passed.

---

# Official Installation References

- [Git for Windows](https://git-scm.com/download/win)
- [Python on Windows](https://docs.python.org/3/using/windows.html)
- [Python downloads](https://www.python.org/downloads/)
- [Install WSL](https://learn.microsoft.com/windows/wsl/install)
- [Install Docker Desktop on Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Docker Desktop Kubernetes](https://docs.docker.com/desktop/use-desktop/kubernetes/)
- [Install kubectl on Windows](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/)
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Kubernetes probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [Kubernetes persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)

---

## Final Verified Prototype Results

- Main FastAPI application works locally and in containers.
- Independent Order Service stores orders in PostgreSQL.
- Docker Compose runs three Order Service replicas behind NGINX.
- Requests continue after one Docker replica is stopped.
- Local SQLite fallback works when the external service is unavailable.
- Kubernetes runs three ready Order Service Pods.
- Kubernetes automatically replaces a deleted Order Service Pod.
- Requests continue during Kubernetes Pod replacement.
- The replacement Pod receives Service traffic.
- PostgreSQL data survives replacement of the database Pod through the PVC.
- The real Kubernetes Secret is excluded from Git.
- Automated test result: **27 passed, 1 warning**.
