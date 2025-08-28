# Test cases extracted from flake8-clean-block project
# Source: https://github.com/cyyc1/flake8-clean-block
# These represent "before" cases that need blank line formatting

# Basic for loop
a = 2
for i in range(5):
    a += 1
print(a)

# Multiple control structures
if True:
    print('test')
if True:
    print('test2')
for i in range(2):
    print(i)
while False:
    break

# Nested if statements
if 3 >= 2:
    if 2 > 1:
        print('yes')
    print('no')
print('good')

# Function with if/elif/else
def test_func():
    x, y = 1, 2
    if x < 5:
        print(x)
    elif y == 2:
        print(y)
    else:
        raise ValueError
    return 2

# While loop
while False:
    print(1)
print(2)

# Try/except blocks with nested if
try:
    f = open('myfile.txt')
except OSError as err:
    print(2)
    if True:
        b = 1
    b = 2
except ValueError:
    print('asdf')

# With statement
with open(__file__) as fp:
    data = fp.read()
print(len(data))

# Function with nested control structures
def some_func(arg1: list, arg2: list) -> int:
    for i in range(len(arg1)):
        for j in range(len(arg2)):
            print(i)
        print(j)
    return 5
if True:
    some_func([1, 2, 3], [2, 3])
print('Good morning')

# Complex nested control structures
def complex_func():
    x, y, z = 1, 2, 3
    if x < 5:
        print(x)
        while z > 0:
            print(z)
            z -= 1
    elif y == 2:
        print(y)
        for k in range(10):
            print(k)
            for l in range(2):
                l += 2
            bb = 1
    else:
        raise ValueError
    return 2

# Simple if/elif block
def simple_func():
    a, b = 'a', 'b'
    depth = 0
    if a == 'a':
        depth += 1
    elif b == 'b':
        depth -= 1
    j = 1
    return depth + j

# For loop with try/except
import sys
for arg in ['test']:
    try:
        f = open(arg, 'w')
    except OSError:
        print('cannot open', arg)
    else:
        print(arg, 'opened successfully')
        for k in range(2):
            print(k)
        f.close()

# Try/finally block
try:
    pass
finally:
    for kk in range(5):
        pass
    print('Hello world!')

# With statement containing for loop
with open(__file__) as fp:
    data = fp.read()
    for ii in range(min(10, len(data))):
        pass
print('done')

# Nested loop with manual spacing
a = 2
for i in range(5):
    for j in range(3):
        a += j

    a += i
print(a)

# Single line for statement - no transformation needed
for i in range(5): pass

# Single line for with following code - no transformation needed
for i in range(5): pass

print('after single line')

# Deep nested loops that need formatting
for i in range(5):
    for j in range(5):
        for k in range(5):
            for l in range(5):
                for m in range(5):
                    for n in range(5):
                        for o in range(5):
                            for p in range(5):
                                for q in range(5):
                                    for r in range(5):
                                        for s in range(5):
                                            for t in range(5):
                                                for u in range(5):
                                                    for v in range(5):
                                                        for w in range(5):
                                                            for x in range(5):
                                                                print(1)
print(2)

# Deep nested loops already formatted - no transformation needed
for i in range(5):
    for j in range(5):
        for k in range(5):
            for l in range(5):
                for m in range(5):
                    for n in range(5):
                        for o in range(5):
                            for p in range(5):
                                for q in range(5):
                                    for r in range(5):
                                        for s in range(5):
                                            for t in range(5):
                                                for u in range(5):
                                                    for v in range(5):
                                                        for w in range(5):
                                                            for x in range(5):
                                                                print(1)

print(2)

# Function with if block that needs formatting
def some_func_needing_format(arg1):
    if arg1 == 2:
        return 1
    return 2

# Class with methods containing control structures that need formatting
class MyClass:
    def __init__(self, arg1):
        if arg1 == 2:
            self.my_attr = 1
        self.my_attr = 2

    def do_something(self, arg1):
        for i in range(20):
            print(i)
        print(arg1)

    def do_something_else(self, arg1, arg2):
        if 5 in arg1:
            print(arg1)
        for j in arg2:
            foo = 3 + 4
        return 5

# Empty code case
# (no code here - represents empty string)

# Function with properly formatted if block - no transformation needed
def another_func(arg1):
    if arg1:
        return 2

    return 1
