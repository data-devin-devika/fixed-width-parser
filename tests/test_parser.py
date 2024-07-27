### Test Script

**tests/test_parser.py**
```python
import unittest
from fixed_width_parser import parse_spec_file, validate_and_parse_fixed_width_file, write_csv
import os

class TestFixedWidthParser(unittest.TestCase):
    
    def setUp(self):
        self.spec_file = "spec.txt"
        self.fixed_width_file = "data.txt"
        self.csv_file = "output.csv"
        self.valid_output_file = "valid_data.txt"
        self.error_file = "errors.txt"
        self.spec_content = "name:9\naddress:17\nage:2\n"
        self.fixed_width_content = "John      123 Main St        25\nAlice     456 Oak Ave        30\nBob       789 Pine Rd        22\n"
        self.invalid_fixed_width_content = "John      123 Main St       25\nAlice     456 Oak Ave       30\nBob       789 Pine Rd       22\nsatish    789 Pine Rd       22 this ismatching except last row."

        with open(self.spec_file, 'w') as f:
            f.write(self.spec_content)
        
        with open(self.fixed_width_file, 'w') as f:
            f.write(self.fixed_width_content)

    def tearDown(self):
        os.remove(self.spec_file)
        os.remove(self.fixed_width_file)
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)
        if os.path.exists(self.valid_output_file):
            os.remove(self.valid_output_file)
        if os.path.exists(self.error_file):
            os.remove(self.error_file)

    def test_parse_spec_file(self):
        expected = [("name", 9), ("address", 17), ("age", 2)]
        result = parse_spec_file(self.spec_file)
        self.assertEqual(result, expected)

    def test_validate_and_parse_fixed_width_file(self):
        spec = [("name", 9), ("address", 17), ("age", 2)]
        expected = [
            ["John", "123 Main St", "25"],
            ["Alice", "456 Oak Ave", "30"],
            ["Bob", "789 Pine Rd", "22"]
        ]
        
        parsed_data = validate_and_parse_fixed_width_file(self.fixed_width_file, spec, self.valid_output_file, self.error_file)
        self.assertEqual(parsed_data, expected)
        
        with open(self.valid_output_file, 'r', encoding='utf-8') as file:
            valid_content = file.read().strip().split('\n')
        self.assertEqual(valid_content, [
            "John      123 Main St        25",
            "Alice     456 Oak Ave        30",
            "Bob       789 Pine Rd        22"
        ])
        
        with open(self.error_file, 'r', encoding='utf-8') as file:
            error_content = file.read().strip()
        self.assertEqual(error_content, "")

        with open(self.fixed_width_file, 'w') as f:
            f.write(self.invalid_fixed_width_content)

        with self.assertRaises(ValueError):
            validate_and_parse_fixed_width_file(self.fixed_width_file, spec, self.valid_output_file, self.error_file)

    def test_write_csv(self):
        data = [
            ["John", "123 Main St", "25"],
            ["Alice", "456 Oak Ave", "30"],
            ["Bob", "789 Pine Rd", "22"]
        ]
        headers = ["name", "address", "age"]
        write_csv(data, self.csv_file, headers)
        with open(self.csv_file, 'r', encoding='utf-8') as file:
            content = file.read().strip().split('\n')
            expected = [
                "name,address,age",
                "John,123 Main St,25",
                "Alice,456 Oak Ave,30",
                "Bob,789 Pine Rd,22"
            ]
            self.assertEqual(content, expected)

if __name__ == "__main__":
    unittest.main()