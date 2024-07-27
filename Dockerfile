# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run fixed_width_parser.py when the container launches
CMD ["python", "fixed_width_parser.py", "spec.txt", "data.txt", "output.csv", "valid_output.txt", "errors.txt", "summary.csv", "--output-format", "csv", "--summary-format", "csv", "generated_fixed_width.txt"]