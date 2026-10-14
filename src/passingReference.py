def eggs(some_parameter):
    some_parameter.append('Hello')

spam = [1, 2, 3]
eggs(spam)
print(spam)  # This will print [1, 2, 3, 'Hello'] because the list is modified in place