import os
import sys
import subprocess

class VirtualEnvironment:
    """Handles virtual environment creation, activation, and package installation."""

    def __init__(self, env_name="my_env", requirements_file="xrequirements.txt"):
        self.env_name = env_name
        self.requirements_file = requirements_file
        self.python_exec = sys.executable  # Uses the current Python version
        self.env_path = os.path.join(os.getcwd(), self.env_name)
        self.pip_exec = os.path.join(self.env_path, "bin", "pip") if sys.platform != "win32" else os.path.join(self.env_path, "Scripts", "pip.exe")
        self.python_bin = os.path.join(self.env_path, "bin", "python") if sys.platform != "win32" else os.path.join(self.env_path, "Scripts", "python.exe")

    def create_env(self):
        """Create the virtual environment if it doesn't exist."""
        if not os.path.exists(self.env_path):
            print("Creating virtual environment...")
            subprocess.run([self.python_exec, "-m", "venv", self.env_path], check=True)
            print("Virtual environment created.")
        else:
            print("Virtual environment already exists.")

    def install_requirements(self):
        """Install dependencies from xrequirements.txt inside the virtual environment."""
        if not os.path.exists(self.requirements_file):
            print(f"ERROR: {self.requirements_file} not found! Exiting.")
            sys.exit(1)

        print(f"Installing dependencies from {self.requirements_file}...")
        subprocess.run([self.pip_exec, "install", "--upgrade", "pip"], check=True)  # Upgrade pip
        subprocess.run([self.pip_exec, "install", "-r", self.requirements_file], check=True)
        print("All dependencies installed.")

    def setup_and_run(self):
        """Ensure the virtual environment is set up and then return control to Main.py."""
        self.create_env()
        self.install_requirements()

        # Overwrite sys.executable to force using the virtual environment's Python
        os.environ["VIRTUAL_ENV"] = self.env_path
        os.environ["PATH"] = f"{os.path.join(self.env_path, 'bin')}:{os.environ['PATH']}"
        sys.executable = self.python_bin
