# DNSpector version
__version__ = "1.2.0"

# ANSI color codes for colored output
COLORS = {
    "header": "\033[95m",
    "red": "\033[91m",
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "green": "\033[92m",
    "warning": "\033[93m",
    "yellow": "\033[93m",
    "fail": "\033[91m",
    "end": "\033[0m",
    "bold": "\033[1m",
    "white": "\033[97m",
    "magenta": "\033[95m",
    "underline": "\033[4m"
}

# DNS record type descriptions for help text
RECORD_DESCRIPTIONS = {
    "A": "IPv4 address",
    "AAAA": "IPv6 address",
    "CNAME": "Canonical name (alias)",
    "MX": "Mail exchange servers",
    "NS": "Name servers",
    "PTR": "Pointer (reverse DNS)",
    "SOA": "Start of authority",
    "SRV": "Service locator",
    "TXT": "Text records",
    "CAA": "Certificate authority authorization",
    "DNSKEY": "DNSSEC public key",
    "DS": "Delegation signer",
    "NAPTR": "Naming authority pointer",
    "RRSIG": "DNSSEC signature",
    "SPF": "Sender policy framework",
    "TLSA": "TLS authentication",
    "URI": "Uniform resource identifier"
}