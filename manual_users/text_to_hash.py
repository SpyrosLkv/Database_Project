import hashlib
import binascii

def HashPass(original_text):
    hash_password = hashlib.sha256(original_text.encode()).digest()
    answer = binascii.hexlify(hash_password).decode()
    return answer


print(HashPass("password"))
#  5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8