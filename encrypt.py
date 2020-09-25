from Crypto.Cipher import AES
import binascii
import os


dataFile = 'data'

def encrypt_AES_GCM(msg, secretKey):
  aesCipher = AES.new(secretKey, AES.MODE_GCM)
  ciphertext = aesCipher.encrypt(msg)
  return (ciphertext, aesCipher.nonce)

def decrypt_AES_GCM(encryptedMsg, secretKey):
	(ciphertext, nonce) = encryptedMsg
	nonce = binascii.unhexlify(nonce)
	aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
	plaintext = aesCipher.decrypt(ciphertext)
	return plaintext

def write_encrypted_data_to_file(msg, key):
	error_string = ''
	key = binascii.unhexlify(key)
	(data, nonce) = encrypt_AES_GCM(msg.encode('utf-8'), key)
	try:
		f = open(dataFile, 'a')
		f.write(binascii.hexlify(data).decode('utf-8')+' '+binascii.hexlify(nonce).decode('utf-8')+'\n')
		f.close()
	except Exception as error:
		error_string += repr(error)
	return error_string

def decrypt_data_with_key(key):
	error_string = ''
	decrypted = []
	key = binascii.unhexlify(key)
	if not os.path.exists(dataFile):
		open(dataFile, 'w').close()
	try:
		f = open(dataFile, 'r')
		lines = f.readlines()
		for i in range(len(lines)):
			(cipher, nonce) = lines[i].split()
			cipher = binascii.unhexlify(cipher)
			decrypt = 'Could Not Decrypt'
			try:
				decrypt = decrypt_AES_GCM((cipher, nonce), key).decode('utf-8')
			except:
				pass
			decrypted.append('('+str(i)+') '+decrypt)
	except Exception as error:
		error_string += repr(error)
	return (decrypted, error_string)

def write_random_256bit_key_to_file(filename):
	key = binascii.hexlify(os.urandom(32)).decode('utf-8')
	error_string = ''
	try:
		f = open(filename, 'x')
		f.write(key)
		f.close()
	except Exception as error:
		error_string += repr(error)
	return error_string

def read_key_from_file(filename):
	error_string = ''
	key = ''
	try:
		f = open(filename, 'r')
		key += f.readline()
		f.close()
	except Exception as error:
		error_string += repr(error)
	return (key.encode('utf-8'), error_string)

def delete_line_from_file(num):
	error_string = ''
	lines = []
	try:
		f = open(dataFile, 'r')
		lines = f.readlines()	
		f.close()
		f = open(dataFile, 'w')
		for i in range(len(lines)):
			if i != num:
				f.write(lines[i])
		f.close()
	except Exception as error:
		error_string += repr(error)
	return error_string

if __name__ == '__main__':
	write_random_256bit_key_to_file('test.txt')