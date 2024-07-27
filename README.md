# Fixed Width Parser

This project provides a parser for handling fixed-width files and converting them into delimited files like CSV or JSON. It includes a Docker setup for easy execution of the code.

## Project Structure

	•	fixed_width_parser.py
	•	Dockerfile
	•	requirements.txt
	•	spec.txt
	•	data.txt
	•	README.md

## Features

- Parses fixed-width files based on a specification file.
- Generates output in CSV or JSON format.
- Logs errors encountered during parsing.
- Creates a summary file with parsed and error statistics.
- Docker support for easy execution.

## Requirements

- Python 3.x
- Docker (optional, for containerized execution)

## Setup

### Running with Docker

1. **Build the Docker Image**:
   ```sh
   docker build -t fixed-width-parser .

2.	Run the Docker Container:
docker run --rm -v $(pwd):/app fixed-width-parser

3.	Custom Command Example:

docker run --rm -v $(pwd):/app fixed-width-parser python fixed_width_parser.py spec.txt data.txt output.json errors.txt summary.json --output-format json --summary-format json

Usage

python fixed_width_parser.py [SPEC_FILE] [FIXED_WIDTH_FILE] [OUTPUT_FILE] [ERROR_FILE] [SUMMARY_FILE] [--output-format FORMAT] [--summary-format FORMAT]

	•	SPEC_FILE: Path to the specification file (e.g., spec.txt).
	•	FIXED_WIDTH_FILE: Path to the fixed-width file to parse (e.g., data.txt).
	•	OUTPUT_FILE: Path to the output file in CSV or JSON format (e.g., output.csv or output.json).
	•	ERROR_FILE: Path to the error log file (e.g., errors.txt).
	•	SUMMARY_FILE: Path to the summary file in CSV or JSON format (e.g., summary.csv or summary.json).
	•	--output-format FORMAT: The format for the output file. Options are csv or json (default: csv).
	•	--summary-format FORMAT: The format for the summary file. Options are csv or json (default: csv).


Example Specification File (spec.txt)

name:10
address:20
age:3


Example Fixed-Width File (data.txt)

satish      123 Main St          25
drti        456 NRT Ave          30
sdtr        789 gut  Rd          22


Output

	•	Output File: Contains parsed data in the specified format (CSV or JSON).
	•	Error File: Contains lines that did not match the expected length.
	•	Summary File: Contains statistics about the parsing process (number of total lines, parsed lines, and error lines).

Error Handling

Errors encountered during parsing will be logged in the specified error file. The summary file will provide a count of total lines processed, parsed successfully, and those that encountered errors.

Contributing

Feel free to open an issue or submit a pull request if you find any bugs or have suggestions for improvements.