import sys
import socket
import threading 
from time import sleep

lista = ('ska', 'ds', 'das')
x = ' '.join(lista) # insere
x1 = len(lista) # informa quantidade de objetos
x2 = repr(lista) # printa tudo o que contem
x3 = chr(98) # tabela ascii em especifico o char(CLARO :D)
#print(f'Join: {x} \n len: {x1} \n repr: {x2} \n chr: {x3}')
x4 = isinstance(5, str) # checa se o objeto é o que você especificou
#print(x4)

#SRC evita haver problemas com importações


Hex_chr = ''.join(
    [
        (len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)
    ]
)



def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        src = src.decode()
    results = list()
    for i in range(0, len(src), length):
        word = str(src[i:i+length])

        printable = word.translate(Hex_chr)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length * 3
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')
    if show:
        for line in results:
            print(line)
    else:
        return results



def receive_from(connection):
    buffer = b""
    sleep(10)
    
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        pass
    return buffer

def request_hander(buffer):
    #realizar modiicações no pacote
    return buffer
def response_handler(buffer):
    #realizar modiicações no pacote
    return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        remote_buffer = response_handler(remote_buffer)
        if len(remote_buffer):
            print("[<--] Enviado %d bytes para localhost." % len(remote_buffer))
        
        while True:
            local_buffer = receive_from(client_socket)
            if len(local_buffer):
                line = "[-->] Recebido %d bytes do localhost" % len (local_buffer)
                print(line)
                hexdump(local_buffer)

                local_buffer = request_hander(local_buffer)
                remote_socket.send(local_buffer)
                print("[-->] Enviado para o servidor remoto")

            remote_buffer = receive_from(remote_socket)
            if len(remote_buffer):
                print("[<--] Recebido %d Bytes do servidor remoto" % len (remote_buffer))
                hexdump(remote_buffer)

                remote_buffer = response_handler(remote_buffer)
                client_socket.send(remote_buffer)
                print("[<--] Enviado para o localHost.")

            if not len(local_buffer) or not len(remote_buffer):
                client_socket.close()
                remote_socket.close()
                print("[X] Não há mais dados. fechando conexão")
                break



def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # opcional, mas recomendado

    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print('problema ao conectar: %r' % e)

        print("[!!] Falha ao ouvir em %s:%d" % (local_host, local_port))
        print("[!!] Verifique outros sockets de escuta ou corrija as permissões.")
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sys.exit(0)

    print("[*] Ouvindo em %s:%d" % (local_host, local_port))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        #imprimir as informações da conexão local
        line = "> conexão de entrada recebida de %s:%d" % (addr[0], addr[1])
        print(line)
        # iniciar uma thread para se comunicar com o host remoto
        proxy_thread = threading.Thread(
            target = proxy_handler,
            args=(client_socket, remote_host,
                  remote_port, receive_first))
        proxy_thread.start()





def main():
    if len(sys.argv[1:]) != 5:
        print("Uso: ./proxy.py [localhost] [localport]", end='')
        print("[remotehost] [remoteport] [receive_first]")
        print("Exemplo: ./proxy.py 127.0.01 9000 10.12.132.1 9000 True")
        sys.exit(0)
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True

    else:
        receive_first = False
        

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)
if __name__ == '__main__':
    main()