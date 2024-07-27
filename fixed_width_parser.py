import csv
import json
import argparse
import os

class FixedWidthParser:
    def __init__(self, spec_file_path, fixed_width_file_path, output_file_path, error_file_path, summary_file_path, output_format, summary_format):
        self.spec_file_path = spec_file_path
        self.fixed_width_file_path = fixed_width_file_path
        self.output_file_path = output_file_path
        self.error_file_path = error_file_path
        self.summary_file_path = summary_file_path
        self.output_format = output_format
        self.summary_format = summary_format

    def parse_spec_file(self):
        """Parse the specification file to get field names and lengths."""
        if not os.path.exists(self.spec_file_path):
            raise FileNotFoundError(f"Specification file not found: {self.spec_file_path}")

        try:
            with open(self.spec_file_path, 'r') as file:
                spec = []
                for line in file:
                    field, length = line.strip().split(':')
                    spec.append((field, int(length)))
            if not spec:
                raise ValueError(f"Specification file is empty: {self.spec_file_path}")
            return spec
        except Exception as e:
            raise Exception(f"Error reading spec file: {e}")

    def validate_and_parse_fixed_width_file(self, spec):
        """Validate and parse the fixed width file based on the specification."""
        total_length = sum(length for _, length in spec)
        parsed_data = []

        if not os.path.exists(self.fixed_width_file_path):
            raise FileNotFoundError(f"Fixed width file not found: {self.fixed_width_file_path}")

        try:
            with open(self.fixed_width_file_path, 'r', encoding='utf-8') as file, \
                 open(self.error_file_path, 'w', encoding='utf-8') as error_file:

                total_lines = 0
                parsed_lines = 0
                error_lines = 0

                for line_number, line in enumerate(file, start=1):
                    total_lines += 1
                    line = line.rstrip('\n')
                    if len(line) == total_length:
                        parsed_line = []
                        start = 0
                        for _, length in spec:
                            end = start + length
                            parsed_line.append(line[start:end].strip())
                            start = end
                        parsed_data.append(parsed_line)
                        parsed_lines += 1
                    else:
                        error_file.write(f"Line {line_number} is not of the expected length {total_length}. Actual length: {len(line)}. Content: '{line}'\n")
                        error_lines += 1

            if total_lines == 0:
                raise ValueError(f"Fixed width file is empty: {self.fixed_width_file_path}")

            summary = {
                "total_lines": total_lines,
                "parsed_lines": parsed_lines,
                "error_lines": error_lines
            }

            return parsed_data, summary
        except Exception as e:
            raise Exception(f"Error processing fixed width file: {e}")

    def write_output(self, parsed_data, headers):
        """Write the parsed data to the output file in the specified format."""
        try:
            if self.output_format == "csv":
                with open(self.output_file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    writer.writerows(parsed_data)
            elif self.output_format == "json":
                with open(self.output_file_path, 'w', encoding='utf-8') as file:
                    json.dump([dict(zip(headers, row)) for row in parsed_data], file, indent=4)
        except Exception as e:
            raise Exception(f"Error writing output file: {e}")

    def write_summary(self, summary):
        """Write the summary of the parsing process to the summary file in the specified format."""
        try:
            if self.summary_format == "csv":
                with open(self.summary_file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Metric", "Value"])
                    for key, value in summary.items():
                        writer.writerow([key, value])
            elif self.summary_format == "json":
                with open(self.summary_file_path, 'w', encoding='utf-8') as file:
                    json.dump(summary, file, indent=4)
        except Exception as e:
            raise Exception(f"Error writing summary file: {e}")

    def execute(self):
        """Execute the parsing process."""
        try:
            spec = self.parse_spec_file()
            headers = [field for field, _ in spec]
            parsed_data, summary = self.validate_and_parse_fixed_width_file(spec)
            self.write_output(parsed_data, headers)
            self.write_summary(summary)
        except Exception as e:
            print(f"Execution error: {e}")

class FixedWidthParserBuilder:
    def __init__(self):
        self._spec_file_path = None
        self._fixed_width_file_path = None
        self._output_file_path = None
        self._error_file_path = None
        self._summary_file_path = None
        self._output_format = "csv"
        self._summary_format = "csv"

    def spec_file(self, spec_file_path):
        """Set the specification file path."""
        self._spec_file_path = spec_file_path
        return self

    def fixed_width_file(self, fixed_width_file_path):
        """Set the fixed width file path."""
        self._fixed_width_file_path = fixed_width_file_path
        return self

    def output_file(self, output_file_path):
        """Set the output file path."""
        self._output_file_path = output_file_path
        return self

    def error_file(self, error_file_path):
        """Set the error log file path."""
        self._error_file_path = error_file_path
        return self

    def summary_file(self, summary_file_path):
        """Set the summary file path."""
        self._summary_file_path = summary_file_path
        return self

    def output_format(self, output_format):
        """Set the output file format."""
        self._output_format = output_format
        return self

    def summary_format(self, summary_format):
        """Set the summary file format."""
        self._summary_format = summary_format
        return self

    def build(self):
        """Build and return the FixedWidthParser object."""
        required_parameters = [
            self._spec_file_path, self._fixed_width_file_path, 
            self._output_file_path, self._error_file_path, self._summary_file_path
        ]

        if any(param is None for param in required_parameters):
            missing_params = [param for param in ["spec_file", "fixed_width_file", "output_file", "error_file", "summary_file"] if getattr(self, f'_{param}') is None]
            raise ValueError(f"Missing required input parameters: {', '.join(missing_params)}")

        return FixedWidthParser(
            self._spec_file_path,
            self._fixed_width_file_path,
            self._output_file_path,
            self._error_file_path,
            self._summary_file_path,
            self._output_format,
            self._summary_format
        )

def main(args):
    """Main function to execute the parsing process."""
    try:
        parser = FixedWidthParserBuilder()\
            .spec_file(args.spec_file)\
            .fixed_width_file(args.fixed_width_file)\
            .output_file(args.output_file)\
            .error_file(args.error_file)\
            .summary_file(args.summary_file)\
            .output_format(args.output_format)\
            .summary_format(args.summary_format)\
            .build()
        
        parser.execute()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Parse fixed width file and convert to CSV or JSON.")
    arg_parser.add_argument("--spec-file", required=True, help="Path to the specification file.")
    arg_parser.add_argument("--fixed-width-file", required=True, help="Path to the fixed width file.")
    arg_parser.add_argument("--output-file", required=True, help="Path to the output file.")
    arg_parser.add_argument("--error-file", required=True, help="Path to the error log file.")
    arg_parser.add_argument("--summary-file", required=True, help="Path to the summary file.")
    arg_parser.add_argument("--output-format", choices=["csv", "json"], default="csv", help="The format for the output file (default: csv).")
    arg_parser.add_argument("--summary-format", choices=["csv", "json"], default="csv", help="The format for the summary file (default: csv).")

    args = arg_parser.parse_args()
    main(args)