import requests
import re
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from utils import colored

def fetch_subdomains(url, domain, source_name):
    """ 
    Fetches subdomains from a given URL and returns them as a set.
    
    Args:
        url: URL to fetch subdomains from
        domain: Target domain
        source_name: Human-readable name of the source (for progress display)
    
    Returns:
        Set of discovered subdomains
    """
    try:
        print(colored(f"  [*] Querying {source_name}...", "cyan"))
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        pattern = re.compile(rf'((?:[a-zA-Z0-9_]|[a-zA-Z0-9_][a-zA-Z0-9_-]*[a-zA-Z0-9_])\.{re.escape(domain)})')
        subdomains = set(pattern.findall(response.text))
        if subdomains:
            print(colored(f"  [✓] {source_name}: Found {len(subdomains)} subdomain(s)", "green"))
        else:
            print(colored(f"  [✓] {source_name}: No subdomains found", "yellow"))
        return subdomains
    except requests.exceptions.Timeout:
        print(colored(f"  [!] {source_name}: Timeout", "red"))
        return set()
    except requests.exceptions.RequestException as e:
        print(colored(f"  [!] {source_name}: Error ({type(e).__name__})", "red"))
        return set()

def fetch_all_subdomains(domain):
    """ 
    Fetches subdomains from all sources concurrently and returns them as a set.
    Progress indicators show which sources are being queried and results in real-time.
    
    Args:
        domain: Target domain to enumerate subdomains for
    
    Returns:
        Set of all discovered subdomains
    """
    print(colored(f"\n[*] Starting subdomain enumeration for {domain}", "header"))
    print(colored("[*] Querying 5 external sources...\n", "cyan"))
    
    sources = [
        ("RapidDNS", f'https://rapiddns.io/subdomain/{domain}?full=1#result'),
        ("Web Archive", f'http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=text&fl=original&collapse=urlkey'),
        ("crt.sh", f'https://crt.sh/?q=%.{domain}'),
        ("AlienVault OTX", f'https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns'),
        ("URLScan.io", f'https://urlscan.io/api/v1/search/?q=domain:{domain}'),
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_subdomains, url, domain, name): name for name, url in sources}
        subdomains = set()
        completed = 0
        total = len(futures)
        
        for future in concurrent.futures.as_completed(futures):
            completed += 1
            subdomains |= future.result()
            print(colored(f"  [{completed}/{total}] Sources queried, {len(subdomains)} unique subdomains found so far", "blue"))
    
    print(colored(f"\n[✓] Enumeration complete: {len(subdomains)} unique subdomain(s) discovered\n", "green"))
    return subdomains
