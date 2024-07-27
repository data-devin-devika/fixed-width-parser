import csv
import argparse

def parse_spec_file(spec_file_path):
    with open(spec_file_path, 'r') as file:
        spec = []
        for line in file:
            field, length = line.strip().split(':')
            spec.append((field, int(length)))
    return spec

def validate_and_parse_fixed_width_file(fixed_width_file_path, spec, valid_output_file_path, error_file_path):
    total_length = sum(length for _, length in spec)
    parsed_data = []
    with open(fixed_width_file_path, 'r', encoding='utf-8') as file, \
         open(valid_output_file_path, 'w', encoding='utf-8') as valid_file, \
         open(error_file_path, 'w', encoding='utf-8') as error_file:
        
        for line_number, line in enumerate(file, start=1):
            line = line.rstrip('\n')
            if len(line) == total_length:
                valid_file.write(line + '\n')
                parsed_line = []
                start = 0
                for _, length in spec:
                    end = start + length
                    parsed_line.append(line[start:end].strip())
                    start = end
                parsed_data.append(parsed_line)
            else:
                error_file.write(f"Line {line_number} is not of the expected length {total_length}. Actual length: {len(line)}. Content: '{line}'\n")
    return parsed_data

def write_csv(parsed_data, csv_file_path, headers):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(parsed_data)

def main(spec_file_path, fixed_width_file_path, csv_file_path, valid_output_file_path, error_file_path):
    spec = parse_spec_file(spec_file_path)
    headers = [field for field, _ in spec]
    parsed_data = validate_and_parse_fixed_width_file(fixed_width_file_path, spec, valid_output_file_path, error_file_path)
    write_csv(parsed_data, csv_file_path, headers)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse fixed width file and convert to CSV.")
    parser.add_argument("spec_file", help="Path to the specification file.")
    parser.add_argument("fixed_width_file", help="Path to the fixed width file.")
    parser.add_argument("csv_file", help="Path to the output CSV file.")
    parser.add_argument("valid_output_file", help="Path to the output valid fixed width file.")
    parser.add_argument("error_file", help="Path to the error log file.")
    args = parser.parse_args()
    main(args.spec_file, args.fixed_width_file, args.csv_file, args.valid_output_file, args.error_file)