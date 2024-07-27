```markdown
# Fixed Width Parser

This project provides a parser for fixed-width files and converts them into CSV or JSON formats. It includes Docker support for easy execution.

## Project Structure

- `fixed_width_parser.py`: Python script for parsing.
- `Dockerfile`: Docker container setup.
- `requirements.txt`: Python dependencies.
- `spec.txt`: Example specification file.
- `data.txt`: Example fixed-width data file.
- `README.md`: Project documentation.

## Setup and Usage

### With Docker

1. **Build the Docker Image**:
   ```sh
   docker build -t fixed-width-parser .
   ```

2. **Run the Docker Container**:
   ```sh
   docker run --rm -v $(pwd):/app fixed-width-parser python fixed_width_parser.py spec.txt data.txt output.csv errors.txt summary.csv --output-format csv --summary-format csv
   ```

### Without Docker

1. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

2. **Run the Script**:
   ```sh
   python fixed_width_parser.py spec.txt data.txt output.csv errors.txt summary.csv --output-format csv --summary-format csv
   ```

## Command Line Arguments

- `SPEC_FILE`: Path to the specification file (e.g., `spec.txt`).
- `FIXED_WIDTH_FILE`: Path to the fixed-width file to parse (e.g., `data.txt`).
- `OUTPUT_FILE`: Path to the output file in CSV or JSON format (e.g., `output.csv` or `output.json`).
- `ERROR_FILE`: Path to the error log file (e.g., `errors.txt`).
- `SUMMARY_FILE`: Path to the summary file in CSV or JSON format (e.g., `summary.csv` or `summary.json`).
- `--output-format FORMAT`: Output file format (`csv` or `json`, default: `csv`).
- `--summary-format FORMAT`: Summary file format (`csv` or `json`, default: `csv`).

## Example Files

- **Specification File (`spec.txt`)**:
  ```
  name:10
  address:20
  age:3
  ```

- **Fixed-Width File (`data.txt`)**:
  ```
  satish      123 Main St       25
  drit        456 gnt rd        30
  nrt         789 nrt Rd        22
  ```

## Output

- **Output File**: Parsed data in CSV or JSON format.
- **Error File**: Lines that did not match the expected length.
- **Summary File**: Statistics about the parsing process.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```