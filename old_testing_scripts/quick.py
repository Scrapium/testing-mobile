import base64

string1 = "Tsb/NGr2wlyiA2nQgYVLz09gnTo="
string2 = "+1HZEOZIpJFk698eab1i7tAQyoQ="

decoded1 = base64.b64decode(string1)
decoded2 = base64.b64decode(string2)

decoded_string1 = decoded1.decode('utf-8', 'ignore')  # 'ignore' to skip invalid characters
decoded_string2 = decoded2.decode('utf-8', 'ignore')

print(decoded_string1)
print(decoded_string2)