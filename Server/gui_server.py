import tkinter

# customtkinter for GUI customization
import customtkinter

# tkinter.END and tkinter.messagebox for GUI interaction
from tkinter import END, messagebox

# subprocess used to run external processes: Python scripts
import subprocess

# os is used for getting the script directory
import os

# Crypto.Cipher is used for AES encryption
from Crypto.Cipher import AES

# Crypto.Random used for generating random bytes
from Crypto.Random import get_random_bytes

# Crypto.Util.Padding used for padding and unpadding data during encryption/decryption
from Crypto.Util.Padding import unpad

# Get the directory of the currently running script
script_directory = os.path.dirname(__file__)

# CustomTkinter - System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


# Introductory frame for the GUI
class Intro_Frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.welcome_message = customtkinter.CTkLabel(
            self,
            text="Welcome to your new Remote Access Software! \n\n Server Side",
            font=("Roboto", 50),
        )
        self.welcome_message.grid(
            row=0, column=0, padx=10, pady=(10, 50), sticky="nesw"
        )

        intro_text = (
            "Sharing will work on the same local network.\n"
            "In case of external software, set up your own VPN using Open-source Software like Outline.\n"
            "* Mandatory to execute any Script.\n"
            "** Mandatory to execute screen sharing Script.\n"
            "*** Mandatory to execute file sharing Script.\n\n"
        )

        self.check = customtkinter.CTkLabel(
            self,
            text=intro_text,
            font=("Roboto", 30),
        )
        self.check.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nesw")

        how_to_title = customtkinter.CTkLabel(
            self, text="How it works?\n\n", font=("Roboto", 40, "underline")
        )
        how_to_title.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nesw")

        instructions_text = (
            "1. Choose the IP Address and the Port number for your server.\n\n"
            "2. Write them down in the text fields.\n\n"
            "3. For screen sharing: Choose what screen you want to share. NB: The index screen number always begins with 0. Click then on start monitoring.\n\nFor file sharing: Click on receive file. Set the save path. And then copy the key and the IV and send them to the client.\n\n"
            "4. You are done!"
        )

        self.instructions = customtkinter.CTkLabel(
            self,
            text=instructions_text,
            font=("Roboto", 20),
        )
        self.instructions.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="nesw")


# Frame for accessing the server with various options
class Access_Frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Labels for IP address, port number, and screen index
        labels = [
            "*Server's IP Address:",
            "*Port number:",
            "**Screen Index Number:",
            "***Save Path:",
        ]

        self.label_widgets = []

        # Label widgets for each label text
        for i, label_text in enumerate(labels):
            label = customtkinter.CTkLabel(self, text=label_text, font=("Roboto", 20))
            label.grid(row=i * 2, column=0, padx=0, pady=10, sticky="nesw")
            self.label_widgets.append(label)

        entry_placeholder_texts = [
            "Enter the IP Address for your server:",
            "Enter the Port number:",
            "Screen index begins with 0",
            "Enter the save path for received files:",
        ]

        self.entry_widgets = []

        # Entry widgets with placeholder text for user input
        for i, placeholder_text in enumerate(entry_placeholder_texts):
            entry = customtkinter.CTkEntry(
                self,
                placeholder_text=placeholder_text,
                font=("Roboto", 20),
                width=350,
                height=40,
            )
            entry.grid(row=i * 2 + 1, column=0, padx=0, pady=0, sticky="nesw")
            self.entry_widgets.append(entry)

        # Buttons for starting monitoring, receiving files, copying keys/IV, and clearing fields
        self.button_connect = customtkinter.CTkButton(
            self,
            text="Start Monitoring",
            height=50,
            width=100,
            font=("Roboto", 20),
            command=self.start_monitoring,
        )
        self.button_connect.grid(row=11, column=0, padx=0, pady=20, sticky="nesw")

        self.button_receive_file = customtkinter.CTkButton(
            self,
            text="Receive File",
            height=50,
            width=100,
            font=("Roboto", 20),
            command=self.receive_file,
        )
        self.button_receive_file.grid(
            row=12, column=0, padx=0, pady=(0, 20), sticky="nesw"
        )

        self.copy_key_button = customtkinter.CTkButton(
            self,
            text="Copy Key",
            height=50,
            width=100,
            font=("Roboto", 20),
            command=self.copy_key_to_clipboard,
        )
        self.copy_key_button.grid(row=18, column=0, padx=0, pady=(0, 20), sticky="nesw")

        self.copy_iv_button = customtkinter.CTkButton(
            self,
            text="Copy IV",
            height=50,
            width=100,
            font=("Roboto", 20),
            command=self.copy_iv_to_clipboard,
        )
        self.copy_iv_button.grid(row=19, column=0, padx=0, pady=(0, 20), sticky="nesw")

        self.clear_button = customtkinter.CTkButton(
            self,
            text="Clear Fields",
            height=50,
            width=100,
            font=("Roboto", 20),
            command=self.clear,
        )
        self.clear_button.grid(row=20, column=0, padx=0, pady=5)

        # Labels for displaying generated AES key and IV
        self.generated_key_label = customtkinter.CTkLabel(
            self,
            text="Generated AES Key:",
            font=("Roboto", 20),
        )
        self.generated_key_label.grid(
            row=14, column=0, padx=0, pady=(20, 0), sticky="nesw"
        )

        self.generated_key_value = customtkinter.CTkLabel(
            self,
            text="",
            font=("Roboto", 20),
        )
        self.generated_key_value.grid(row=15, column=0, padx=0, pady=10, sticky="nesw")

        self.generated_iv_label = customtkinter.CTkLabel(
            self,
            text="Generated IV:",
            font=("Roboto", 20),
        )
        self.generated_iv_label.grid(row=16, column=0, padx=0, pady=10, sticky="nesw")

        self.generated_iv_value = customtkinter.CTkLabel(
            self,
            text="",
            font=("Roboto", 20),
        )
        self.generated_iv_value.grid(
            row=17, column=0, padx=0, pady=(0, 20), sticky="nesw"
        )

    # Function to start monitoring
    def start_monitoring(self):
        ip_address, port_number, screen_index, *_ = [
            entry.get() for entry in self.entry_widgets
        ]

        if ip_address and port_number and screen_index:
            try:
                # Full path to server.py in the same directory
                server_py_path = os.path.join(script_directory, "server.py")
                subprocess.Popen(
                    ["python", server_py_path, ip_address, port_number, screen_index],
                    shell=True,
                )
                messagebox.showinfo(
                    "Success",
                    "Monitoring start instruction sent successfully!\n Check your terminal.",
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start monitoring: {str(e)}")
        else:
            messagebox.showerror("Error", "Please enter all required fields.")

    # Function to receive files
    def receive_file(self):
        ip_address, port_number, _, save_path = [
            entry.get() for entry in self.entry_widgets
        ]

        if ip_address and port_number and save_path:
            try:
                server_files_py_path = os.path.join(script_directory, "server_files.py")
                key, iv = generate_key_iv()
                subprocess.Popen(
                    [
                        "python",
                        server_files_py_path,
                        ip_address,
                        port_number,
                        key.hex(),
                        iv.hex(),
                        save_path,
                    ],
                    shell=True,
                )
                messagebox.showinfo(
                    "Success",
                    "File receiving started successfully!\n Check your terminal for generated keys.",
                )
                self.generated_key_value.configure(text=f"{key.hex()}")
                self.generated_iv_value.configure(text=f"{iv.hex()}")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to start file receiving: {str(e)}"
                )
        else:
            messagebox.showerror(
                "Error", "Please enter IP Address, Port, and Save Path."
            )

    # Function to copy AES key to clipboard
    def copy_key_to_clipboard(self):
        key_value = self.generated_key_value.cget("text")
        if key_value:
            self.master.clipboard_clear()  # Delete Clipboard
            self.master.clipboard_append(key_value)  # Copy Key Value
            self.master.update()  # Update Clipboard
            messagebox.showinfo("Success", "AES Key copied to clipboard!")

    # Function to copy IV to clipboard
    def copy_iv_to_clipboard(self):
        iv_value = self.generated_iv_value.cget("text")
        if iv_value:
            self.master.clipboard_clear()
            self.master.clipboard_append(iv_value)
            self.master.update()
            messagebox.showinfo("Success", "IV copied to clipboard!")

    # Function to clear input fields
    def clear(self):
        for entry in self.entry_widgets:
            entry.delete(0, END)


# Function to generate AES key and IV
def generate_key_iv():
    key = get_random_bytes(16)  # AES-128
    iv = get_random_bytes(16)  # IV for CBC mode
    return key, iv


# Main application class
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Server - Remote Access Software")
        self.geometry("1920x1080")

        self.frame1 = Intro_Frame(self)
        self.frame1.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nesw")
        self.frame1.configure(fg_color="transparent")

        self.frame2 = Access_Frame(self)
        self.frame2.grid(row=0, column=1, padx=(10, 0), pady=(10, 0), sticky="nesw")
        self.frame2.configure(fg_color="transparent")


app = App()
app.mainloop()
