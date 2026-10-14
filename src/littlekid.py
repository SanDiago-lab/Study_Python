print('What is your name?')
name = input()
print('Then, what is your age?')
age = int(input())
if name == 'Alice':
    print('やぁ,Alice.')
elif age < 12:
    print('Aliceじゃないね,お嬢ちゃん.')
else:
    print('君はAliceでも子供でもないね.')
