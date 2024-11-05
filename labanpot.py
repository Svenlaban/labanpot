import socket
import os
import threading
from datetime import datetime

HOST = '0.0.0.0'  # Listen on all network interfaces
BUFFER_SIZE = 1024

# Log file names for different protocols
USER_FILE = 'usernames.txt'
PASS_FILE = 'passwords.txt'

def display_banner():
    """Display a graphical banner in the terminal on startup."""
    print("\n" + "="*40)
    print("          LabanPot v0.2")
    print("    A Simple Multi-Protocol Honeypot")
    print("="*40 + "\n")

def log_event(message):
    """Log and display activity in the terminal."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] {message}')

def log_to_file(filename, data):
    """Log usernames or passwords to a file with a counter."""
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            pass  # Create the file if it doesn't exist

    # Read the current data from the file
    found = False
    lines = []
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Update the counter if data already exists in the file
    for i, line in enumerate(lines):
        if line.startswith(data):
            count = int(line.strip().split(' ')[1]) + 1
            lines[i] = f'{data} {count}\n'
            found = True
            break

    # If data wasn't found, add a new line with counter = 1
    if not found:
        lines.append(f'{data} 1\n')

    # Write all lines back to the file
    with open(filename, 'w') as f:
        f.writelines(lines)

def start_ftp_honeypot():
    """Start a simple FTP honeypot."""
    log_event("Starting FTP honeypot...")
    start_honeypot(port=21, welcome_message="220 (vsFTPd 3.0.3)\n", protocol="FTP")

def start_ssh_honeypot():
    """Start a simple SSH honeypot."""
    log_event("Starting SSH honeypot...")
    start_honeypot(port=22, welcome_message="SSH-2.0-OpenSSH_7.9p1 Debian-10\n", protocol="SSH")

def start_telnet_honeypot():
    """Start a simple Telnet honeypot."""
    log_event("Starting Telnet honeypot...")
    start_honeypot(port=23, welcome_message="Welcome to Telnet\n", protocol="Telnet")

def start_rdp_honeypot():
    """Start a simple RDP honeypot."""
    log_event("Starting RDP honeypot...")
    start_honeypot(port=3389, welcome_message="RDP Server 6.1.7601\n", protocol="RDP")

def start_honeypot(port, welcome_message, protocol):
    """Generic honeypot function to handle multiple protocols."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, port))
    server_socket.listen(1)
    
    log_event(f'{protocol} honeypot is running on port {port}...')

    while True:
        # Wait for a connection from the client
        client_socket, client_address = server_socket.accept()
        log_event(f'{protocol} connection from: {client_address[0]}:{client_address[1]}')

        try:
            # Send a welcome message to simulate the server response
            client_socket.sendall(welcome_message.encode('utf-8'))

            username = None
            password = None

            while True:
                # Receive data from the client
                data = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
                if not data:
                    break

                log_event(f'{protocol} data from {client_address[0]}: {data}')

                # Check if the client is sending a username
                if data.upper().startswith('USER'):
                    username = data.split(' ')[1]
                    log_event(f'{protocol} attempted login with username: {username}')
                    log_to_file(USER_FILE, f"{protocol}_USER: {username}")
                    client_socket.sendall('331 Please specify the password.\n'.encode('utf-8'))

                # Check if the client is sending a password
                elif data.upper().startswith('PASS'):
                    password = data.split(' ')[1]
                    log_event(f'{protocol} attempted login with password: {password}')
                    log_to_file(PASS_FILE, f"{protocol}_PASS: {password}")
                    client_socket.sendall('530 Login incorrect.\n'.encode('utf-8'))

                # If the client sends "QUIT", close the connection
                elif 'QUIT' in data.upper():
                    log_event(f'{protocol} client disconnected: {client_address[0]}')
                    break

                # Handle other commands with a generic response
                else:
                    client_socket.sendall('530 User not logged in\n'.encode('utf-8'))

        except Exception as e:
            log_event(f'{protocol} error: {e}')
        finally:
            client_socket.close()

if __name__ == '__main__':
    display_banner()

    # Start each honeypot in a separate thread
    threads = [
        threading.Thread(target=start_ftp_honeypot),
        threading.Thread(target=start_ssh_honeypot),
        threading.Thread(target=start_telnet_honeypot),
        threading.Thread(target=start_rdp_honeypot),
    ]

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
