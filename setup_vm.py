import subprocess
import time
import paramiko  # Ensure paramiko is installed for SSH access

TERRAFORM_DIR = "C:\\path\\to\\terraform\\config"

def run_terraform():
    """Initialize and apply Terraform configuration."""
    subprocess.run(["terraform", "init"], cwd=TERRAFORM_DIR, check=True)
    subprocess.run(["terraform", "apply", "-auto-approve"], cwd=TERRAFORM_DIR, check=True)

def get_vm_ip():
    """Extract VM IP address from Terraform output."""
    result = subprocess.run(["terraform", "output", "-raw", "vm_ip"], cwd=TERRAFORM_DIR, capture_output=True, text=True)
    return result.stdout.strip()

def install_dependencies(ip, username="admin", password="password"):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"Connecting to VM at {ip}...")
    retries = 5
    while retries:
        try:
            ssh.connect(ip, username=username, password=password)
            break
        except:
            print("Retrying SSH connection...")
            time.sleep(10)
            retries -= 1
    
    print("Installing Python dependencies...")
    commands = [
        "sudo apt update && sudo apt install -y python3-pip",  # Linux
        "pip install flask requests"  # Install API dependencies
    ]
    
    for cmd in commands:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode(), stderr.read().decode())
    
    ssh.close()

if __name__ == "__main__":
    run_terraform()
    vm_ip = get_vm_ip()
    install_dependencies(vm_ip)
