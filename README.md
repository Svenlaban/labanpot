
# LabanPot v0.4

LabanPot is a simple multi-protocol honeypot designed to monitor and log login attempts for several services, including FTP, SSH, Telnet, RDP, and SMB. It captures and logs incoming IP addresses along with their country of origin and logs login attempts, raw data, and connection information.

## Features

- **Multi-protocol support**: Supports FTP, SSH, Telnet, RDP, and SMB protocols.
- **Real-time logging** of connection attempts, usernames, and passwords in the terminal.
- **Geolocation logging**: Logs IP addresses along with their country of origin using ipinfo.io without an API key.
- **Unified IP logging**: Stores all IP logs in a single `ip_log.txt` file in the format `IP,Country,Service`.
- **Separate logs for each service**: Each protocol has its own dedicated log file for detailed tracking.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Svenlaban/labanpot.git
   cd labanpot
   ```

2. **Install dependencies**:

   Use the `requirements.txt` file to install necessary libraries:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the honeypot with root privileges to bind to standard ports:

```bash
sudo python3 labanpot.py
```

Follow the prompts to select which services to activate.

## Logs and Output

- **ip_log.txt**: Stores all logged IP addresses along with their country of origin and service (e.g., `192.168.1.1,US,FTP`).
- **Dedicated logs** for each protocol (e.g., `ssh_connections_log.txt`, `rdp_connections_log.txt`, etc.) store connection and raw data for deeper analysis.

## Example Output

Running the honeypot produces output similar to:

```
========================================
          LabanPot v0.4
    A Simple Multi-Protocol Honeypot
========================================

[2024-11-06 14:32:52] Starting FTP honeypot...
[2024-11-06 14:32:53] FTP honeypot is running on port 21...
[2024-11-06 14:32:54] SSH connection from: 192.168.1.10:51123
[2024-11-06 14:32:54] IP logged: 192.168.1.10 from US on SSH
[2024-11-06 14:32:55] SSH data from 192.168.1.10: SSH-2.0-OpenSSH_7.4
```

## Security Notice

This honeypot is for educational and monitoring purposes. Running a honeypot can attract unwanted attention and should be deployed with caution. Ensure compliance with legal and ethical guidelines when using this tool.

