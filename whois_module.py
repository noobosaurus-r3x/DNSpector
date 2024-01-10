import whois
from utils import colored

def get_whois_data(domain):
    """ Perform a WHOIS lookup and format the output for readability, handling None values """
    try:
        w = whois.whois(domain)

        def format_field(field):
            return field if field is not None else "Not Available"

        formatted_data = colored("WHOIS Data:", "header") + "\n"
        formatted_data += colored("Domain Name:", "blue") + f" {format_field(w.domain_name)}\n"
        formatted_data += colored("Registrar:", "blue") + f" {format_field(w.registrar)}\n"
        formatted_data += colored("Updated Date:", "blue") + f" {format_field(w.updated_date)}\n"
        formatted_data += colored("Creation Date:", "blue") + f" {format_field(w.creation_date)}\n"
        formatted_data += colored("Expiration Date:", "blue") + f" {format_field(w.expiration_date)}\n"
        formatted_data += colored("Name Servers:", "blue") + "\n - " + "\n - ".join(format_field(w.name_servers)) + "\n"
        formatted_data += colored("Status:", "blue") + "\n - " + "\n - ".join(format_field(w.status)) + "\n"
        formatted_data += colored("Emails:", "blue") + "\n - " + "\n - ".join(format_field(w.emails)) + "\n"
        formatted_data += colored("DNSSEC:", "blue") + f" {format_field(w.dnssec)}\n"
        formatted_data += colored("Registrant Info:", "blue") + "\n"
        formatted_data += "  Name: " + format_field(w.name) + "\n"
        formatted_data += "  Organization: " + format_field(w.org) + "\n"
        formatted_data += "  Address: " + format_field(w.address) + "\n"
        formatted_data += "  City: " + format_field(w.city) + "\n"
        formatted_data += "  State: " + format_field(w.state) + "\n"
        formatted_data += "  Postal Code: " + format_field(w.registrant_postal_code) + "\n"
        formatted_data += "  Country: " + format_field(w.country) + "\n"

        return formatted_data
    except Exception as e:
        return colored(f"WHOIS lookup failed: {e}", "fail")