tuple1 = (1, 3, 4, 5)
tuple2 = (1, 4, 5, 6)
tuple3 = (1, 6, 7, 4)

result1 = set(set(tuple1) & set(tuple2) & set(tuple3))
print(result1)

temp1 = set(tuple1).difference(set(tuple2)|set(tuple3))
temp2 = set(tuple2).difference(set(tuple1)|set(tuple3))
temp3 = set(tuple3).difference(set(tuple1)|set(tuple2))

result2 = temp1.union(temp2).union(temp3)
print(result2)


result3 = []
for a, b, c in zip(tuple1, tuple2, tuple3):
    if a == b == c:
        result3.append(a)
print(result3)
