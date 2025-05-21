# core/crash_analyzer.py
from core.log_parser import read_kernel_log

crash_keywords: dict[list] = {
    "kernel": [
        "kernel panic", "BUG:", "Oops", "segfault", "general protection fault",
        "invalid opcode", "fatal exception", "stack overflow", "stack trace",
        "Call Trace:", "RIP:", "RSP:", "RAX:", "RDX:", "EIP:", "ESP:",
        "unable to handle kernel paging request", "bad page state",
        "page allocation failure", "slab error", "corrupted memory",
        "kernel BUG at", "soft lockup", "hard lockup", "watchdog: BUG:"
    ],
    "filesystem": [
        "I/O error", "ext4-fs error", "xfs: internal error", "filesystem corruption",
        "journal commit I/O error", "buffer I/O error", "Failed to mount",
        "mount error", "blk_update_request: I/O error", "nfs: server not responding",
        "FAT-fs (.*): warning", "jbd2: transaction commit failure"
    ],
    "modules": [
        "Failed to load module", "module verification failed", "tainted kernel",
        "unknown symbol in module", "module load failure", "firmware: failed to load",
        "modprobe:", "rmmod:"
    ],
    "hardware": [
        "thermal shutdown", "overheating", "voltage fault", "ACPI BIOS Error",
        "ECC memory error", "hardware error", "Machine Check Exception",
        "CPU stuck", "watchdog timeout", "fan failure", "power supply error",
        "dmi: Firmware bug", "PCIe Bus Error", "I/O APIC", "DMA failure"
    ],
    "security": [
        "Spectre", "Meltdown", "stack smashing detected", "kernel tainted",
        "attempt to access restricted", "audit: avc: denied", "SELinux: denied",
        'apparmor="DENIED"', "seccomp:", "LSM:", "securityfs:"
    ],
    "warnings": [
        "WARNING: CPU:", "rcu_sched detected stall", "rcu: INFO:", "hung task",
        "soft lockup - CPU", "unable to enumerate USB device", "usb reset failure",
        "net_ratelimit", "link down", "transmit queue timed out",
        "eth0: NIC Link is Down", "drm:", "firmware bug"
    ],
    "network": [
        "netdev watchdog:", "eth0: transmit timed out", "TCP: ", "UDP: ",
        "netlink: ", "bridge: ", "bonding: ", "NIC Link is Down", "packet loss"
    ],
    "power": [
        "ACPI: ", "PM: ", "Power state:", "Battery: ", "thermal zone", "CPU frequency",
        "CPU idle", "Suspend:", "Resume:", "PM: suspend entry", "PM: resume entry"
    ]
}

lower_crash_keywords = {
    cat: [kw.lower() for kw in kws]
    for cat, kws in crash_keywords.items()
}

def detect_crashes(log_lines=None, verbose=False):
    if log_lines is None:
        log_lines = read_kernel_log()

    crash_data = []

    for line in log_lines:
        line_l = line.lower()
        for category, keywords in lower_crash_keywords.items():
            matched_keywords = [kw for kw in keywords if kw in line_l]
            if matched_keywords:
                entry = {
                    "category": category,
                    "message": line.strip(),
                    "matched": matched_keywords
                }
                crash_data.append(entry)
                if verbose:
                    print(f"[{category.upper()}] {line.strip()}")
                break  

    return crash_data
