import os
import socket
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def decrypt_data(key, iv, encrypted_data):
    """
    Decrypts data using AES encryption in CBC mode.

    Parameters:
    - key: The secret key used for decryption.
    - iv: The initialization vector for decryption.
    - encrypted_data: The data to be decrypted.

    Returns:
    - The decrypted data.
    """
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted_data), AES.block_size)


def receive_file(conn, filename, key, iv, save_path):
    """
    Receives a file from the client, decrypts it, and saves it to the specified path.

    Parameters:
    - conn: The connection gateway from the client.
    - filename: The name of the file.
    - key: The secret key used for decryption.
    - iv: The initialization vector for decryption.
    - save_path: The path where the decrypted file will be saved.
    """
    full_path = os.path.join(
        save_path, filename
    )  # Construct the full path for the file
    with open(full_path, "wb") as file:
        while True:
            data = conn.recv(1024)  # Receive data from the client
            if not data:
                break  # Stop if no more data is received
            decrypted_data = decrypt_data(key, iv, data)  # Decrypt the received data
            file.write(decrypted_data)  # Write the decrypted data to the file


def server_program():
    """
    Main server program to handle incoming connections and file transfers.
    """
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 6:
        print(
            "Usage: python server_tcp.py <ip_address> <port> <key_hex> <iv_hex> <save_path>"
        )
        sys.exit(1)

    # Extract command-line arguments from Servers GUI
    ip_address = sys.argv[1]
    port = int(sys.argv[2])
    key_hex = sys.argv[3]
    iv_hex = sys.argv[4]
    save_path = sys.argv[5]

    # Convert hexadecimal key and IV to bytes
    try:
        key = bytes.fromhex(key_hex)
        iv = bytes.fromhex(iv_hex)
    except ValueError:
        print("Invalid hexadecimal key or IV format.")
        sys.exit(1)

    # Create a socket and bind it to the provided IP address and port
    server_socket = socket.socket()
    server_socket.bind((ip_address, port))
    server_socket.listen(2)
    print(f"Server listening on {ip_address}:{port}")

    # Accept a connection
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    # Receive and process files from the client
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break  # Exit loop if no more data is received
        print("Received from user: " + str(data))
        filename = os.path.basename(data)
        receive_file(conn, filename, key, iv, save_path)  # Save the received file
        print("File has been received and decrypted successfully.")

    conn.close()  # Close the connection


if __name__ == "__main__":
    server_program()
