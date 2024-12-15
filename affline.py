from collections import Counter
import string

def char_to_num(c):
    return ord(c.upper()) - ord('A')

def num_to_char(n):
    return chr((n % 26) + ord('A'))

def mod_inverse(a, m=26):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_decrypt(ciphertext, a, b):
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        return None
    plaintext = ""
    for ch in ciphertext:
        if ch.isalpha():
            C = char_to_num(ch)
            P = (a_inv * (C - b)) % 26
            plaintext += num_to_char(P)
        else:
            plaintext += ch
    return plaintext

def gcd(a,b):
    while b:
        a,b = b,a%b
    return a

# Read the ciphertext from an external file named "21.txt"
with open("21.txt", "r", encoding="utf-8") as f:
    ciphertext = f.read()

filtered_text = [ch for ch in ciphertext.upper() if ch.isalpha()]
freq = Counter(filtered_text)

most_common = freq.most_common(2)
if len(most_common) < 2:
    print("Not enough data.")
    exit()

c1, freq1 = most_common[0]
c2, freq2 = most_common[1]

print(f"Most frequent letter in ciphertext: {c1}, count: {freq1}")
print(f"Second most frequent letter in ciphertext: {c2}, count: {freq2}")

P1, P2 = 4, 19
C1 = char_to_num(c1)    
C2 = char_to_num(c2)    

deltaP = (P1 - P2) % 26
deltaC = (C1 - C2) % 26

deltaP_inv = mod_inverse(deltaP, 26)
if deltaP_inv is None:
    print("No modular inverse for deltaP. Try another assumption.")
    exit()

a = (deltaC * deltaP_inv) % 26

b = (C1 - a*P1) % 26

print(f"Assumed a={a}, b={b}")

plaintext = affine_decrypt(ciphertext, a, b)
if plaintext:
    print("Decrypted text (first 500 chars):")
    print(plaintext[:500])
else:
    print("Decryption failed or not meaningful. Try different assumptions.")
