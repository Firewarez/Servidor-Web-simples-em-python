from socket import *
import sys  

serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = 6789             
serverSocket.bind(('', serverPort))
serverSocket.listen(1)         


while True:
    # Estabelece a conexão
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        # Recebe a mensagem do cliente (requisição HTTP)
        message = connectionSocket.recv(1024).decode()

        filename = message.split()[1]
        f = open(filename[1:], 'r')
        outputdata = f.read()
        

        
        header = "HTTP/1.1 200 OK\r\n\r\n"
        connectionSocket.send(header.encode())

        # Envia o conteúdo do arquivo ao cliente
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        # Fecha a conexão com o cliente
        connectionSocket.close()

    except IOError:
        # Envia mensagem de erro 404 se o arquivo não for encontrado
        error_header = "HTTP/1.1 404 Not Found\r\n\r\n"
        error_body = "<html><body><h1>404 Not Found</h1></body></html>"
        connectionSocket.send(error_header.encode())
        connectionSocket.send(error_body.encode())

        connectionSocket.close()

serverSocket.close()
sys.exit()
