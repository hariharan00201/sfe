keyy = "secret"

ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%=:?./|~>*()<'





def encryptMessage (messages):
    return cipherMessage(messages, keyy, 'encrypt')


def decryptMessage(messages):
    return cipherMessage(messages, keyy, 'decrypt')



def cipherMessage (messages, keys, mode):
    cipher = []
    k_index = 0
    key = keys
    for i in messages:
        text = ALPHA.find(i)

        if mode == 'encrypt':
             text += ALPHA.find(key[k_index])
             key += i
        elif mode == 'decrypt':
             text -= ALPHA.find(key[k_index])
             key += ALPHA[text]
        text %= len(ALPHA)
        k_index += 1
        cipher.append(ALPHA[text])
    return ''.join(cipher)

