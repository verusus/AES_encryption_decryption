from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# -------------------- encryption part ------------------------

# generate the key file named mykey.key
# key = Fernet.generate_key()
key = get_random_bytes(16)

with open('mykey.key', 'wb') as mykey:
    mykey.write(key)

with open("data.json", "rb") as data_file:
    data = data_file.read()
# data = b'secret data'

cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(data)

file_out = open("encrypted.json", "wb")
[file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
file_out.close()
# --------------------------------------------------------------------
# ------------------------------------ decryption part ----------------

file_in = open("encrypted.json", "rb")
nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]

with open("mykey.key", "rb") as mykey_file:
    key = mykey_file.read()
# let's assume that the key is somehow available again
cipher = AES.new(key, AES.MODE_EAX, nonce)
data = cipher.decrypt_and_verify(ciphertext, tag)
print(data)
with open("decrypted.json", "wb") as decrypted_file:
    decrypted_file.write(data)
