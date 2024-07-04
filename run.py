from functools import reduce
import itertools

a = [[1, 2], [3, 4], [5, 6]]
print([[item[0], item[1]] for item in a])
print(list(itertools.chain.from_iterable(a)))

print(list(itertools.chain(*a)))
print(list(itertools.chain(**a)))