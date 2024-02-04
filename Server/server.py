import socket  # Socket library for network communication
import threading  # Threading for concurrent client handling
import cv2  # OpenCV for image processing
import struct  # Struct for handling binary data
import numpy as np  # NumPy for numerical operations on images
from mss import mss  # mss library for screen capture
from screeninfo import (
    get_monitors,
)  # get_monitors for monitor information retrieval
import sys  # sys for command-line arguments


# Function to capture the screen specified by its number
def capture_screen(screen_number):
    monitors = get_monitors()  # Retrieve information about available monitors
    if screen_number >= len(monitors):  # Check if the specified screen number is valid
        raise ValueError("Screen number out of range.")
    monitor = monitors[screen_number]  # Get information about the specified monitor

    # Capture a screenshot of the specified monitor
    with mss() as sct:
        monitor_region = {
            "top": monitor.y,
            "left": monitor.x,
            "width": monitor.width,
            "height": monitor.height,
        }
        sct_img = sct.grab(monitor_region)  # Capture the screen region
        frame = np.array(
            sct_img
        )  # Convert the screenshot to a NumPy array to avoid software crashing
        frame = cv2.cvtColor(
            frame, cv2.COLOR_BGRA2BGR
        )  # Convert from Blue-Green-Red-Alpha to Blue-Green-Red color format
        return frame  # Return the captured screen as a BGR image


# Function to handle each client connection in a separate thread
def client_thread(conn, addr, screen_number):
    try:
        while True:
            frame = capture_screen(screen_number)  # Capture the current screen frame

            # Encode the captured frame as JPEG , change the quality to reduce the size of the frame
            # Control the quality of the frame - Default Value is 80%
            _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])

            # Send the size of the frame to the client in a binary format
            size = len(buffer)
            conn.sendall(struct.pack(">L", size))

            # Send the frame data to the client
            conn.sendall(buffer)

    except Exception as e:
        print(f"Error on screen {screen_number}: {e}")
    finally:
        conn.close()  # Close the client connection when done


# Function to start the server for a specific screen
def start_server_for_screen(host, port, screen_number):
    server_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    )  # Create a socket object

    try:
        server_socket.bind(
            (host, port)
        )  # Bind the server socket to the specified host and port
        server_socket.listen(
            5
        )  # Listen for incoming connections (up to 5 queued connections)
        print(f"Server for screen {screen_number} listening on {host}:{port}")

        while True:
            conn, addr = server_socket.accept()  # Accept a new client connection
            print("Connection from:", addr)

            # Start a new thread to handle the client
            threading.Thread(
                target=client_thread, args=(conn, addr, screen_number)
            ).start()

    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()  # Close the server socket when done


# Entry point of the program
if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python server.py <IP address> <Port> <Screen Index>")
        sys.exit(1)

    host = sys.argv[1]  # Retrieve the IP address from arguments
    port = int(sys.argv[2])  # Retrieve the port number from arguments
    screen_number = int(sys.argv[3])  # Retrieve the screen index from arguments

    # Start the server for the specified screen
    start_server_for_screen(host, port, screen_number)
