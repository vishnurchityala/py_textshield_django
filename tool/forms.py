from django import forms

class encryptorForm(forms.Form):
    plain_text = forms.CharField(max_length=3000,label="plain_text",initial="")
    encryption_key = forms.CharField(max_length=16, label="encryption_key",initial="")

class decryptorForm(forms.Form):
    cipher_text = forms.CharField(max_length=3000,initial="")
    decryption_key = forms.CharField(max_length=16, initial="")
