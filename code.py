"""
s = input("Enter the string: ")

sub = ""
max_len = 0

for char in s:
    if char in sub:
        sub = sub[sub.index(char) + 1:]
    sub += char
    max_len = max(max_len, len(sub))

print(max_len)
