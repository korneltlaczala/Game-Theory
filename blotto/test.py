import copy

testlist = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
newlist = copy.deepcopy(testlist)
print(testlist)
print(newlist)
print("====================")
newlist[0][0] = 100
print(testlist)
print(newlist)