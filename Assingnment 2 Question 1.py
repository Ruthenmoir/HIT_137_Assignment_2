# This code assumes that we are shifting the characters by their index in the alphabet and replacing the original character with the letter located at the new index.

import string

def build_translation_table(n, m):
    table = {}
    
    # Process lowercase letters: a-m and n-z are two groups of 13 letters each.
    for letter in string.ascii_lowercase:
        if 'a' <= letter <= 'm':
            # Compute position in 0-12 range and shift forward by n * m.
            pos = ord(letter) - ord('a') # index of the letter k in the alpahbet
            shift = n * m % 13
            new_pos = (pos + shift) % 13
            new_letter = chr(new_pos + ord('a'))
        else:  # letter between n and z
            # Compute position relative to 'n' and shift backward by n + m.
            pos = ord(letter) - ord('n')
            shift = n + m % 13
            new_pos = (pos - shift) % 13
            new_letter = chr(new_pos + ord('n'))
        table[ord(letter)] = ord(new_letter)
    
    # Process uppercase letters: A-M and N-Z.
    for letter in string.ascii_uppercase:
        if 'A' <= letter <= 'M':
            # Compute position in 0-12 range and shift backward by n.
            pos = ord(letter) - ord('A')
            shift = n % 13
            new_pos = (pos - shift) % 13
            new_letter = chr(new_pos + ord('A'))
        else:  # letter between N and Z
            # Compute position relative to 'N' and shift forward by m^2.
            pos = ord(letter) - ord('N')
            shift = m ** 2 % 13
            new_pos = (pos + shift) % 13
            new_letter = chr(new_pos + ord('N'))
        table[ord(letter)] = ord(new_letter)
    
    # Special characters, digits, punctuation, and whitespace remain unchanged.
    for char in string.punctuation + string.digits + string.whitespace:
        table[ord(char)] = ord(char)
    
    return table

def build_decryption_table(n, m):
    # Invert the encryption table to create the decryption mapping.
    encryption_table = build_translation_table(n, m)
    decryption_table = {value: key for key, value in encryption_table.items()}
    return decryption_table

def encrypt_text(text, n, m):
    table = build_translation_table(n, m)
    return text.translate(table)

def decrypt_text(text, n, m):
    table = build_decryption_table(n, m)
    return text.translate(table)

def check_decryption(original_text, decrypted_text):
    """
    Check if the decrypted text matches the original text.
    Returns True if they match; otherwise, returns False.
    """
    return original_text == decrypted_text

def main():
    try:
        n = int(input("Enter the value for n: "))
        m = int(input("Enter the value for m: "))
    except ValueError:
        print("Please enter valid integers for n and m.")
        return

    # Read the original text from file.
    try:
        with open("raw_text.txt", "r", encoding="utf-8") as f:
            original_text = f.read()
    except FileNotFoundError:
        print("The file 'raw_text.txt' was not found.")
        return

    # Encrypt the text.
    encrypted_text = encrypt_text(original_text, n, m)
    with open("encrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(encrypted_text)
    print("Encryption complete. Encrypted text saved to 'encrypted_text.txt'.")

    # Decrypt the text.
    decrypted_text = decrypt_text(encrypted_text, n, m)
    with open("decrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(decrypted_text)
    print("Decryption complete. Decrypted text saved to 'decrypted_text.txt'.")

    # Check that the decryption correctly recovered the original text.
    is_correct = check_decryption(original_text, decrypted_text)
    print("Original text:", original_text)
    print("Encrypted text:", encrypted_text)
    print("Decrypted text:", decrypted_text)
    print("Decryption correct:", is_correct)

if __name__ == "__main__":
    main()
