"""Test case for code that's already properly formatted."""

def process_items(items):
    results = []

    for item in items:
        if item > 0:
            results.append(item * 2)

        else:
            results.append(0)

    return results

def handle_errors():
    try:
        with open('nonexistent.txt') as f:
            data = f.read()

        return data
    except FileNotFoundError:
        print('File not found')
        return None

def main():
    data = [1, -2, 3, -4, 5]
    processed = process_items(data)

    while processed:
        item = processed.pop(0)
        if item > 5:
            print(f'Large item: {item}')

        else:
            print(f'Small item: {item}')

    print('All done!')

if __name__ == '__main__':
    main()
