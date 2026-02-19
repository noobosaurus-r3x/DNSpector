import dns.resolver
import dns.exception
import re
from utils import colored, validate_domain, validate_nameserver

VALID_RECORD_TYPES = ["A", "AAAA", "CNAME", "MX", "NS", "PTR", "SOA", "SRV", "TXT", "CAA", "DNSKEY", "DS", "NAPTR", "RRSIG", "SPF", "TLSA", "URI"]

def is_root_domain(target):
    # Implement logic to check if the target is a root domain
    return target.count('.') <= 1

def dns_queries(target, nameserver="", record_types=None, timeout=5.0):
    """
    Query DNS records for a target domain using dnspython.
    
    Args:
        target: Domain name to query
        nameserver: DNS server to use (optional, uses default if not specified)
        record_types: List of record types or 'all' (default: ['A'])
        timeout: Query timeout in seconds (default: 5.0)
    
    Returns:
        List of formatted result strings
    """
    # Validate inputs to prevent injection
    if not validate_domain(target):
        print(colored(f"Error: Invalid domain name: {target}", "red"))
        return []

    if nameserver and not validate_nameserver(nameserver):
        print(colored(f"Error: Invalid nameserver: {nameserver}", "red"))
        return []

    # Configure resolver
    resolver = dns.resolver.Resolver()
    resolver.timeout = timeout
    resolver.lifetime = timeout
    if nameserver:
        resolver.nameservers = [nameserver]
        print(colored(f"Using nameserver: {nameserver}", "cyan"))
    else:
        default_ns = resolver.nameservers[0]
        print(colored(f"Using default nameserver: {default_ns}", "cyan"))

    # Normalize record_types to upper case
    if record_types is None:
        record_types = ['A']  # Default to 'A' if no record types are specified
    elif 'all' in record_types:
        record_types = VALID_RECORD_TYPES
    else:
        # Normalize to upper case for case-insensitive comparison
        record_types = [rt.upper() for rt in record_types if rt.upper() in VALID_RECORD_TYPES]

    if not record_types:
        print(colored("Error: No valid DNS record types provided.", "red"))
        return []

    results = []
    for record_type in record_types:
        try:
            # Query using dnspython
            answers = resolver.resolve(target, record_type)
            
            # Format output similar to dig
            output_lines = []
            for answer in answers:
                # Format based on record type for readability
                if record_type in ['A', 'AAAA']:
                    output_lines.append(f"{target}.\t\tIN\t{record_type}\t{answer.address}")
                elif record_type == 'MX':
                    output_lines.append(f"{target}.\t\tIN\tMX\t{answer.preference} {answer.exchange}.")
                elif record_type == 'NS':
                    output_lines.append(f"{target}.\t\tIN\tNS\t{answer.target}.")
                elif record_type == 'CNAME':
                    output_lines.append(f"{target}.\t\tIN\tCNAME\t{answer.target}.")
                elif record_type == 'SOA':
                    output_lines.append(f"{target}.\t\tIN\tSOA\t{answer.mname}. {answer.rname}. {answer.serial} {answer.refresh} {answer.retry} {answer.expire} {answer.minimum}")
                elif record_type == 'TXT':
                    # TXT records can have multiple strings
                    txt_value = ' '.join([s.decode() if isinstance(s, bytes) else str(s) for s in answer.strings])
                    output_lines.append(f"{target}.\t\tIN\tTXT\t\"{txt_value}\"")
                elif record_type == 'SRV':
                    output_lines.append(f"{target}.\t\tIN\tSRV\t{answer.priority} {answer.weight} {answer.port} {answer.target}.")
                else:
                    # Generic formatting for other record types
                    output_lines.append(f"{target}.\t\tIN\t{record_type}\t{str(answer)}")
            
            processed_output = '\n'.join(output_lines)
            result_block = (
                colored(f"\nRecord Type: {record_type}", "header") + "\n" +
                colored("Processed Output:", "cyan") + "\n" + processed_output +
                "\n" + "-"*40  # Separator line
            )
            results.append(result_block)

        except dns.resolver.NXDOMAIN:
            message = f"Domain {target} does not exist (NXDOMAIN)."
            result_block = (
                colored(f"\nRecord Type: {record_type}", "header") + "\n" +
                colored(message, "warning")
            )
            results.append(result_block)
        
        except dns.resolver.NoAnswer:
            message = f"Query successful but no {record_type} records found for {target}."
            result_block = (
                colored(f"\nRecord Type: {record_type}", "header") + "\n" +
                colored(message, "warning")
            )
            results.append(result_block)
        
        except dns.resolver.NoNameservers:
            message = f"No nameservers available to answer query for {target}."
            result_block = (
                colored(f"\nRecord Type: {record_type}", "header") + "\n" +
                colored(message, "red")
            )
            results.append(result_block)
        
        except dns.exception.Timeout:
            message = f"Query timeout while looking up {record_type} records for {target}."
            result_block = (
                colored(f"\nRecord Type: {record_type}", "header") + "\n" +
                colored(message, "red")
            )
            results.append(result_block)
        
        except Exception as e:
            results.append(colored(f"Error while querying {record_type} records for {target}: {str(e)}", "red"))

    return results
