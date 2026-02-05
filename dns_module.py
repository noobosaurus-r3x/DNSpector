import dns.resolver
import subprocess
import re
from utils import run_command, colored, validate_domain, validate_nameserver

VALID_RECORD_TYPES = ["A", "AAAA", "CNAME", "MX", "NS", "PTR", "SOA", "SRV", "TXT", "CAA", "DNSKEY", "DS", "NAPTR", "RRSIG", "SPF", "TLSA", "URI"]

def is_root_domain(target):
    # Implement logic to check if the target is a root domain
    return target.count('.') <= 1

def is_soa_only_output(relevant_lines, record_type):
    if not relevant_lines or record_type in ["PTR", "SRV", "DNSKEY", "DS", "NAPTR", "RRSIG", "SPF", "TLSA", "URI"]:
        return True
    return all(' IN SOA ' in line for line in relevant_lines) and record_type != "SOA"

def dns_queries(target, nameserver="", record_types=None):
    # Validate inputs to prevent injection
    if not validate_domain(target):
        print(colored(f"Error: Invalid domain name: {target}", "red"))
        return []

    if nameserver and not validate_nameserver(nameserver):
        print(colored(f"Error: Invalid nameserver: {nameserver}", "red"))
        return []

    if not nameserver:
        default_ns = dns.resolver.get_default_resolver().nameservers[0]
        nameserver = default_ns
        print(colored(f"Using default nameserver: {nameserver}", "cyan"))

    # Normalize record_types to upper case right after determining what they are
    if record_types is None:
        record_types = ['A']  # Default to 'A' if no record types are specified
    elif 'all' in record_types:
        record_types = VALID_RECORD_TYPES  # Assuming VALID_RECORD_TYPES are all in upper case
    else:
        # Normalize to upper case for case-insensitive comparison
        record_types = [rt.upper() for rt in record_types if rt.upper() in VALID_RECORD_TYPES]

    if not record_types:
        print(colored("Error: No valid DNS record types provided.", "red"))
        return []

    results = []
    for record_type in record_types:
        try:
            # Build command as list to avoid shell injection
            cmd_list = ["dig", record_type, target]
            if nameserver:
                cmd_list.append(f"@{nameserver}")
            cmd_display = ' '.join(cmd_list)
            output = run_command(cmd_list)

            lines = output.split('\n')
            relevant_lines = [line for line in lines if line and not line.startswith(';') and not line.startswith(';;')]

            if is_soa_only_output(relevant_lines, record_type):
                message = f"Query successful but no {record_type} records found for {target}."
                result_block = (
                    colored(f"\nRecord Type: {record_type}", "header") + "\n" +
                    colored("Command:", "blue") + f"\n{cmd_display}\n" +
                    colored(message, "warning")
                )
            else:
                processed_output = '\n'.join(relevant_lines)
                result_block = (
                    colored(f"\nRecord Type: {record_type}", "header") + "\n" +
                    colored("Command:", "blue") + f"\n{cmd_display}\n" +
                    colored("Processed Output:", "cyan") + "\n" + processed_output +
                    "\n" + "-"*40  # Separator line
                )
            results.append(result_block)

        except Exception as e:
            results.append(colored(f"Error while querying {record_type} records for {target}: {str(e)}", "red"))

    return results

