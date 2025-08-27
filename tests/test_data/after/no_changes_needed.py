"""Test case for code that shouldn't be modified."""

def simple_function():
    return 'hello world'

def another_function():
    x = 1
    y = 2
    return x + y

class SimpleClass:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

# Module level code
CONSTANT = 42
variable = 'test'

# Function calls
result1 = simple_function()
result2 = another_function()

# Object creation
obj = SimpleClass(10)
value = obj.get_value()

print(f'Results: {result1}, {result2}, {value}')
