import socket
import threading
import sys
from aes256 import AES_256
from cliente_interfaz import interfaz


class Cliente(AES_256):
    """docstring for Cliente"""

    def __init__(self, host="localhost", port=4000):

        self.aes = AES_256()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((str(host), int(port)))

        self.ventana = interfaz(self.send_msg, self.sock)

        msg_recv = threading.Thread(target=self.msg_recv)

        msg_recv.daemon = True
        msg_recv.start()

        self.ventana._mostrar()

    def msg_recv(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if data:
                    plaintext = self.aes.dec(data)
                    print(plaintext.decode("utf-8"))
                    self.ventana.mensaje_recibido(plaintext.decode("utf-8"))
                    self.aes = AES_256()
            except Exception as e:
                print(e)

    def send_msg(self, msg):
        aux = ':'.join(str(c)
                       for c in self.sock.getpeername()) + ' dice: ' + msg
        self.enc_msg = self.aes.enc(str.encode(aux))
        self.sock.send(str.encode(self.enc_msg))
        self.aes = AES_256()

c = Cliente()