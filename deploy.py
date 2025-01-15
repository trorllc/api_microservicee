import os
import subprocess
import sys

# Base directory where the services are located
BASE_DIR = "./services"

# Function to build and deploy a service
def build_and_deploy(service_name):
    # Construct the path to the service directory
    service_dir = os.path.join(BASE_DIR, service_name)
    
    # Check if the service directory exists
    if not os.path.isdir(service_dir):
        print(f"Service '{service_name}' does not exist in {BASE_DIR}.")
        return
    
    # Build the Docker image for the service
    image_name = f"{service_name}-image:latest"
    print(f"Building Docker image for {service_name}...")
    
    # Specify the Dockerfile name explicitly, as it is named `dockapi.dockerfile`
    subprocess.run(["docker", "build", "-t", image_name, "-f", os.path.join(service_dir, "dockapi.dockerfile"), service_dir], check=True)

    # Update the Kubernetes YAML files with the service name and image name
    for file in ["k8sdeploy.yml", "k8service.yml"]:
        file_path = os.path.join(service_dir, file)
        with open(file_path, "r") as f:
            content = f.read().replace("{{SERVICE_NAME}}", service_name).replace("{{IMAGE_NAME}}", image_name)
        with open(file_path, "w") as f:
            f.write(content)

    # Deploy the service to Kubernetes
    print(f"Applying Kubernetes deployment and service for {service_name}...")
    subprocess.run(["kubectl", "apply", "-f", os.path.join(service_dir, "k8sdeploy.yml")], check=True)
    subprocess.run(["kubectl", "apply", "-f", os.path.join(service_dir, "k8service.yml")], check=True)

    print(f"Service '{service_name}' deployed successfully.")

# Entry point of the script
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python deploy.py <service_name>")
        sys.exit(1)
    
    service_name = sys.argv[1]
    build_and_deploy(service_name)
