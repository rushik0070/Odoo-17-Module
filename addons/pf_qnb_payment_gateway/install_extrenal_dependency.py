# install_dependencies.py
import subprocess
import sys

def install_simplifycommerce():
    try:
        # Attempt to install the simplifycommerce package
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'simplify'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'matplotlib'])
        print("simplifycommerce package installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install simplifycommerce: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    install_simplifycommerce()
