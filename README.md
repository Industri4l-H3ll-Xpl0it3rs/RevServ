# RevServ

cr34t3d by [infrar3d](https://github.com/Infrar3dd)

Automated server preparation script for reverse shell operations and remote access.

This script bootstraps a fresh Debian/Ubuntu-based server and prepares it for reverse shell usage by:

- Installing essential tools
- Configuring SSH access
- Creating a privileged user (optional)
- Setting up firewall rules (UFW)
- Opening a listener port (default: 4444)

Designed for red teamers, pentesters, and bug bounty hunters who need a quick and repeatable environment setup.

## Usage

```bash
chmod +x revserv.py
sudo ./revserv.py
```

or

```bash
python3 revserv.py
```

## Features

- Base tools installation (`curl`, `wget`, `git`, `net-tools`, etc.)
- Optional creation of a new sudo user
- SSH hardening:
  - Disable root login
  - Enable password authentication
- UFW firewall configuration:
  - Allow SSH (22/tcp)
  - Allow reverse shell port (4444/tcp)
- One-command setup

## Requirements

- Debian/Ubuntu-based system
- Root privileges

### ⚠️ Disclaimer ⚠️

This software and proof-of-concept code is provided **for educational and research purposes only**. 

*   The authors are **not responsible** for any misuse or damage caused by this program.
*   **Do not use** against any systems without explicit **prior permission**.
*   Use of this tools for attacking targets without consent is **illegal**.

You are responsible for obeying all applicable laws. **Use ethically and responsibly.**
