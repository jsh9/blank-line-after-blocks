"""Test case for loops and with statements."""
import json

def process_files(filenames):
    results = []
    for filename in filenames:
        try:
            with open(filename) as f:
                data = json.load(f)

            results.append(data)
        except FileNotFoundError:
            print(f'File {filename} not found')
        except json.JSONDecodeError:
            print(f'Invalid JSON in {filename}')

    return results

def count_items(items, threshold=10):
    count = 0
    while count < threshold:
        for item in items:
            if item > count:
                print(f'Found item {item} > {count}')
                count += 1
                break

        else:
            print('No more items found')
            break

    return count

if __name__ == '__main__':
    files = ['data1.json', 'data2.json']
    data = process_files(files)
    result = count_items([1, 5, 10, 15, 20])
    print(f'Final count: {result}')
