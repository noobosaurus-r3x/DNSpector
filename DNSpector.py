import argparse
import dns.query
import dns.zone
import dns.resolver
from dns_module import dns_queries
from whois_module import get_whois_data
from subdomain_module import fetch_all_subdomains
from utils import colored

def perform_axfr_query(domain, nameserver):
    try:
        zone_transfer = dns.query.xfr(nameserver, domain, lifetime=10)
        zone = dns.zone.from_xfr(zone_transfer)
        records = [zone[n].to_text(n) for n in zone.nodes.keys()]
        return True, "\n".join(records)
    except Exception as e:
        return False, str(e)

def main():
    banner = '''

    ____  _   _______                 __            
   / __ \/ | / / ___/____  ___  _____/ /_____  _____
  / / / /  |/ /\__ \/ __ \/ _ \/ ___/ __/ __ \/ ___/
 / /_/ / /|  /___/ / /_/ /  __/ /__/ /_/ /_/ / /    
/_____/_/ |_//____/ .___/\___/\___/\__/\____/_/     
                 /_/                                
'''
    print(banner)
    print("DNSpector - DNS Enumeration and Analysis Tool")

    parser = argparse.ArgumentParser(description="DNS Enumeration and Analysis Tool")
    parser.add_argument("target", help="Target domain")
    parser.add_argument("-n", "--nameserver", help="Nameserver/IP to use", default="")
    parser.add_argument("-r", "--records", nargs="*", help="Specific DNS record types to query", default=None)
    parser.add_argument("-w", "--whois", help="Perform a WHOIS lookup", action="store_true")
    parser.add_argument("-sd", "--subdomain", help="Perform passive subdomain enumeration", action="store_true")
    parser.add_argument("-zt", "--zone-transfer", help="Perform a Zone Transfer Check", action="store_true")

    args = parser.parse_args()

    try:
        if args.target:
            if args.whois:
                print(get_whois_data(args.target))

            # Regular DNS Queries
            if args.records:
                if 'all' in args.records and 'axfr' in args.records:
                    args.records.remove('axfr')
                dns_results = dns_queries(args.target, args.nameserver, args.records)
                for result in dns_results:
                    print(result)

            # Subdomain Enumeration
            if args.subdomain:
                subdomains = fetch_all_subdomains(args.target)
                for subdomain in subdomains:
                    print(subdomain)

            # Zone Transfer Check
            if args.zone_transfer:
                success, axfr_result = perform_axfr_query(args.target, args.nameserver)
                if success:
                    print(colored("\nZone Transfer Results:", "header"))
                    print(axfr_result)
                else:
                    print(colored(f"\nZone Transfer Failed: {axfr_result}", "fail"))

    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting DNSpector...")

if __name__ == "__main__":
    main()