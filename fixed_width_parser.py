import csv
import json
import argparse

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
        with open(self.spec_file_path, 'r') as file:
            spec = []
            for line in file:
                field, length = line.strip().split(':')
                spec.append((field, int(length)))
        return spec

    def validate_and_parse_fixed_width_file(self, spec):
        total_length = sum(length for _, length in spec)
        parsed_data = []
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
                    
        summary = {
            "total_lines": total_lines,
            "parsed_lines": parsed_lines,
            "error_lines": error_lines
        }

        return parsed_data, summary

    def write_output(self, parsed_data, headers):
        if self.output_format == "csv":
            with open(self.output_file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(parsed_data)
        elif self.output_format == "json":
            with open(self.output_file_path, 'w', encoding='utf-8') as file:
                json.dump([dict(zip(headers, row)) for row in parsed_data], file, indent=4)

    def write_summary(self, summary):
        if self.summary_format == "csv":
            with open(self.summary_file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Metric", "Value"])
                for key, value in summary.items():
                    writer.writerow([key, value])
        elif self.summary_format == "json":
            with open(self.summary_file_path, 'w', encoding='utf-8') as file:
                json.dump(summary, file, indent=4)

    def execute(self):
        spec = self.parse_spec_file()
        headers = [field for field, _ in spec]
        parsed_data, summary = self.validate_and_parse_fixed_width_file(spec)
        self.write_output(parsed_data, headers)
        self.write_summary(summary)


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
        self._spec_file_path = spec_file_path
        return self

    def fixed_width_file(self, fixed_width_file_path):
        self._fixed_width_file_path = fixed_width_file_path
        return self

    def output_file(self, output_file_path):
        self._output_file_path = output_file_path
        return self

    def error_file(self, error_file_path):
        self._error_file_path = error_file_path
        return self

    def summary_file(self, summary_file_path):
        self._summary_file_path = summary_file_path
        return self

    def output_format(self, output_format):
        self._output_format = output_format
        return self

    def summary_format(self, summary_format):
        self._summary_format = summary_format
        return self

    def build(self):
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

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Parse fixed width file and convert to CSV or JSON.")
    arg_parser.add_argument("spec_file", help="Path to the specification file.")
    arg_parser.add_argument("fixed_width_file", help="Path to the fixed width file.")
    arg_parser.add_argument("output_file", help="Path to the output file.")
    arg_parser.add_argument("error_file", help="Path to the error log file.")
    arg_parser.add_argument("summary_file", help="Path to the summary file.")
    arg_parser.add_argument("--output-format", choices=["csv", "json"], default="csv", help="The format for the output file (default: csv).")
    arg_parser.add_argument("--summary-format", choices=["csv", "json"], default="csv", help="The format for the summary file (default: csv).")

    args = arg_parser.parse_args()
    main(args)