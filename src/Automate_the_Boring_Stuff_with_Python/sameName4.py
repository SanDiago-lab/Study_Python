def spam():
    print(eggs) # エラー!
    eggs = 'spam local'

eggs = 'global'
spam()