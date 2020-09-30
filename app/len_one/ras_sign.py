import base64

import rsa

# 生成密钥：生成RSA公钥和秘钥
(pubkey, privkey) = rsa.newkeys(1024)

# 保存密钥(一个公钥一个私钥)
with open('public.pem', 'w+') as f:
    f.write(pubkey.save_pkcs1().decode())
with open('private.pem', 'w+') as f:
    f.write(privkey.save_pkcs1().decode())

# 导入密钥
with open('public.pem', 'r') as f:
    pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
with open('private.pem', 'r') as f:
    privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())

print(pubkey, type(pubkey))
print(privkey, type(privkey))
# 明文
message = """{"EventType":1,"SN":"XT-PE29641214A06C004","InfoCode":null,"Data":"cGluZw=="}"""
# print(message)
# 公钥对明文加密，得到密文
crypto = rsa.encrypt(message.encode(), pubkey)
# print(crypto.decode(encoding="utf-8"))
# 私钥对密文解密，得到明文
message = rsa.decrypt(crypto, privkey).decode()
print(message)

message = """{"EventType":1,"SN":"XT-PE29641214A06C004","InfoCode":null,"Data":"cGluZw=="}"""
# 私钥签名
signature = rsa.sign(message.encode("utf-8"), privkey, 'SHA-1')
print(signature)
# print(str(base64.b64decode(signature), "utf-8"))
# signature += b'1'
# 公钥验证：同时收到指令明文、密文，然后用公钥验证，进行身份确认
try:
    result = rsa.verify(message.encode("utf-8"), signature, pubkey)
    # 获取加密方式
    if result:
        print("OK")
    res = rsa.find_signature_hash(signature, pubkey)
    if res:
        print("OK")
except Exception:
    print("验证签名不通过")


import hashlib
a = hashlib.sha1()
a.update(message.encode('utf-8'))
msg = a.hexdigest()
print(msg.upper())

# maxa = int('2000000000L')
# print(maxa, type(maxa))
