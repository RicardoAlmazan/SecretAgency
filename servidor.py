import socket
import threading
import sys
import pickle
from aes256 import AES_256


class Servidor():
    """docstring for Servidor"""

    def __init__(self, host="localhost", port=4000):

        self.clientes = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)
        self.sock.setblocking(False)

        aceptar = threading.Thread(target=self.aceptarCon)
        procesar = threading.Thread(target=self.procesarCon)

        aceptar.daemon = True
        aceptar.start()

        procesar.daemon = True
        procesar.start()

        self.aes = AES_256()

        while True:
            msg = input('->')
            if msg == 'salir':
                self.sock.close()
                sys.exit()
            else:
                pass

    def msg_to_all(self, msg, cliente):
        if "salir" in self.aes.dec(msg).decode("utf-8").lower():
            self.aes = AES_256()
            aux = ':'.join(str(c)
                           for c in cliente.getpeername()) + ' se desconecto'
            msg = str.encode(self.aes.enc(str.encode(aux)))
            print(cliente.getpeername(), ' se ha desconectado')
            self.aes = AES_256()
            self.clientes.remove(cliente)
        else:
            self.aes = AES_256()

        for c in self.clientes:
            if c != cliente:
                c.send(msg)
            else:
                print(c.getpeername(), " dice ", msg.decode("utf-8"))

    def aceptarCon(self):
        print("aceptarCon iniciado")
        while True:
            try:
                conn, addr = self.sock.accept()
                conn.setblocking(False)
                self.clientes.append(conn)
                print("%s:%s conectado" % addr)
                conn.send(self.aes.enc("Hola, ahora estas conectado"))
                self.aes = AES_256()
            except:
                pass

    def procesarCon(self):
        print("ProcesarCon iniciado")
        while True:
            if len(self.clientes) > 0:
                for c in self.clientes:
                    try:
                        data = c.recv(1024)
                        if data:
                            self.msg_to_all(data, c)
                    except:
                        pass


s = Servidor()
