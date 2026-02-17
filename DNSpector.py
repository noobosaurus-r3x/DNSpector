import argparse
import dns.query
import dns.zone
import dns.resolver
from dns_module import dns_queries
from whois_module import get_whois_data
from subdomain_module import fetch_all_subdomains
from utils import colored
from constants import __version__, RECORD_DESCRIPTIONS

def perform_axfr_query(domain, nameserver, timeout=10):
    try:
        zone_transfer = dns.query.xfr(nameserver, domain, lifetime=timeout)
        zone = dns.zone.from_xfr(zone_transfer)
        records = [zone[n].to_text(n) for n in zone.nodes.keys()]
        return True, "\n".join(records)
    except Exception as e:
        return False, str(e)

def main():
    banner = r'''

    ____  _   _______                 __            
   / __ \/ | / / ___/____  ___  _____/ /_____  _____
  / / / /  |/ /\__ \/ __ \/ _ \/ ___/ __/ __ \/ ___/
 / /_/ / /|  /___/ / /_/ /  __/ /__/ /_/ /_/ / /    
/_____/_/ |_//____/ .___/\___/\___/\__/\____/_/     
                 /_/                                
'''
    # Build epilog with record type descriptions
    record_help = "\nSupported DNS record types:\n"
    for record_type, description in sorted(RECORD_DESCRIPTIONS.items()):
        record_help += f"  {record_type:10} - {description}\n"
    
    epilog = record_help + "\nExamples:\n"
    epilog += "  python DNSpector.py example.com -r A AAAA MX\n"
    epilog += "  python DNSpector.py example.com -r all --whois\n"
    epilog += "  python DNSpector.py example.com --subdomain\n"
    epilog += "  python DNSpector.py example.com -n 8.8.8.8 --zone-transfer\n"

    parser = argparse.ArgumentParser(
        description="DNS Enumeration and Analysis Tool for Security Research",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("target", help="Target domain to analyze")
    parser.add_argument("-n", "--nameserver", help="Nameserver/IP to use for queries (default: system resolver)", default="", metavar="NS")
    parser.add_argument("-r", "--records", nargs="*", help="DNS record types to query (use 'all' for all types)", default=None, metavar="TYPE")
    parser.add_argument("-w", "--whois", help="Perform WHOIS domain registration lookup", action="store_true")
    parser.add_argument("-sd", "--subdomain", help="Perform passive subdomain enumeration from public sources", action="store_true")
    parser.add_argument("-zt", "--zone-transfer", help="Test for misconfigured zone transfer (AXFR)", action="store_true")
    parser.add_argument("-q", "--quiet", help="Suppress banner and non-essential output", action="store_true")
    parser.add_argument("-t", "--timeout", type=float, default=5.0, help="Query timeout in seconds (default: 5.0)", metavar="SEC")
    parser.add_argument("--version", action="version", version=f"DNSpector {__version__}")

    args = parser.parse_args()

    # Display banner unless --quiet
    if not args.quiet:
        print(banner)
        print(f"DNSpector v{__version__} - DNS Enumeration and Analysis Tool")
        print()

    try:
        if args.target:
            if args.whois:
                print(get_whois_data(args.target))

            # Regular DNS Queries
            if args.records:
                if 'all' in args.records and 'axfr' in args.records:
                    args.records.remove('axfr')
                dns_results = dns_queries(args.target, args.nameserver, args.records, args.timeout)
                for result in dns_results:
                    print(result)

            # Subdomain Enumeration
            if args.subdomain:
                subdomains = fetch_all_subdomains(args.target)
                for subdomain in subdomains:
                    print(subdomain)

            # Zone Transfer Check
            if args.zone_transfer:
                success, axfr_result = perform_axfr_query(args.target, args.nameserver, args.timeout)
                if success:
                    print(colored("\nZone Transfer Results:", "header"))
                    print(axfr_result)
                else:
                    print(colored(f"\nZone Transfer Failed: {axfr_result}", "fail"))

    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting DNSpector...")

if __name__ == "__main__":
    main()
