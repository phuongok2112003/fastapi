import re

def extract_public_id(url):
    # Biểu thức regex để tìm public_id
    match = re.search(r'/v\d+/(.+)\.', url)
    if match:
        return match.group(1)
    return None