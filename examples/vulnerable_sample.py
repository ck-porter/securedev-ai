import subprocess

def get_user_report(filename):
    # Intentionally vulnerable example for scanner testing.
    command = "type " + filename
    return subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )