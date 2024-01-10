import dns.resolver
import subprocess
import re
from utils import run_command, colored

VALID_RECORD_TYPES = ["A", "AAAA", "CNAME", "MX", "NS", "PTR", "SOA", "SRV", "TXT", "CAA", "DNSKEY", "DS", "NAPTR", "RRSIG", "SPF", "TLSA", "URI"]

def is_root_domain(target):
    # Implement logic to check if the target is a root domain
    return target.count('.') <= 1

def is_soa_only_output(relevant_lines, record_type):
    if not relevant_lines or record_type in ["PTR", "SRV", "DNSKEY", "DS", "NAPTR", "RRSIG", "SPF", "TLSA", "URI"]:
        return True
    return all(' IN SOA ' in line for line in relevant_lines) and record_type != "SOA"

def dns_queries(target, nameserver="", record_types=None):
    if not nameserver:
        default_ns = dns.resolver.get_default_resolver().nameservers[0]
        nameserver = default_ns
        print(colored(f"Using default nameserver: {nameserver}", "cyan"))

    # Check for 'all' keyword in record_types
    if record_types is None:
        record_types = ['A']
    elif 'all' in record_types:
        record_types = VALID_RECORD_TYPES
    else:
        record_types = [rt for rt in record_types if rt in VALID_RECORD_TYPES]
        if not record_types:
            print(colored("Error: No valid DNS record types provided.", "red"))
            return []

    ns_arg = f" @{nameserver}" if nameserver else ""

    results = []
    for record_type in record_types:
        try:
            cmd = f"dig {record_type} {target}{ns_arg}"
            output = run_command(cmd)

            lines = output.split('\n')
            relevant_lines = [line for line in lines if line and not line.startswith(';') and not line.startswith(';;')]

            if is_soa_only_output(relevant_lines, record_type):
                result_block = (
                    colored(f"\nRecord Type: {record_type}", "header") + "\n" +
                    colored(f"No {record_type} records found, or the record type is not applicable for this domain.", "warning")
                )
            else:
                processed_output = '\n'.join(relevant_lines)
                result_block = (
                    colored(f"\nRecord Type: {record_type}", "header") + "\n" +
                    colored("Command:", "blue") + f"\n{cmd}\n" +
                    colored("Processed Output:", "cyan") + "\n" + processed_output +
                    "\n" + "-"*40  # Separator line
                )
            results.append(result_block)

        except Exception as e:
            results.append(colored(f"Error while querying {record_type} records for {target}: {str(e)}", "red"))

    return results
