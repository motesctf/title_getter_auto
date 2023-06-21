import time
from urllib.parse import urlparse, urlunparse


def check_http(url: str):
    if url.split(':')[0] in ['http', 'https']:
        return url
    return "http://" + url


def check_http_alternative(url: str):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        parsed_url = parsed_url._replace(scheme='http')
        return urlunparse(parsed_url)
    return url


with open("../data/domains_for_test_check_http.txt", 'r') as file:
    domains = [line.strip() for line in file]

    start_time = time.time()
    for domain in domains:
        check_http(domain)
    original_time = time.time() - start_time

    start_alt_time = time.time()
    for domain in domains:
        check_http_alternative(domain)
    alternative_time = time.time() - start_alt_time

print(f"Original function execution time: {original_time:.6f} seconds")
print(f"Alternative function execution time: {alternative_time:.6f} seconds")

# check_http = 0.005257 seconds
# check_http_alternative = 0.082233 seconds



