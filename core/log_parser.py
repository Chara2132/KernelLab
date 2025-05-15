import subprocess as sub


def read_kernel_log():
    try:
        return sub.check_output(["dmesg"],text=True).splitlines()
    except sub.CalledProcessError:
        try:
            return sub.check_output(["journalctl","-k","--no-pager"],text=True).splitlines()
        except sub.CalledProcessError as e:
            print("[red] Impossible to read kernel log, try with root")
            return []

