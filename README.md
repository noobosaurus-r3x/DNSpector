# DNSpector: DNS Enumeration and Analysis Tool

Work In Progress, but the tool is working.

## Description

DNSpector is a DNS enumeration and analysis tool tailored for cybersecurity practitioners. It streamlines and automates the usage of established tools such as `dig` and `whois`, adding enhanced readability and a user-friendly interface. This tool doesn't reinvent the wheel but rather smartly combines existing utilities with additional automation for a more efficient workflow.

**This tool is a testament to the power of simplicity. It does not reinvent the wheel but instead, harnesses the capabilities of existing tools, presenting their output in a more user-friendly manner. It's tailored for those who appreciate efficiency and clarity in their cybersecurity investigations.**
## Features

- Integrated DNS Tools: Leverages dig for DNS record queries and whois for domain information.
  
- Automated Analysis: Simplifies and automates the analysis of complex DNS data.
  
- Color-Coded Output: Outputs are enhanced with ANSI color codes for easy reading and analysis.
  
- Subdomain Enumeration & Zone Transfer Checks: Includes features for passive subdomain enumeration and testing for zone transfer vulnerabilities.

## Installation

1- Clone the repo
```bash
https://github.com/noobosaurus-r3x/DNSpector
```

2- Install dependencies 
```bash
pip install -r requirements.txt
```

## Usage

Basic Syntax :

```bash
python3 DNSpector.py [target] [options]
```

Help :

```bash
python3 DNSpector.py -h
```

Querying DNS records (A and MX) :

```bash
python3 DNSpector.py example.com -r A MX
```

Querying all DNS records :

```bash
python3 DNSpector.py example.com -r all
```

Querying everything :

```bash
python3 DNSpectre.py example.com -n [IP/Nameserver] -w -r all -zt -sd 
```

**Options :**

`-n, --nameserver` : Specify a nameserver/IP.

`-r, --records` : Select DNS record types to query.

List of records' types : "A", "AAAA", "CNAME", "MX", "NS", "PTR", "SOA", "SRV", "TXT", "CAA", "DNSKEY", "DS", "NAPTR", "RRSIG", "SPF", "TLSA", "URI"

`-w, --whois` : Perform a WHOIS lookup.

`-sd, --subdomain` : Enable passive subdomain enumeration. That might take a while, don't worry.

`-zt, --zone-transfer` : Check for Zone Transfer vulnerabilities.

## Requirements

Python 3.x

Dependencies as listed in requirements.txt

## Limitations

Relies on third-party services and tools, which may have limitations or access restrictions.

Effectiveness is dependent on the target domain's configuration and the availability of data from external sources.

My skills in dev.

## Acknowledgements :

Special thanks to all the open-source tools and their contributors that made DNSpector possible. 

This project stands on the shoulders of these giants in the spirit of collaboration and open knowledge.

ChatGPT was used during the process.

