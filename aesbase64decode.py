import base64
from Crypto.Cipher import AES
from pathlib import Path

while True:
    pw = input("Please enter the password:\n")
    if pw == "samplepassword":
        break    

# Start of decoding process of a base64 encoded file into a binary AES128 encrypted file
imageEncryptedEncoded = open('inputjpg_encrypted_encoded', 'rb')
imageEncryptedEncoded_str = imageEncryptedEncoded.read()
imageEncrypted_str = base64.decodebytes(imageEncryptedEncoded_str) 
# create a writable file and write the decoding result
imageEncrypted = open('image_encrypted', 'wb') 
imageEncrypted.write(imageEncrypted_str)
imageEncryptedEncoded.close()
imageEncrypted.close()

# Start of decrypting process of a binary AES128 encrypted file into a JPEG image
# Calculate the nearest multiple of 16 that is lesser than the current file size
print("File size of encrypted, padded image: ")
padded_file_size = Path('image_encrypted').stat().st_size
print(str(padded_file_size))
print("nearest round-down 16-divisible byte size")
nearest_16_byte_size = padded_file_size - (padded_file_size % 16)
print(str(nearest_16_byte_size))

# Decrypt binary AES128 encrypted file into jpg
key = 'ivanhuIVANHUivhu'
# Encode the key string into UTF8 as is required by the Crypto.Cipher library
keyutf8 = str.encode(key)
input_file = open('image_encrypted', 'rb')
output_file = open('image_decrypted.jpg' , 'wb')
input_file_str = input_file.read()
# Trim encrypted, padded image to nearest 16 bytes
input_file_str = input_file_str[0:nearest_16_byte_size]
decipher = AES.new(keyutf8, AES.MODE_ECB)
output_file_str = decipher.decrypt(input_file_str)
output_file.write(output_file_str)

