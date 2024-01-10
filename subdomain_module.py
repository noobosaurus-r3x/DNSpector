import requests
import re
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

def fetch_subdomains(url, domain):
    """ Fetches subdomains from a given URL and returns them as a set """
    try:
        response = requests.get(url)
        response.raise_for_status()
        pattern = re.compile(rf'((?:[a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9])\.{domain})')
        return set(pattern.findall(response.text))
    except requests.exceptions.RequestException:
        return set()

def fetch_all_subdomains(domain):
    """ Fetches subdomains from all URLs concurrently and returns them as a set """
    urls = [
        f'https://rapiddns.io/subdomain/{domain}?full=1#result',
        f'http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=text&fl=original&collapse=urlkey',
        f'https://crt.sh/?q=%.{domain}',
        f'https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns',
        f'https://urlscan.io/api/v1/search/?q=domain:{domain}',
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_subdomains, url, domain) for url in urls]
        subdomains = set()
        for future in concurrent.futures.as_completed(futures):
            subdomains |= future.result()

    return subdomains