from django.shortcuts import render
from .forms import encryptorForm, decryptorForm
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import binascii
import codecs
def encrypt(key,message):
    padder = padding.PKCS7(128).padder()
    padded_message = padder.update(message) + padder.finalize()
    # Create an AES cipher object with ECB mode
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    # Encrypt the padded message
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()

    return ciphertext

def decrypt(ciphertext,key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_message = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()

    return decrypted_message
def toolView(request):
    encryptorform = encryptorForm(initial={"plain_text":"","encryption_key":""})
    decryptorform = decryptorForm(initial={"cipher_text": "", "decryption_key": ""})
    encrypted_text = ""
    decrypted_text = ""
    if request.method == "POST":
        encryptorform = encryptorForm(request.POST)
        if encryptorform.is_valid():
            plain_text = encryptorform.cleaned_data['plain_text']
            encryption_key = encryptorform.cleaned_data['encryption_key']
            encrypted_text =  binascii.hexlify(encrypt(encryption_key.encode('utf-8'),plain_text.encode('utf-8'))).decode('ascii')
        decryptorform = decryptorForm(request.POST)
        if decryptorform.is_valid():
            cipher_text = decryptorform.cleaned_data['cipher_text']
            decryption_key = decryptorform.cleaned_data['decryption_key']
            try:
                decrypted_text = decrypt(bytes.fromhex(cipher_text),decryption_key.encode('utf-8')).decode('ascii')
            except:
                decrypted_text = "Invalid Decryption key"
    else:
        encryptorform = encryptorForm()
        decryptorform = decryptorForm()

    return render(request, "tool.html",{"encryptor":encryptorform,"decryptor":decryptorform,"encrypted_text":encrypted_text,"decrypted_text":decrypted_text})