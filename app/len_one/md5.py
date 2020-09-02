import hashlib


m = hashlib.md5()
m.update(b'hello,word!')
ms = m.hexdigest()
print(ms)
'9702d6722a0901398efd4ecb3a20423f'