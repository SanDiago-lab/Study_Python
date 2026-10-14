import random

messages = ['確かにそうだ', '間違いなくそうだ', 
            'はい', 
            'なんとも。もう一度やってみて', 
            '後でもう一度聞いてみて', 
            '集中してもう一度聞いてみて', 
            '私の答えはノーです', 
            '見通しは良くない', 
            'とても疑わしい']

print(messages[random.randint(0, len(messages) - 1)])