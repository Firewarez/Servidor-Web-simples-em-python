from socket import *
import sys  

#Cria ponto de comunicação: AF_INET utiliza IPV4 , SOCK_STREAM = PROTOCOLO TCP
serverSocket = socket(AF_INET, SOCK_STREAM)

# 1 Prepara a porta | 2 Rerva a serverPort | 3 Define a fila de espera
serverPort = 6789          
serverSocket.bind(('', serverPort))
serverSocket.listen(1)          

print(f'\nServidor funcionando em: http://localhost:{serverPort}/HelloWorld.html')

while True:
    # 1. Aceita a conexão
    connectionSocket, addr = serverSocket.accept()
    
    try:
        # 2. Recebe a mensagem do cliente
        message = connectionSocket.recv(1024).decode()

        Se a mensagem vier vazia, fecha e ignora
        if not message:
            connectionSocket.close()
            continue

        # 3. Tenta ler o nome do arquivo
        filename = message.split()[1]
        f = open(filename[1:], 'r')
        outputdata = f.read()
        
        # 4. Se achou o arquivo, envia a resposta 200 OK
        header = "HTTP/1.1 200 OK\r\n\r\n"
        connectionSocket.send(header.encode())

        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()

    except IOError:
        # Erro 404: Arquivo não encontrado
        error_header = "HTTP/1.1 404 Not Found\r\n\r\n"
        error_body = "<html><body><h1>404 Not Found</h1></body></html>"
        try:
            connectionSocket.send(error_header.encode())
            connectionSocket.send(error_body.encode())
        except:
            pass # Se der erro ao enviar o erro, apenas segue a vida
        connectionSocket.close()

    except IndexError:
        # Se o navegador mandar um pedido incompleto, apenas fecha a conexão
        connectionSocket.close()

serverSocket.close()
sys.exit()
