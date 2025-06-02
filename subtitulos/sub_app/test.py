import googletrans
from langdetect import detect
import re

txt = '1 00:01:06,007 --> 00:01:08,840 31 AÑOS DESPUÉS DE LA III GUERRA MUNDIAL'

patron = r"\b[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+\b"
new_txt = re.findall(patron, txt)
new_txt = ''.join(new_txt).lower()
print('new_txt', new_txt)

r = detect(new_txt)
print(r)
