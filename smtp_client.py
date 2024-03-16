#smtp_client.py
import socket
import logging

class ClientConfig:
    def __init__(self, server_hostname='127.0.0.1', server_port=1025, sender_email='sender@example.com', recipient_email='recipient@example.com', subject='Test email', body='Hello, this is a test email from SMTP client.'):
        self.server_hostname = server_hostname
        self.server_port = server_port
        self.sender_email = sender_email
        self.recipient_email = recipient_email
        self.subject = subject
        self.body = body

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger('smtp_client')

class SMTPClient:
    def __init__(self, config):
        self.config = config
        self.logger = setup_logging()

    def send_email(self, sender, recipient,email_data, cc_recipients=None, bcc_recipients=None, attachment_path=None):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.config.server_hostname, self.config.server_port))
            self.logger.info("Connected to SMTP server.")

            response = client_socket.recv(1024)
            self.logger.info(response.decode('utf-8'))

            # Send EHLO/HELO command
            client_socket.send(b'EHLO client\r\n')
            response = client_socket.recv(1024)
            self.logger.info(response.decode('utf-8'))

            # Send MAIL FROM command
            client_socket.send(f'MAIL FROM:<{sender}>\r\n'.encode('utf-8'))
            response = client_socket.recv(1024)
            self.logger.info(response.decode('utf-8'))

            # Send RCPT TO command for the main recipient
            client_socket.send(f'RCPT TO:<{recipient}>\r\n'.encode('utf-8'))
            response = client_socket.recv(1024)
            self.logger.info(response.decode('utf-8'))

            # Send RCPT TO command for CC recipients if any
            if cc_recipients:
                for cc_recipient in cc_recipients:
                    client_socket.send(f'RCPT TO:<{cc_recipient}>\r\n'.encode('utf-8'))
                    response = client_socket.recv(1024)
                    self.logger.info(response.decode('utf-8'))

            # Send RCPT TO command for BCC recipients if any
            if bcc_recipients:
                for bcc_recipient in bcc_recipients:
                    client_socket.send(f'RCPT TO:<{bcc_recipient}>\r\n'.encode('utf-8'))
                    response = client_socket.recv(1024)
                    self.logger.info(response.decode('utf-8'))

            # Send DATA command
            client_socket.send(b'DATA\r\n')
            response = client_socket.recv(1024)
            self.logger.info(response.decode('utf-8'))

            # Send email data
            client_socket.send(email_data.encode('utf-8'))

            # If attachment is provided, send it
            if attachment_path:
                with open(attachment_path, 'rb') as attachment_file:
                    attachment_data = attachment_file.read()
                client_socket.send(attachment_data)

            # End email data with a dot
            client_socket.send(b'\r\n.\r\n')
            response = client_socket.recv(1024)
            self.logger.info(response.decode('utf-8'))

            # Send QUIT command
            client_socket.send(b'QUIT\r\n')
            response = client_socket.recv(1024)
            self.logger.info(response.decode('utf-8'))

            client_socket.close()
        except Exception as e:
            self.logger.error(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    config = ClientConfig(
        server_hostname='172.20.10.2',  # Server IP address---check this using ipconfig on cmd---change accordingly
        server_port=25,  
        sender_email='your_sender_email@example.com',
        recipient_email='your_recipient_email@example.com',
        subject='Your email subject',
        body='Your email body.'
    )

    client = SMTPClient(config)

    # Prompt the user to enter sender, recipient, email data, and attachment path
    sender = input("Enter sender email address: ")
    recipient = input("Enter recipient email address: ")
    cc_recipients = input("Enter CC email addresses (comma-separated, leave empty if none): ").split(',')
    bcc_recipients = input("Enter BCC email addresses (comma-separated, leave empty if none): ").split(',')
    email_subject = input("Enter email subject: ")
    email_body = input("Enter email body: ")
    attachment_path = input("Enter attachment file path (leave empty if none): ")

    # Construct the email data
    email_data = f"""\
    From: {sender}
    To: {recipient}
    Cc: {', '.join(cc_recipients)}
    Bcc: {', '.join(bcc_recipients)}
    Subject: {email_subject}

    {email_body}
    """

    client.send_email(sender, recipient,email_data, cc_recipients, bcc_recipients, attachment_path)
