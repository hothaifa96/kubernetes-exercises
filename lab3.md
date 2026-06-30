# Lab: Deploy Jenkins on Kubernetes with a NodePort Service

## Objective

In this lab you will learn how to:

- Create a Pod manually
- Configure CPU and Memory **Requests**
- Configure CPU and Memory **Limits**
- Expose a Pod using a **NodePort Service**
- Access an application running inside **Minikube**
- Verify resources and networking

---

# So....

Your company wants to deploy a Jenkins server for developers to use.

Instead of using a Deployment, the operations team wants to test Jenkins by creating a single Pod manually.

Your task is to:

- Deploy the Jenkins container
- Configure resource requests and limits
- Expose it using a NodePort Service
- Access Jenkins from your browser

---

# Requirements

## Pod

Name:

```
jenkins-pod
```

Image:

```
jenkins/jenkins:lts
```

Container Name:

```
jenkins
```

Container Port:

```
8080
```

---

## Resources

Configure the following resources.

### Requests

CPU

```
500m
```

Memory

```
512Mi
```

### Limits

CPU

```
1000m
```

Memory

```
1Gi
```

---

## Service

Create a Service named:

```
jenkins-service
```

Type:

```
NodePort
```

Target Port:

```
8080
```

Service Port:

```
8080
```

NodePort:

```
30080
```

---

# Tasks

## Task 1

Create the Pod and svc YAML.

Save them as

```
jenkins-pod.yaml
jenkins-svc.yaml
```

---

## Task 2

Deploy the Pod and the service

---

## Task 3

Verify the Pod is running.

Expected output

```
1/1 Running
```

---

## Task 4

Describe the Pod.

Verify:

- Image
- Requests
- Limits
- Container Port

---

## Task 5

Display the Pod YAML created in Kubernetes.

```bash
-o yaml
```

---

## Task 6

Verify the Service.

```bash
kubectl get ???
```

Expected output should include

```
TYPE       NodePort
PORT(S)    8080:30080/TCP
```

---

## Task 9

Access Jenkins.

If using Minikube, first retrieve the cluster IP.

```bash
minikube ip
```

Open your browser:

```
http://<MINIKUBE-IP>:30080
```

You should see the Jenkins setup page.
or
```bash
kubectl service jenkins-service
```
---

## Task 10

Retrieve the Jenkins initial administrator password.

its in this path inside the jenkins container 
`/var/jenkins_home/secrets/initialAdminPassword`


Copy the password.

---

## Task 11

Unlock Jenkins using the password.

---

## Task 12

Check the allocated resources.

Display the Pod.

Locate:

```
Requests
```

and

```
Limits
```

---

## Task 13

Display all Kubernetes objects.

```bash
kubectl get all
```

---

# Bonus Challenge 1

Add the following environment variable to the Pod.

```
JAVA_OPTS=-Djenkins.install.runSetupWizard=false
```

Redeploy the Pod.

What happens when Jenkins starts?

---

# Bonus Challenge 2

Add the following labels.

```
app=jenkins
tier=devops
environment=lab
```

Update the Service selector to match these labels.

Verify the Service still routes traffic correctly.

---

# Bonus Challenge 3

Increase the CPU limit to:

```
2
```

Increase the Memory limit to:

```
2Gi
```

Redeploy the Pod and verify the changes using:

```bash
kubectl describe pod jenkins-pod
```

---