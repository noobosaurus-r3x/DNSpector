import subprocess
from subprocess import TimeoutExpired
from constants import COLORS

def colored(text, color):
    """ Apply ANSI color code to text """
    return f"{COLORS[color]}{text}{COLORS['end']}"

def run_command(command, timeout=10):  # Add a timeout parameter
    """ Run a shell command and return its output """
    try:
        return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=timeout).decode()
    except subprocess.CalledProcessError as e:
        return colored(f"Error executing command: {command}\n{e.output.decode()}", "fail")
    except TimeoutExpired:
        return colored(f"Timeout expired for command: {command}", "warning")