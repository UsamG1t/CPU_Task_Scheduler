ans = []
while (s:= input()):
    a, b, c, d = eval(s)
    ans.append(f'{a}, {b // 100}, {(tmp := max(1, c // 100))}, {int(max(tmp // 1.5, 1, d // 100))}')

print(*ans, sep = '\n')