import os
import threading
import socket
from datetime import datetime
import logging
import requests
from impacket import smbserver

# Network configuration constants
HOST = '0.0.0.0'
BUFFER_SIZE = 1024

# Log files for different protocols
USER_FILE = 'usernames.txt'
PASS_FILE = 'passwords.txt'
RDP_LOG_FILE = 'rdp_connections_log.txt'
SMB_LOG_FILE = 'smb_connections_log.txt'
SSH_LOG_FILE = 'ssh_connections_log.txt'
IP_LOG_FILE = 'ip_log.txt'  # Unified IP log file for all services
TELNET_COMMANDS_LOG_FILE = 'telnet_commands_log.txt'

# Set logging level for requests to avoid debug logs
logging.getLogger("requests").setLevel(logging.WARNING)

def display_banner():
    """Display a banner in the terminal on startup."""
    print("\n" + "="*40)
    print("          LabanPot v0.4")
    print("    A Simple Multi-Protocol Honeypot")
    print("="*40 + "\n")

def log_event(message):
    """Log and display activity in the terminal."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] {message}')

def log_to_file(filename, data):
    """Log data to a specified file."""
    with open(filename, 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {data}\n")

def get_country(ip_address):
    """Retrieve the country for a given IP address using ipinfo.io without API key."""
    try:
        response = requests.get(f"http://ipinfo.io/{ip_address}/json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("country", "Unknown")
        else:
            log_event(f"Could not retrieve data for IP: {ip_address}")
            return "Unknown"
    except requests.exceptions.Timeout:
        log_event(f"Timeout reached for IP lookup: {ip_address}")
        return "Unknown"
    except requests.exceptions.RequestException as e:
        log_event(f"Error retrieving country for IP {ip_address}: {e}")
        return "Unknown"

def log_ip(ip_address, protocol):
    """Log IP addresses with country information to a unified IP log file."""
    country = get_country(ip_address)
    log_data = f"{ip_address},{country},{protocol}"
    log_to_file(IP_LOG_FILE, log_data)
    log_event(f"IP logged: {ip_address} from {country} on {protocol}")

def start_ftp_honeypot():
    """Start a basic FTP honeypot."""
    log_event("Starting FTP honeypot...")
    start_honeypot(port=21, welcome_message="220 (vsFTPd 3.0.3)\n", protocol="FTP")

def start_ssh_honeypot():
    """Start an SSH honeypot that logs raw data and connection attempts."""
    log_event("Starting SSH honeypot...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, 22))
    server_socket.listen(1)

    log_event('SSH honeypot is running on port 22...')

    while True:
        client_socket, client_address = server_socket.accept()
        log_event(f'SSH connection from: {client_address[0]}:{client_address[1]}')
        log_ip(client_address[0], "SSH")  # Log IP for SSH with country
        log_to_file(SSH_LOG_FILE, f'Connection from {client_address[0]}:{client_address[1]}')

        try:
            while True:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break

                # Try decoding data as text, otherwise log as hexadecimal
                try:
                    decoded_data = data.decode('utf-8').strip()
                    log_event(f'SSH data from {client_address[0]}: {decoded_data}')
                    log_to_file(SSH_LOG_FILE, f'Data from {client_address[0]}: {decoded_data}')
                except UnicodeDecodeError:
                    hex_data = data.hex()
                    log_event(f'SSH raw data from {client_address[0]}: {hex_data}')
                    log_to_file(SSH_LOG_FILE, f'Raw data from {client_address[0]}: {hex_data}')

        except Exception as e:
            log_event(f'SSH error: {e}')
            log_to_file(SSH_LOG_FILE, f'Error from {client_address[0]}: {e}')
        finally:
            client_socket.close()

def start_telnet_honeypot():
    """Start a basic Telnet honeypot that logs commands."""
    log_event("Starting Telnet honeypot...")
    
    # Set up a Telnet-specific honeypot server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, 23))
    server_socket.listen(1)
    
    log_event('Telnet honeypot is running on port 23...')

    while True:
        client_socket, client_address = server_socket.accept()
        log_event(f'Telnet connection from: {client_address[0]}:{client_address[1]}')
        log_ip(client_address[0], "Telnet")  # Log IP for Telnet with country
        log_to_file(TELNET_COMMANDS_LOG_FILE, f'Connection from {client_address[0]}:{client_address[1]}')

        try:
            client_socket.sendall("Welcome to Telnet\n".encode('utf-8'))

            while True:
                # Receive data from the client
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break

                # Try decoding data as UTF-8, log as hex if decoding fails
                try:
                    decoded_data = data.decode('utf-8').strip()
                    log_event(f'Telnet command from {client_address[0]}: {decoded_data}')
                    log_to_file(TELNET_COMMANDS_LOG_FILE, f'Command from {client_address[0]}: {decoded_data}')
                except UnicodeDecodeError:
                    hex_data = data.hex()
                    log_event(f'Telnet raw data from {client_address[0]}: {hex_data}')
                    log_to_file(TELNET_COMMANDS_LOG_FILE, f'Raw data from {client_address[0]}: {hex_data}')

                # Send a generic response to each command
                client_socket.sendall('Command received\n'.encode('utf-8'))

        except Exception as e:
            log_event(f'Telnet error: {e}')
            log_to_file(TELNET_COMMANDS_LOG_FILE, f'Error from {client_address[0]}: {e}')
        finally:
            client_socket.close()

def start_rdp_honeypot():
    """Start a basic RDP honeypot that logs connection attempts and raw data."""
    log_event("Starting RDP honeypot...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, 3389))
    server_socket.listen(1)

    log_event('RDP honeypot is running on port 3389...')

    while True:
        client_socket, client_address = server_socket.accept()
        log_event(f'RDP connection from: {client_address[0]}:{client_address[1]}')
        log_ip(client_address[0], "RDP")  # Log IP for RDP with country
        log_to_file(RDP_LOG_FILE, f'Connection from {client_address[0]}:{client_address[1]}')

        try:
            while True:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break

                # Log raw data from RDP connection as hexadecimal in RDP log
                hex_data = data.hex()
                log_event(f'RDP raw data from {client_address[0]}: {hex_data}')
                log_to_file(RDP_LOG_FILE, f'Raw data from {client_address[0]}: {hex_data}')

        except Exception as e:
            log_event(f'RDP error: {e}')
            log_to_file(RDP_LOG_FILE, f'Error from {client_address[0]}: {e}')
        finally:
            client_socket.close()

def start_smb_honeypot():
    """Start a basic SMB honeypot that logs connection attempts."""
    log_event("Starting SMB honeypot...")
    server = smbserver.SimpleSMBServer()
    server.addShare("SHARE", "/tmp", "Honeypot SMB Share")
    
    # Remove automatic logging to avoid unnecessary log creation
    # server.setLogFile(SMB_LOG_FILE)  # Comment out to avoid immediate log creation

    log_event("SMB honeypot is running on port 445...")

    # Start the SMB server
    server.start()

    # Manually log connections as they happen
    while True:
        try:
            # Wait for an actual connection to log it manually
            client_socket, client_address = server.accept()
            log_event(f'SMB connection from: {client_address[0]}:{client_address[1]}')
            log_ip(client_address[0], "SMB")  # Log IP for SMB with country
            log_to_file(SMB_LOG_FILE, f'Connection from {client_address[0]}:{client_address[1]}')
            client_socket.close()
        except Exception as e:
            log_event(f'SMB error: {e}')
            break

def start_honeypot(port, welcome_message, protocol):
    """Generic honeypot function for FTP, SSH, and Telnet."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, port))
    server_socket.listen(1)
    
    log_event(f'{protocol} honeypot is running on port {port}...')

    while True:
        client_socket, client_address = server_socket.accept()
        log_event(f'{protocol} connection from: {client_address[0]}:{client_address[1]}')
        log_ip(client_address[0], protocol)  # Log IP with country

        try:
            client_socket.sendall(welcome_message.encode('utf-8'))

            while True:
                data = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
                if not data:
                    break

                log_event(f'{protocol} data from {client_address[0]}: {data}')

                if data.upper().startswith('USER'):
                    username = data.split(' ')[1]
                    log_event(f'{protocol} attempted login with username: {username}')
                    log_to_file(USER_FILE, f"{protocol}_USER: {username}")
                    client_socket.sendall('331 Please specify the password.\n'.encode('utf-8'))

                elif data.upper().startswith('PASS'):
                    password = data.split(' ')[1]
                    log_event(f'{protocol} attempted login with password: {password}')
                    log_to_file(PASS_FILE, f"{protocol}_PASS: {password}")
                    client_socket.sendall('530 Login incorrect.\n'.encode('utf-8'))

                elif 'QUIT' in data.upper():
                    log_event(f'{protocol} client disconnected: {client_address[0]}')
                    break
                else:
                    client_socket.sendall('530 User not logged in\n'.encode('utf-8'))

        except Exception as e:
            log_event(f'{protocol} error: {e}')
        finally:
            client_socket.close()

def get_user_selection():
    """Prompt the user to select which honeypot services to start."""
    services = {
        '1': ("FTP", start_ftp_honeypot),
        '2': ("SSH", start_ssh_honeypot),
        '3': ("Telnet", start_telnet_honeypot),
        '4': ("RDP", start_rdp_honeypot),
        '5': ("SMB", start_smb_honeypot),
    }
    
    print("Select the services to run (e.g., 1,3,5):")
    for key, (name, _) in services.items():
        print(f"{key}: {name}")

    choice = input("Enter your choices: ").split(',')
    selected_services = [services[c.strip()][1] for c in choice if c.strip() in services]

    return selected_services

if __name__ == '__main__':
    display_banner()
    
    selected_services = get_user_selection()
    
    # Start each selected honeypot service in a separate thread
    threads = [threading.Thread(target=service) for service in selected_services]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
