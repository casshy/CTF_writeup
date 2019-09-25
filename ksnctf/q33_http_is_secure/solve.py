n1 = 0x00a5a7ce44462e8ac6e4da5e8a8d58e003b8267568b358106cf06412884ceeb7cc4251c2cce2db74689d1afa109bde9762402e81d96cb6c8c6c5aebc8d45a96bf214a618b499a8c6134035c5039bf9a39bc47190e4cc4560cb75ab8d63635cdee8e50f5815b29180cc51a4c8cf76a8bbe6e61c68aca385fdf99e712b10a6be7ed794cf27540b7aa00f59da5579040a9b3b7c23e9e22a15c29eb0c060b96d1f48d1c458e2c412512962ce5af885237b6138df6c9e85d101c266c3b80b02ff97d6fde46598e19e3fa1df2c56bd34addfe716569a2ed42c6442bf2db5e9a51cc2d7dd4497717ddd9a8a66ae281e1a2abf7df7a59779b499cc0f8167a19e3ca5c9bbe3

n2 = 0x00a4daad49eae0b5c59da0452978ae987e1b96f149dedb62274c97f99ac4544aa90db4aaf9a0967f118b7009097bcb0baeb4a19636777a7747e06ad84496c9c61d18a7b5ca776585a817526ed6d9f0f2abd8c434c62cbf025eb7ce5a83e4a7f9938f3862de24e6292f43270ffda757c17aaa797ff9fe18fd1cb23921dc585d4550384ff5c4f24e6dfc6d4f44b569345808239247c20d266cd0f5e373889ed4e459590b7d742d2837c1c48dcf9418e22191ab4a0bca0ed79b1d45c0ca5d36ea6960c9360c11412329fd5d90ff3467f2d82e23021adf3b6d8be24903b76effc938154ec219f344118f1c41fec31171b62945a07e35762a961a05795389086052dec7

def gcd(x, y):
    while y != 0:
        x, y = y, x%y
    return x

def lcm(a, b):
    return a * b // gcd(a, b)

p1 = p2 = gcd(n1, n2)
q1 = n1 // p1
q2 = n2 // p2
#print('p1 = {}'.format(p1))
#print('q1 = {}'.format(q1))

e = 65537  # Public exponent

# Calculate private exponent
def private_exponent(p, q):
    l = lcm(p - 1, q - 1)
    y = 1
    while (1 - l*y) % e != 0:
        y += 1
        d = (1 - l*y) // e
        if d < 0:
            d += l
    return d

d1 = private_exponent(p1, q1)
d2 = private_exponent(p2, q2)

from Crypto.PublicKey import RSA
key1 = RSA.construct((n1, e, d1))
key2 = RSA.construct((n2, e, d2))

with open('rsa_key1.key', 'w') as f:
    f.write(key1.exportKey(format='PEM').decode('utf-8'))
with open('rsa_key2.key', 'w') as f:
    f.write(key2.exportKey(format='PEM').decode('utf-8'))
