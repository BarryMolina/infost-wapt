import sys
import requests
import time
import sys
import re
import argparse

def parse_raw_http_request(raw_request):
    # Split the raw request by line breaks
    lines = raw_request.splitlines()

    # Step 1: Parse the request line
    request_line = lines[0].split()
    method = request_line[0]  # e.g., "POST"
    url_path = request_line[1]  # e.g., "/wapt/module4/mi6/extra-credit.php"

    # Step 2: Parse the headers
    headers = {}
    body = None
    i = 1
    while i < len(lines):
        line = lines[i]
        if line == '':  # Empty line indicates the end of headers
            # Step 3: The rest is the body
            body = '\n'.join(lines[i + 1:])
            break
        header_name, header_value = line.split(":", 1)
        headers[header_name.strip()] = header_value.strip()
        i += 1

    # Step 4: Extract the host and construct the full URL
    host = headers.get("Host", "")
    full_url = f"https://{host}{url_path}"

    # Step 5: Return the method, URL, headers, and body
    return method, full_url, headers, body

def send_parsed_request(method, url, headers, body):
    import requests

    # Send the parsed request using the requests library
    if method == "POST":
        response = requests.post(url, headers=headers, data=body)
    elif method == "GET":
        response = requests.get(url, headers=headers)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    return response



def read_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: The file {filename} was not found."
    except Exception as e:
        return f"Error: An error occurred while reading {filename}. Details: {str(e)}"


def interpolate_payload(request_template, payload):
    # Use regex to replace everything between two § symbols with the payload
    return re.sub(r'§.*?§', payload, request_template)

def sniper(template_file, payload_file, out_file):
    template = read_file(template_file)

    with open(payload_file) as f, open(out_file, 'w', buffering=1) as out:
        out.write('payload|status_code|content_length\n')
        for line in f:
            line = line.rstrip()
            if not line.startswith('#'):
                raw_req = interpolate_payload(template, line)
                method, url, headers, body = parse_raw_http_request(raw_req)
                r = send_parsed_request(method, url, headers, body)
                out.write(f"{line}|{r.status_code}|{r.headers['content-length']}\n")
                out.flush()

def main():
        # Set up argument parser
    parser = argparse.ArgumentParser(description='Process a templated request with payloads and submit each one.')
    
    # Add optional arguments with default values
    parser.add_argument('-o', '--outfile', default='out.txt', help='Output file (default: out.txt)')
    parser.add_argument('-t', '--template', default='template.txt', help='Template file (default: template.txt)')
    parser.add_argument('-p', '--payload', default='payload.txt', help='Payload file (default: payload.txt)')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Assign parsed arguments to variables
    template_file = args.template
    payload_file = args.payload
    out_file = args.outfile

    # Run the sniper function with the specified arguments
    sniper(template_file, payload_file, out_file)


if __name__ == "__main__":
    main()
