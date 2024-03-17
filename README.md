# SMTP Server and Client with GUI

This repository contains code for implementing a simple SMTP server and client, along with a graphical user interface (GUI) for the client.

## Features

- **SMTP Server (`smtp_server.py`):**
  - Listens for incoming connections on a specified hostname and port.
  - Handles various SMTP commands such as EHLO, MAIL, RCPT, DATA, and QUIT.
  - Accepts email data and attachments from clients.

- **SMTP Client (`smtp_client.py`):**
  - Sends emails by establishing a connection with the SMTP server.
  - Supports sending emails with attachments.
  - Provides a command-line interface for sending emails with specified parameters.

- **SMTP Client GUI (`smtp_client_gui.py`):**
  - Allows users to input email details such as sender, recipient, subject, body, etc., via a graphical user interface.
  - Provides fields for specifying CC and BCC recipients and attaching files.
  - Initiates the sending process in a separate thread and displays email data in a text widget.

## Setup and Usage

1. **SMTP Server Setup:**
   - Update the configuration details in `smtp_server.py` according to your preferences, such as hostname and port.
   - Run `smtp_server.py` on the machine where you want to receive emails.

2. **SMTP Client Setup:**
   - Update the configuration details in `smtp_client.py` and `smtp_client_gui.py` according to your SMTP server settings(check comments).
   - Run `smtp_client_gui.py` on a machine from which you want to send emails.
   - Alternatively, you can use `smtp_client.py` directly from the command line by providing the required email details as arguments.

## Dependencies

- Python 3.x
- Tkinter (for GUI)

## Usage

- For detailed usage instructions, please refer to the docstrings and comments within each module.
- Run `smtp_server.py` and `smtp_client_gui.py` from the command line or your preferred Python environment.
- Follow the prompts in the GUI to input email details and send emails.


