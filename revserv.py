#!/usr/bin/env python3
import os
import subprocess
import getpass


print("""
  _____               _____                 
 |  __ \\             / ____|                
 | |__) |_____   __ | (___   ___ _ ____   __
 |  _  // _ \\ \\ / /_ \\___ \\ / _ \\ '__\\ \\ / /
 | | \\ \\  __/\\ V /| |____) |  __/ |   \\ V / 
 |_|  \\_\\___| \\_/_| |_____/_\\___|_|    \\_/  
         / __|/ _ \\ __| | | | '_ \\          
         \\__ \\  __/ |_| |_| | |_) |         
         |___/\\___|\\__|\\__,_| .__/          
                 by infrar3d| |             
                            |_|                                     

    """)


def run(cmd):
    print(f"\n[+] {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def get_user_choice():
    while True:
        response = input("\nCreate a new sudo user? (will be used in ssh) [Y/n]: ").strip().lower()
        
        if response == '':
            return True
        
        if response in ['y', 'yes']:
            return True
        
        if response in ['n', 'no']:
            return False

def install_base_tools():
    print("\n[*] Installing base tools")
    run("apt update")
    run("apt install -y sudo curl wget git ufw openssh-server net-tools gnupg")

def create_user():
    print("\n[*] Creating a new sudo user")

    username = input("Enter new username: ")
    password = getpass.getpass("Enter password: ")

    run(f"useradd -m -s /bin/bash {username}")

    subprocess.run(f"echo {username}:{password} | chpasswd", shell=True, check=True)

    run(f"usermod -aG sudo {username}")

    print(f"[+] User {username} created and added to sudo")

def setup_ssh(additionaluser):
    run("systemctl enable ssh")
    run("systemctl start ssh")
    if additionaluser:
        sshd_config = "/etc/ssh/sshd_config"
        print("\n[*] Configuring SSH")

        with open(sshd_config, "r") as f:
            lines = f.readlines()

        new_lines = []
        found_root = False
        found_pass = False

        for line in lines:
            if line.strip().startswith("PermitRootLogin"):
                new_lines.append("PermitRootLogin no\n")
                found_root = True
            elif line.strip().startswith("PasswordAuthentication"):
                new_lines.append("PasswordAuthentication yes\n")
                found_pass = True
            else:
                new_lines.append(line)

        if not found_root:
            new_lines.append("\nPermitRootLogin no\n")

        if not found_pass:
            new_lines.append("PasswordAuthentication yes\n")

        with open(sshd_config, "w") as f:
            f.writelines(new_lines)

        run("systemctl restart ssh")

        print("[+] SSH configured (root disabled, password enabled)")

def setup_ufw():
    run("ufw default deny incoming")
    run("ufw default allow outgoing")
    run("ufw allow 22/tcp")
    run("ufw allow 4444/tcp")
    run("ufw --force enable")

def main():
    if os.geteuid() != 0:
        print("[-] Run as root")
        return

    install_base_tools()

    additional_user = get_user_choice()
    if additional_user:
        create_user()
    setup_ssh(additional_user)
    setup_ufw()

    print("\n[+] Setup complete!")
    print("\n[!] Reboot recommended: reboot")

if __name__ == "__main__":
    main()