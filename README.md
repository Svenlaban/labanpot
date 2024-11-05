
# LabanPot v0.2

LabanPot is a simple multi-protocol honeypot designed to monitor and log login attempts for FTP, SSH, Telnet, and RDP services. It captures usernames and passwords used in attempted logins and displays connection attempts in real-time within the terminal, allowing for easy monitoring of suspicious activity.

## Features

- **Real-time logging** of connection attempts, usernames, and passwords in the terminal.
- **Multi-protocol support**: Supports FTP, SSH, Telnet, and RDP protocols.
- **File-based logging** of attempted usernames and passwords, with a counter that tracks how many times each username or password was attempted.
- **Simulated responses** to mimic real servers, deterring attackers and gathering information on their actions.
- **Lightweight and simple design**, easy to run in a terminal on a Linux server.

## Installation

Clone the repository from GitHub and navigate to the directory:

```bash
git clone https://github.com/Svenlaban/labanpot.git
cd labanpot
```

## Usage

1. **Run the honeypot** using root privileges (required to bind to standard ports):
   ```bash
   sudo python3 labanpot.py
   ```
2. **Observe activity** in the terminal. All attempted usernames and passwords will be logged in real-time, and also saved to `usernames.txt` and `passwords.txt` with the count of each attempt.

## Services

LabanPot currently supports the following protocols:
- **FTP**: Listens on port 21.
- **SSH**: Listens on port 22.
- **Telnet**: Listens on port 23.
- **RDP**: Listens on port 3389.

Each service responds with messages similar to those of actual servers, which can help deter attackers or collect more information about their intentions.

## Files Created

- `usernames.txt` - Logs all attempted usernames across all protocols along with the count of each attempt.
- `passwords.txt` - Logs all attempted passwords across all protocols along with the count of each attempt.

## Example Output

When running the honeypot, you will see output similar to the following:
```
========================================
          LabanPot v0.2
    A Simple Multi-Protocol Honeypot
========================================

[2024-11-05 20:43:42] Starting FTP honeypot...
[2024-11-05 20:43:42] FTP honeypot is running on port 21...
[2024-11-05 20:43:43] Starting SSH honeypot...
[2024-11-05 20:43:43] SSH honeypot is running on port 22...
[2024-11-05 20:43:44] Connection from: 192.168.1.100:51234 on FTP
[2024-11-05 20:43:45] Attempted login with username: admin on FTP
[2024-11-05 20:43:46] Attempted login with password: password123 on FTP
```

## Security Note

This honeypot is intended for educational and monitoring purposes. Running a honeypot can attract unwanted attention and should be deployed with caution. Always ensure you are complying with legal and ethical guidelines when using this tool.

## License

This project is licensed under the MIT License.
