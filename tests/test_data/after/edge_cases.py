"""Test case for edge cases and special scenarios."""

# Single line if
if True: print('one liner')

# Empty blocks
def empty_conditions(x):
    if x > 0:
        pass

    print('after if')

    while x > 0:
        x -= 1

    print('after while')

    for i in range(1):
        pass

    print('after for')

# Nested in class
class TestClass:
    def method(self):
        try:
            if self.condition():
                with self.get_context():
                    self.do_work()

                self.cleanup()

        except Exception as e:
            self.handle_error(e)

        print('method complete')

    def condition(self):
        return True

    def get_context(self):
        return open('test.txt', 'w')

    def do_work(self):
        pass

    def cleanup(self):
        pass

    def handle_error(self, error):
        print(f'Error: {error}')

# Edge case: blocks at end of file
def final_function():
    if True:
        print('final block')
