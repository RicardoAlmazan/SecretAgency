from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

class AES_256():
	"""docstring for AES"""
	#aes = AES.new(key, AES.MODE_OFB, iv)
	def __init__(self):
		self.key = b'01234567890123456789012345678901'
		self.iv = b'0123456789012345'#Random.new().read(AES.block_size)
		self.aes = AES.new(self.key, AES.MODE_OFB, self.iv)
		#print('iv =', self.iv)
		#print('key =', self.key)
	
	def enc(self, msg):
		ciphertext = self.aes.encrypt(pad(msg, 32))
		self.iv64 = b64encode(self.aes.iv).decode('utf-8')
		self.ciphertext64 = b64encode(ciphertext).decode('utf-8')
		return self.ciphertext64


	def dec(self, data):
		plaintext64 = b64decode(data.decode("utf-8"))
		plaintext = unpad(self.aes.decrypt(plaintext64), 32)
		return plaintext
