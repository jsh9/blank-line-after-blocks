"""Test case for complex nested structures."""

class DataProcessor:
    def __init__(self, data):
        self.data = data
        self.processed = []

    def process_all(self):
        for item in self.data:
            if isinstance(item, dict):
                try:
                    if 'required_field' in item:
                        with open(item['file_path']) as f:
                            content = f.read()
                        processed_item = self.transform_data(content, item)
                        self.processed.append(processed_item)
                    else:
                        print('Missing required field')
                except FileNotFoundError:
                    print(f"File not found: {item.get('file_path', 'unknown')}")
                except Exception as e:
                    print(f'Error processing item: {e}')
                finally:
                    item['processed'] = True
            else:
                if item is not None:
                    self.processed.append(str(item))
        return self.processed

    def transform_data(self, content, metadata):
        if content.strip():
            try:
                result = {
                    'content': content,
                    'length': len(content),
                    'metadata': metadata
                }
                return result
            except Exception:
                return None
        return {'empty': True}

# Usage example
if __name__ == '__main__':
    data = [
        {'file_path': 'test1.txt', 'required_field': True},
        {'file_path': 'test2.txt', 'required_field': True},
        'simple_string',
        None
    ]
    processor = DataProcessor(data)
    results = processor.process_all()
    for result in results:
        print(result)
