import subprocess
import re
from subprocess import TimeoutExpired
from constants import COLORS

# Domain validation: letters, digits, hyphens, dots only
DOMAIN_PATTERN = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$')

# IP validation: simple pattern for IPv4 and basic IPv6
IPV4_PATTERN = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
IPV6_PATTERN = re.compile(r'^[0-9a-fA-F:]+$')


def colored(text, color):
    """ Apply ANSI color code to text """
    return f"{COLORS[color]}{text}{COLORS['end']}"


def validate_domain(domain):
    """Validate domain name to prevent injection attacks."""
    if not domain or len(domain) > 253:
        return False
    return bool(DOMAIN_PATTERN.match(domain))


def validate_nameserver(ns):
    """Validate nameserver (domain or IP address)."""
    if not ns:
        return True  # Empty is OK (use default)
    # Accept valid IPs
    if IPV4_PATTERN.match(ns):
        parts = ns.split('.')
        return all(0 <= int(p) <= 255 for p in parts)
    if IPV6_PATTERN.match(ns) and ':' in ns:
        return True
    # Accept valid domains
    return validate_domain(ns)


def run_command(command, timeout=10):
    """Run a command safely. Accepts a list of arguments (no shell=True)."""
    if isinstance(command, str):
        # Legacy support: split string into args (but prefer passing lists)
        import shlex
        command = shlex.split(command)
    try:
        return subprocess.check_output(command, shell=False, stderr=subprocess.STDOUT, timeout=timeout).decode()
    except subprocess.CalledProcessError as e:
        cmd_str = ' '.join(command)
        return colored(f"Error executing command: {cmd_str}\n{e.output.decode()}", "fail")
    except TimeoutExpired:
        cmd_str = ' '.join(command)
        return colored(f"Timeout expired for command: {cmd_str}", "warning")