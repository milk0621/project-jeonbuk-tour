a = ['전주시', '군산시', '정읍시', '익산시']
a = list(map(lambda x : f"\'{x}\'", a))
print(", ".join(a))