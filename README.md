
# LabanPot v0.1

LabanPot is a simple FTP honeypot designed to monitor and log FTP login attempts, including usernames and passwords, made by potential attackers. It displays connection attempts in real-time within the terminal, allowing for easy monitoring of suspicious activity.

## Features

- **Real-time logging** of connection attempts, usernames, and passwords in the terminal.
- **File-based logging** of attempted usernames and passwords, with a counter that tracks how many times each username or password was attempted.
- **Simulated FTP responses** to mimic a real FTP server, deterring attackers and gathering more information on their actions.
- **Lightweight and simple design**, easy to run in a terminal on a Linux server.

## Installation

Clone the repository from GitHub and navigate to the directory:

```bash
git clone https://github.com/Svenlaban/labanpot.git
cd labanpot
```

## Usage

1. **Run the honeypot** using root privileges (required for FTP on port 21):
   ```bash
   sudo python3 labanpot.py
   ```
2. **Observe activity** in the terminal. All attempted usernames and passwords will be logged in real-time, and also saved to `usernames.txt` and `passwords.txt` with the count of each attempt.

## Files Created

- `usernames.txt` - Logs all attempted usernames along with the count of each attempt.
- `passwords.txt` - Logs all attempted passwords along with the count of each attempt.

## Example Output

When running the honeypot, you will see output similar to the following:
```
========================================
          LabanPot v0.1
     A Simple FTP Honeypot
========================================

[2024-11-04 12:34:56] FTP honeypot is running on port 21...
[2024-11-04 12:35:02] Connection from: 192.168.1.100:51234
[2024-11-04 12:35:03] Attempted login with username: admin
[2024-11-04 12:35:04] Attempted login with password: password123
```

## Security Note

This honeypot is intended for educational and monitoring purposes. Running a honeypot can attract unwanted attention and should be deployed with caution. Always ensure you are complying with legal and ethical guidelines when using this tool.
