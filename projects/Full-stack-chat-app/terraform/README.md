   # Chat App Terraform Deployment

   ## Prerequisites

   - [Terraform](https://www.terraform.io/downloads.html) installed (v1.0.0+)
   - [Minikube](https://minikube.sigs.k8s.io/docs/start/) installed and running
   - [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) installed

   ## Quick Start

   1. Start Minikube:
      ```
      minikube start
      ```

   2. Initialize and apply Terraform:
      ```
      cd terraform
      terraform init
      terraform validate
      terraform apply -auto-approve
      ```
   
   3. Access the application:
      ```
      kubectl port-forward -n ingress-nginx service/ingress-nginx-controller 8080:80 --address=0.0.0.0
      ```
      
      Then open in browser:
      - Frontend: `http://localhost:8080`
      - Backend API: `http://localhost:8080/api`

   ## Cleanup

   ```
   terraform destroy -auto-approve
   ```

   ## Troubleshooting

   If the application is not accessible:

   1. Check Ingress addon: `minikube addons list`
   2. Verify Nginx controller: `kubectl get pods -n ingress-nginx`
   3. Check port forwarding: Ensure the port forwarding command is running without errors