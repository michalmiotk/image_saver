from cryptography.fernet import Fernet

secret_key = 'nNjpIdfAx2LRtm-p6ryCRZ8lRsL0DtuY0f9JeAe2wG0='
encoded_key = secret_key.encode('utf-16')
encoding_bytes_type = 'utf-16'

def convert_pass_from_text_to_bytes():
    message_to_user = "prosze wprowadz dane do zaszyfrowania, otrzymasz je potem zaszyfrowane w formie bajtow\n"
    pass_raw_text = input(message_to_user)
    pass_bytes = pass_raw_text.encode(encoding_bytes_type)
    f = Fernet(encoded_key)
    encoded_password_to_bytes = f.encrypt(pass_bytes)
    print(encoded_password_to_bytes)

def from_bytes_cipher_to_plain_text(bytes_cipher):
    f = Fernet(encoded_key)
    decrypted = f.decrypt(bytes_cipher)

    return decrypted.decode(encoding_bytes_type)

if __name__ == '__main__':
    convert_pass_from_text_to_bytes()
