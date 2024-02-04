import sys
import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def encrypt_data(key, iv, data):
    """
    Encrypts data using AES encryption in CBC mode.

    Parameters:
    - key: The secret key used for encryption.
    - iv: The initialization vector for encryption.
    - data: The plaintext data to be encrypted.

    Returns:
    - The encrypted data.
    """
    cipher = AES.new(key, AES.MODE_CBC, iv)  # Create a new AES cipher object
    return cipher.encrypt(pad(data, AES.block_size))  # Pad and encrypt the data


def send_file(client_socket, filepath, key, iv):
    """
    Encrypts and sends a file to the server.

    Parameters:
    - client_socket: The socket object used to communicate with the server.
    - filepath: The path to the file to be sent.
    - key: The secret key used for encryption.
    - iv: The initialization vector for encryption.
    """
    with open(filepath, "rb") as file:  # Open the file in binary read mode
        while True:
            bytes_read = file.read(
                1024 - (1024 % AES.block_size)
            )  # Read the file in chunks
            if not bytes_read:
                break  # Break the loop if end of file is reached
            encrypted_data = encrypt_data(key, iv, bytes_read)  # Encrypt the chunk
            client_socket.sendall(encrypted_data)  # Send the encrypted chunk


def client_program():
    """
    Main client program to handle file encryption and sending.
    """
    # Ensure the correct number of command-line arguments
    if len(sys.argv) != 6:
        print(
            "Usage: python client_files.py <ip_address> <port> <key_hex> <iv_hex> <filepath>"
        )
        sys.exit(1)

    # Parse command-line arguments
    host = sys.argv[1]
    port = int(sys.argv[2])
    key_hex = sys.argv[3]
    iv_hex = sys.argv[4]
    filepath = sys.argv[5]

    # Convert hexadecimal key and IV to bytes
    key = bytes.fromhex(key_hex)
    iv = bytes.fromhex(iv_hex)

    # Establish a socket connection to the server
    client_socket = socket.socket()
    print(f"Connecting to {host}:{port}")
    client_socket.connect((host, port))

    # Send the filename to the server as a preamble to file transfer
    filename = filepath.split("/")[-1]  # Extract the filename from the filepath
    client_socket.send(filename.encode())  # Encode and send the filename

    # Start the file transfer
    print("Sending file...")
    send_file(client_socket, filepath, key, iv)  # Encrypt and send the file
    print("File has been encrypted and sent successfully.")

    # Close the socket connection
    client_socket.close()


if __name__ == "__main__":
    client_program()
