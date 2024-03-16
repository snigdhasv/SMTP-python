#smtp_client_gui.py
import tkinter as tk
from tkinter import ttk
from smtp_client import SMTPClient, ClientConfig
import threading

class EmailClientGUI:
    def __init__(self, config):
        self.config = config

        self.root = tk.Tk()
        self.root.title("SMTP Client")
        self.root.geometry("500x400")

        # Set up font style
        self.default_font = ('Helvetica', 10)

        # Create a frame for input fields
        self.input_frame = ttk.Frame(self.root, padding="10")
        self.input_frame.pack(fill=tk.BOTH, expand=True)

        # Sender Email
        self.sender_label = ttk.Label(self.input_frame, text="Sender Email:", font=self.default_font)
        self.sender_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.sender_entry = ttk.Entry(self.input_frame, width=40, font=self.default_font)
        self.sender_entry.grid(row=0, column=1, sticky=tk.W, pady=5)

        # Recipient Email
        self.recipient_label = ttk.Label(self.input_frame, text="Recipient Email:", font=self.default_font)
        self.recipient_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.recipient_entry = ttk.Entry(self.input_frame, width=40, font=self.default_font)
        self.recipient_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

        # CC Email
        self.cc_label = ttk.Label(self.input_frame, text="CC (comma-separated):", font=self.default_font)
        self.cc_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.cc_entry = ttk.Entry(self.input_frame, width=40, font=self.default_font)
        self.cc_entry.grid(row=2, column=1, sticky=tk.W, pady=5)

        # BCC Email
        self.bcc_label = ttk.Label(self.input_frame, text="BCC (comma-separated):", font=self.default_font)
        self.bcc_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        self.bcc_entry = ttk.Entry(self.input_frame, width=40, font=self.default_font)
        self.bcc_entry.grid(row=3, column=1, sticky=tk.W, pady=5)

        # Subject
        self.subject_label = ttk.Label(self.input_frame, text="Subject:", font=self.default_font)
        self.subject_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        self.subject_entry = ttk.Entry(self.input_frame, width=40, font=self.default_font)
        self.subject_entry.grid(row=4, column=1, sticky=tk.W, pady=5)

        # Body
        self.body_label = ttk.Label(self.input_frame, text="Body:", font=self.default_font)
        self.body_label.grid(row=5, column=0, sticky=tk.W, pady=5)
        self.body_entry = ttk.Entry(self.input_frame, width=40, font=self.default_font)
        self.body_entry.grid(row=5, column=1, sticky=tk.W, pady=5)

        # Attachment
        self.attachment_label = ttk.Label(self.input_frame, text="Attachment Path:", font=self.default_font)
        self.attachment_label.grid(row=6, column=0, sticky=tk.W, pady=5)
        self.attachment_entry = ttk.Entry(self.input_frame, width=40, font=self.default_font)
        self.attachment_entry.grid(row=6, column=1, sticky=tk.W, pady=5)

        # Create a send button
        self.send_button = ttk.Button(self.input_frame, text="Send Email", command=self.send_email, style='PrimaryButton.TButton')
        self.send_button.grid(row=7, column=0, columnspan=2, pady=10)

        # Create a frame for displaying sent email data
        self.output_frame = ttk.Frame(self.root, padding="10")
        self.output_frame.pack(fill=tk.BOTH, expand=True)

        # Email data display label
        self.email_data_label = ttk.Label(self.output_frame, text="Email Data:", font=self.default_font)
        self.email_data_label.pack(anchor=tk.W, pady=(10, 5))

        # Email data text widget
        self.email_data_text = tk.Text(self.output_frame, height=50, width=50, font=self.default_font)
        self.email_data_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        # Set up styles
        self.style = ttk.Style()
        self.style.configure('PrimaryButton.TButton', font=('Helvetica', 10, 'bold'))

    def send_email(self):
        # Get email details from the entry fields
        sender = self.sender_entry.get()
        recipient = self.recipient_entry.get()
        cc_recipients = [email.strip() for email in self.cc_entry.get().split(',')]
        bcc_recipients = [email.strip() for email in self.bcc_entry.get().split(',')]
        subject = self.subject_entry.get()
        body = self.body_entry.get()
        attachment_path = self.attachment_entry.get()

        # Define a function to send email in a separate thread
        def send_email_thread():
            # Call the SMTPClient to send the email
            client = SMTPClient(self.config)

            # Read attachment file content if provided
            attachment_content = ""
            if attachment_path:
                with open(attachment_path, "r") as attachment_file:
                    attachment_content = attachment_file.read()

            email_data = f"""\
            From: {sender}
            To: {recipient}
            CC: {', '.join(cc_recipients)}
            BCC: {', '.join(bcc_recipients)}
            Subject: {subject}

            {body}

            Attachment Contents:
            {attachment_content}
            """
            self.email_data_text.delete(1.0, tk.END)  # Clear previous email data
            self.email_data_text.insert(tk.END, email_data)  # Insert new email data

            client.send_email(sender, recipient, email_data, cc_recipients=cc_recipients, bcc_recipients=bcc_recipients, attachment_path=attachment_path)

        # Run send_email_thread function in a separate thread
        threading.Thread(target=send_email_thread, daemon=True).start()

if __name__ == "__main__":
    config = ClientConfig(
        server_hostname='172.20.10.2',  # Server IP address---check this using ipconfig on cmd---change accordingly
        server_port=25,  
        sender_email='your_sender_email@example.com',
        recipient_email='your_recipient_email@example.com',
        subject='Your email subject',
        body='Your email body.'
    )
    
    gui = EmailClientGUI(config)
    gui.root.mainloop()
