#smtp_server.py
import socket
import threading
import logging

class ServerConfig:
    def __init__(self):
        self.hostname = '0.0.0.0'  # Listen on all available network interfaces
        self.port = 25  # SMTP default port
        self.max_message_size = 1024  # Maximum size of email message to receive

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger('smtp_server')

class SMTPServer:
    def __init__(self, config):
        self.config = config
        self.logger = setup_logging()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.config.hostname, self.config.port))
        server_socket.listen(5)
        self.logger.info(f"SMTP server listening on {self.config.hostname}:{self.config.port}...")
        
        while True:
            client_socket, client_address = server_socket.accept()
            self.logger.info(f"Connection from {client_address} established.")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        client_socket.send(b'220 localhost SMTP server ready\r\n')

        while True:
            data = client_socket.recv(self.config.max_message_size).decode('utf-8').strip()
            self.logger.info(f"Received: {data}")

            if not data:
                break

            # Process SMTP command
            command = data.split(' ')[0].upper()  # Get the command (e.g., EHLO, MAIL, RCPT, etc.)

            if command == 'EHLO':
                client_socket.send(b'250-localhost\r\n')
                client_socket.send(b'250 STARTTLS\r\n')
                client_socket.send(b'250 AUTH PLAIN LOGIN\r\n')
            elif command == 'MAIL':
                client_socket.send(b'250 Ok\r\n')
            elif command == 'RCPT':
                client_socket.send(b'250 Ok\r\n')
            elif command == 'DATA':
                client_socket.send(b'354 End data with <CR><LF>.<CR><LF>\r\n')
                email_data = ''
                attachment_data = None
                is_attachment = False

                while True:
                    line = client_socket.recv(1024).decode('utf-8')
                    
                    if line.strip() == '.':
                        break

                    if is_attachment:
                        if attachment_data is None:
                            attachment_data = line.encode('utf-8')
                        else:
                            attachment_data += line.encode('utf-8')
                    else:
                        if line.startswith('Content-Type:'):
                            is_attachment = True
                            attachment_data = line.encode('utf-8')
                        else:
                            email_data += line    


                self.logger.info("Received email data:\n" + email_data)  # Log the entire email data
                if is_attachment:
                    self.logger.info("Received attachment data:\n" + attachment_data)  # Log the attachment data
                client_socket.send(b'250 Ok\r\n')
            elif command == 'QUIT':
                client_socket.send(b'221 Bye\r\n')
                break
            else:
                client_socket.send(b'500 Command unrecognized\r\n')

        client_socket.close()

if __name__ == "__main__":
    config = ServerConfig()
    server = SMTPServer(config)
    server.start()
