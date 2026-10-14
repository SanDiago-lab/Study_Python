birthdays = {'アリス': '4/1', 'ボブ': '12/12', 'キャロル': '4/4'}

while True:
    print('名前を入力してください: (終了するにはEnterだけを押してください)')
    name = input()
    if name == '':
        break

    if name in birthdays:
        print(f"{name}の誕生日は{birthdays[name]}です。")
    else:
        print(f"{name}の誕生日は登録されていません。")
        print('誕生日を入力してください:')
        bday = input()
        birthdays[name] = bday
        print(f"{name}の誕生日を{bday}として登録しました。")