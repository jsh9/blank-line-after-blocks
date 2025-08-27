#!/usr/bin/env python3
"""Test case for basic if statements."""

def process_data(data):
    if data:
        print('Processing data')
        result = data * 2
        return result

    print('No data to process')
    return None

def main():
    items = [1, 2, 3, 4, 5]
    for item in items:
        if item % 2 == 0:
            print(f'Even: {item}')
        else:
            print(f'Odd: {item}')

    print('Done processing items')

if __name__ == '__main__':
    main()
