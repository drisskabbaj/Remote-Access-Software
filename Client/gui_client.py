import tkinter
import customtkinter
from tkinter import END, messagebox
import subprocess
import os

# Get the current directory of the script to ensure relative paths work correctly.
script_directory = os.path.dirname(__file__)

# Configure CustomTkinter to use system appearance and set a default color theme.
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class Intro_Frame(customtkinter.CTkFrame):
    """
    Introduction frame displaying welcome message and usage instructions.
    """

    def __init__(self, master):
        super().__init__(master)

        # Display a welcome message for client.
        self.welcome_message = customtkinter.CTkLabel(
            self,
            text="Welcome to your new Remote Access Software! \n\n Client Side",
            font=("Roboto", 50),
        )
        self.welcome_message.grid(
            row=0, column=0, padx=10, pady=(10, 50), sticky="nesw"
        )

        # Provide detailed instructions for client on how to use the software.
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

        # Detailed step-by-step instructions.
        instructions_text = (
            "1. Choose the IP Address and the Port number for your server.\n\n"
            "2. Write them down in the text fields.\n\n"
            "3. For screen sharing you will need also: Screen Index, Screen Width & Height. Click then on start monitoring.\n\n"
            "For file sharing you will also need AES Key & IV & File Path.\n\n"
            "4. You are done!"
        )

        self.instructions = customtkinter.CTkLabel(
            self,
            text=instructions_text,
            font=("Roboto", 20),
        )
        self.instructions.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="nesw")


class Access_Frame(customtkinter.CTkFrame):
    """
    Frame for client input to configure access parameters like IP, port, etc.
    It allows client to input all necessary information for establishing
    a connection for remote access tasks such as screen sharing and file sending.
    """

    def __init__(self, master):
        super().__init__(master)

        # Labels for input fields.
        labels = [
            "*Servers IP Address:",
            "*Port number:",
            "**Screen Index Number:",
            "**Screen Width:",
            "**Screen Height:",
            "***AES Key:",
            "***AES IV:",
            "***File Path:",
        ]

        for i, label_text in enumerate(labels):
            label = customtkinter.CTkLabel(self, text=label_text, font=("Roboto", 20))
            label.grid(row=i * 2, column=0, padx=0, pady=10, sticky="nesw")

        # Entry widgets for user to input the required information.
        entry_placeholder_texts = [
            "Enter the IP Address of your server:",
            "Enter the Port number:",
            "Screen index begins with 0",
            "Enter your screen width in px:",
            "Enter your screen height in px:",
            "Enter AES Key:",
            "Enter AES IV:",
            "Enter File Path:",
        ]

        self.entry_widgets = []

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

        # Button to initiate screen monitoring.
        self.button_connect = customtkinter.CTkButton(
            self,
            text="Start Monitoring",
            height=50,
            width=100,
            font=("Roboto", 20),
            command=self.submit,
        )
        self.button_connect.grid(row=19, column=0, padx=0, pady=20, sticky="nesw")

        # Button for sending files with the specified encryption details.
        self.button_send_file = customtkinter.CTkButton(
            self,
            text="Send File",
            height=50,
            width=100,
            font=("Roboto", 20),
            command=self.send_file,
        )
        self.button_send_file.grid(
            row=20, column=0, padx=0, pady=(0, 20), sticky="nesw"
        )

        # Button to clear all input fields for a new session.
        self.button_clear = customtkinter.CTkButton(
            self,
            text="Clear",
            height=50,
            width=100,
            font=("Roboto", 20),
            command=self.clear,
        )
        self.button_clear.grid(row=21, column=0, padx=0, pady=(5, 5))

    def submit(self):
        """
        Gather inputs from entry fields to initiate screen sharing.
        """
        entry_values = [entry.get() for entry in self.entry_widgets]

        # Extracted variables for clarity
        (
            ip_address,
            port_number,
            screen_index,
            window_width,
            window_height,
            aes_key,
            aes_iv,
            file_path,
        ) = entry_values

        # Check if the mandatory fields for screen sharing are filled
        if (
            ip_address
            and port_number
            and screen_index
            and window_width
            and window_height
        ):
            try:
                # Construct the full path to client.py in the same directory
                client_py_path = os.path.join(script_directory, "client.py")
                # Start the screen sharing process in a subprocess
                subprocess.Popen(
                    [
                        "python",
                        client_py_path,
                        ip_address,
                        port_number,
                        screen_index,
                        window_width,
                        window_height,
                    ],
                    shell=True,
                )
                # Notify the client of the successful operation
                messagebox.showinfo(
                    "Success",
                    "Live Screen start instruction sent successfully! \n Check your terminal.",
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start Live Screen: {str(e)}")
        else:
            messagebox.showerror("Error", "Please enter all required fields.")

    def send_file(self):
        """
        Gather inputs from entry fields to send a file with specified AES encryption.
        """
        entry_values = [entry.get() for entry in self.entry_widgets]

        ip_address, port_number, _, _, _, aes_key, aes_iv, file_path = entry_values

        # Check if the mandatory fields for file sending are filled
        if ip_address and port_number and aes_key and aes_iv and file_path:
            try:
                # Construct the full path to client_files.py in the same directory
                client_files_py_path = os.path.join(script_directory, "client_files.py")
                # Start the file sending process in a subprocess
                subprocess.Popen(
                    [
                        "python",
                        client_files_py_path,
                        ip_address,
                        port_number,
                        aes_key,
                        aes_iv,
                        file_path,
                    ],
                    shell=True,
                )
                # Notify the user of the successful operation
                messagebox.showinfo(
                    "Success", "File sent successfully! \n Check your terminal."
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send file: {str(e)}")
        else:
            messagebox.showerror(
                "Error", "Please enter all required fields for sending the file."
            )

    def clear(self):
        """
        Clear all input fields for a fresh start.
        """
        for entry in self.entry_widgets:
            entry.delete(0, END)


# Main application class, setting up the GUI window and frames.
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Client - Remote Access Software")
        self.geometry("1920x1080")

        self.frame1 = Intro_Frame(self)
        self.frame1.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nesw")
        self.frame1.configure(fg_color="transparent")

        self.frame2 = Access_Frame(self)
        self.frame2.grid(row=0, column=1, padx=(10, 0), pady=(10, 0), sticky="nesw")
        self.frame2.configure(fg_color="transparent")


app = App()
app.mainloop()
