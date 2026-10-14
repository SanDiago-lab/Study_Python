def spam():
    eggs = 'spam local'
    print(eggs) # 'spam local'を表示

def bacon():
    eggs = 'bacon local'
    print(eggs) # 'bacon local'を表示
    spam()
    print(eggs) # 'bacon local'を表示

eggs = 'global'
bacon()
print(eggs) # 'global'を表示