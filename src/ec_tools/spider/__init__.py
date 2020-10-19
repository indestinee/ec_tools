def get_headers(path):
    headers = {}
    with open(path) as f:
        for row in f.readlines():
            row = row.strip()
            index = row.find(":")
            headers[row[:index]] = row[index + 1:].strip()
    return headers
