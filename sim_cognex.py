import random
import socket
import time
from http import client
from pickle import GET


def connect_to_server(host, port):
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            print("Connected to server")
            return client_socket
        except socket.error:
            print("Connection failed. Retrying...")
            time.sleep(5)

def receive_response(client_socket, timeout=0.5):
    """Receive and handle server response"""
    # Set socket to non-blocking with timeout
    client_socket.settimeout(timeout)
    try:
        response = b""
        while True:
            try:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                response += chunk
                # If response is complete, break
                if b"\r\n\r\n" in response and not client_socket.recv(1, socket.MSG_PEEK):
                    break
            except socket.timeout:
                break
        
        if response:
            print("\n----- Server Response -----")
            try:
                # Decode and print the response
                decoded_response = response.decode('utf-8')
                print(decoded_response)
            except UnicodeDecodeError:
                print("Unable to decode response as UTF-8, printing raw bytes:")
                print(response)
            print("-------------------------\n")
        return response
    except socket.error as e:
        print(f"Error receiving response: {e}")
        return b""
    finally:
        # Reset socket to blocking mode
        client_socket.settimeout(None)

def create_put_request(payload):
    """Create a properly formatted PUT request with correct Content-Length header"""
    payload_bytes = payload.encode()
    content_length = len(payload_bytes)
    
    headers = f"""PUT /cognex/onResult/ HTTP/1.1
Host: localhost
User-Agent: cognex
Accept: */*
Connection: keep-alive
Content-Type: application/json
Content-Length: {content_length}

""".encode()
    
    # Combine headers and payload
    return headers + payload_bytes

def create_get_request(payload):
    """Create a properly formatted GET request with payload in URL query string"""

    headers = f"""GET /cognex/onResult/?p={payload} HTTP/1.1
Host: localhost
User-Agent: cognex
Connection: keep-alive

""".encode()

    return headers


def create_head_request():
    """Create a properly formatted HEAD request to keep alive the socket"""

    headers = """HEAD /cognex/onResult/ HTTP/1.1
Host: localhost
User-Agent: cognex
Connection: keep-alive

""".encode()
    
    return headers

#-------------------------------------------------------------------------
# Main function to send requests at specified intervals
#-------------------------------------------------------------------------
def main():
    host = "localhost"
    port = 8000  # Replace with the server port

    client_socket = connect_to_server(host, port)

    send_head_interval = 10  # seconds
    send_get_interval = 23  # seconds
    last_head_time = time.time() - 1000  # Start time in the past to send immediately
    last_get_time = time.time()

    try:
        while True:
            current_time = time.time()

            # Send "head something" every 10 seconds
            if current_time - last_head_time >= send_head_interval:
                try:
                    req = create_head_request()
                    client_socket.sendall(req)
                    print(f"Sent HEAD request ---------------\n{req}")

                    # Handle response after sending HEAD
                    receive_response(client_socket)

                except socket.error:
                    print("Connection lost while sending. Reconnecting...")
                    client_socket = connect_to_server(host, port)
                last_head_time = current_time

            # Send "get blanks" every 23 seconds
            if current_time - last_get_time >= send_get_interval:
                try:
                    nbr = random.randint(0, 1000000)  # Random number for payload
                    payload = f"AV{nbr:06d}4000"  # Format nbr as 6 digits with leading zeros
                    
                    # Create and send a properly formatted GET request
                    get_request = create_get_request(payload)
                    client_socket.sendall(get_request)
                    print(f"Sent GET request -------------\n{get_request}")

                    # Handle response after sending GET
                    receive_response(client_socket)

                except socket.error:
                    print("Connection lost while sending. Reconnecting...")
                    client_socket = connect_to_server(host, port)
                last_get_time = current_time

            # Idle until cancelled
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nCancelled by user. Closing socket.")
        client_socket.close()

if __name__ == "__main__":
    main()
