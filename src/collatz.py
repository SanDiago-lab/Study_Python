def collatz(number):
    if number % 2 == 0:
        result = number // 2
    else:
        result = 3 * number + 1

    print(result)
    return result


print("整数を入力してください:")
try:
    n = int(input())

    # 入力された数がすでに1の場合はループに入らない
    while n != 1:
        n = collatz(n)

except ValueError:
    print("エラー: 整数を入力してください。")