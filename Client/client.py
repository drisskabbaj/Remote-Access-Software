import cv2  #  OpenCV for image processing
import socket  # Socket library for network communication
import struct  # Struct for handling binary data
import tkinter as tk  # Tkinter for creating GUI window
from PIL import Image, ImageTk  # PIL for image manipulation
import numpy as np  # NumPy for numerical operations on images
import sys  # Sys for Clients GUI


# Function to resize a frame to fit target dimensions
def resize_frame(frame, target_width, target_height):
    # Resize the frame to fit the target dimensions from Guis Parameters
    resized_frame = cv2.resize(frame, (target_width, target_height))
    return resized_frame


# Function to receive and display a video stream from a remote server.
def receive_video(host, port, window_width, window_height):
    try:
        # Create a socket object for network communication using the IPv4 protocol (AF_INET)
        # and the TCP transport protocol (SOCK_STREAM).
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the client socket to the specified server using the provided host and port.
        client_socket.connect((host, int(port)))

        # Create a GUI window using the Tkinter library.
        root = tk.Tk()
        root.title("Video Stream")

        # Define the size of the GUI window based on the provided window_width and window_height.
        window_size = f"{window_width}x{window_height}"
        root.geometry(window_size)

        # Create a Tkinter label widget to display the video stream within the GUI window.
        label = tk.Label(root)

        # Pack the label widget with optional padding to position it within the window.
        label.pack(padx=10, pady=10)

        while True:
            # Receive the size of the incoming video frame from the server.
            frame_size_data = client_socket.recv(4)

            # Check if no frame size data is received (indicating the end of the stream).
            if not frame_size_data:
                break

            # Unpack the binary data to retrieve the size of the video frame in bytes.
            frame_size = struct.unpack(">L", frame_size_data)[0]

            # Initialize an empty binary data buffer to store the frame data.
            frame_data = b""

            # Receive the frame data in chunks until the entire frame is received.
            while len(frame_data) < frame_size:
                remaining_size = frame_size - len(frame_data)

                # Receive a chunk of frame data, with a maximum chunk size of 4096 bytes.
                # This ensures that large frames are received in smaller segments.
                frame_data += client_socket.recv(
                    4096 if remaining_size > 4096 else remaining_size
                )

            # Convert the received frame data into a NumPy array of unsigned 8-bit integers.
            nparr = np.frombuffer(frame_data, np.uint8)

            # Decode the NumPy array into a color image/frame using OpenCV.
            frame_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Resize the frame to fit the target dimensions (window_width x window_height).
            frame_np = resize_frame(frame_np, int(window_width), int(window_height))

            # Convert the resized frame into a format suitable for display with Tkinter.
            image = cv2.cvtColor(frame_np, cv2.COLOR_BGR2RGB)
            image = ImageTk.PhotoImage(Image.fromarray(image))

            # Update the Tkinter label with the new frame, allowing real-time display.
            label.config(image=image)
            label.image = image

            # Update the Tkinter GUI to reflect the changes - Update the displayed frame.
            root.update()

    except Exception as e:
        # Handle any exceptions that may occur during the execution of the function.
        print(f"Error: {e}")

    finally:
        # Close the client socket to release network resources.
        client_socket.close()

        # Destroy the Tkinter GUI window when the video stream ends or an error occurs.
        root.destroy()


# Main function
def main():
    if len(sys.argv) != 6:
        print(
            "Usage: python client.py <IP> <Port> <Screen Index> <Window Width> <Window Height>"
        )
        sys.exit(1)

    host = sys.argv[1]  # Retrieve the IP address from Clients GUI
    port = sys.argv[2]  # Retrieve the port number from Clients GUI
    screen_index = sys.argv[3]
    window_width = sys.argv[4]  # Retrieve the target window width from Clients GUI
    window_height = sys.argv[5]  # Retrieve the target window height from Clients GUI

    receive_video(
        host, port, window_width, window_height
    )  # Start receiving and displaying the video stream


if __name__ == "__main__":
    main()
