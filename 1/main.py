def left_shift(bits, n):
    return bits[n:] + bits[:n]

def generate_subkeys(key20):
    # Предполагается, что key20 – это строка из '0'/'1' длиной 20
    # Разделяем на две половины по 10 бит
    left_part = key20[:10]
    right_part = key20[10:]
    # Сдвигаем влево на 1 бит
    left_part = left_shift(left_part, 1)
    right_part = left_shift(right_part, 1)
    subkey1 = left_part[:8] + right_part[:8]  # первые 8 бит из обеих половин
    
    # Сдвигаем влево на 2 бита (дополнительно)
    left_part = left_shift(left_part, 2)
    right_part = left_shift(right_part, 2)
    subkey2 = left_part[:8] + right_part[:8]
    return subkey1, subkey2

def f_function(half, subkey):
    # Пример простой операции: XOR полублока с подключом
    return ''.join(str(int(a)^int(b)) for a,b in zip(half, subkey))

def sdes_encrypt(plaintext, key20):
    subkey1, subkey2 = generate_subkeys(key20)
    left, right = plaintext[:4], plaintext[4:]
    
    # Раунд 1
    temp = f_function(right, subkey1)
    left, right = format(int(left, 2) ^ int(temp, 2), 'b').zfill(4), right
    
    # Раунд 2
    temp = f_function(right, subkey2)
    left, right = format(int(left, 2) ^ int(temp, 2), 'b').zfill(4), right
    
    return left + right

def sdes_decrypt(ciphertext, key20):
    subkey1, subkey2 = generate_subkeys(key20)
    left, right = ciphertext[:4], ciphertext[4:]
    
    # Раунд 1 (с subkey2)
    temp = f_function(right, subkey2)
    left, right = format(int(left, 2) ^ int(temp, 2), 'b').zfill(4), right
    
    # Раунд 2 (с subkey1)
    temp = f_function(right, subkey1)
    left, right = format(int(left, 2) ^ int(temp, 2), 'b').zfill(4), right
    
    return left + right

if __name__ == "__main__":
    test_key = "10100000100111100001"  # 20 бит
    test_plain = "10110011"            # 8 бит
    encrypted = sdes_encrypt(test_plain, test_key)
    print("Зашифрованный текст:", encrypted)
    decrypted = sdes_decrypt(encrypted, test_key)
    print("Расшифрованный текст:", decrypted)