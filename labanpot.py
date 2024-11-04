import socket
import os
from datetime import datetime

HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 21  # FTP port
BUFFER_SIZE = 1024

USER_FILE = 'usernames.txt'
PASS_FILE = 'passwords.txt'

def display_banner():
    """Display a graphical banner in the terminal on startup."""
    print("\n" + "="*40)
    print("          LabanPot v0.1")
    print("     A Simple FTP Honeypot")
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
    display_banner()  # Display the banner at startup

    # Create a socket to listen for incoming connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    
    log_event(f'FTP honeypot is running on port {PORT}...')

    while True:
        # Wait for a connection from the client
        client_socket, client_address = server_socket.accept()
        log_event(f'Connection from: {client_address[0]}:{client_address[1]}')

        try:
            # Send a welcome message as if we're an FTP server
            welcome_message = '220 (vsFTPd 3.0.3)\n'
            client_socket.sendall(welcome_message.encode('utf-8'))

            username = None
            password = None

            while True:
                # Receive data from the client
                data = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
                if not data:
                    break

                log_event(f'Received data from {client_address[0]}: {data}')

                # Check if the client is sending a username
                if data.upper().startswith('USER'):
                    username = data.split(' ')[1]  # Get the username
                    log_event(f'Attempted login with username: {username}')
                    log_to_file(USER_FILE, username)  # Log the username to file
                    client_socket.sendall('331 Please specify the password.\n'.encode('utf-8'))

                # Check if the client is sending a password
                elif data.upper().startswith('PASS'):
                    password = data.split(' ')[1]  # Get the password
                    log_event(f'Attempted login with password: {password}')
                    log_to_file(PASS_FILE, password)  # Log the password to file
                    client_socket.sendall('530 Login incorrect.\n'.encode('utf-8'))

                # If the client sends "QUIT", close the connection
                elif 'QUIT' in data.upper():
                    log_event(f'Client disconnected: {client_address[0]}')
                    break

                # Handle other FTP commands with a generic response
                else:
                    client_socket.sendall('530 User not logged in\n'.encode('utf-8'))

        except Exception as e:
            log_event(f'Error: {e}')
        finally:
            client_socket.close()

if __name__ == '__main__':
    try:
        start_ftp_honeypot()
    except KeyboardInterrupt:
        log_event('FTP honeypot is shutting down.')
