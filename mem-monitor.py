#!/usr/bin/env python3
"""
m2 memory pressure monitor.
Runs every 30s. Logs warnings, kills ComfyUI at critical, updates /tmp/mem-status.json.
"""
import subprocess, re, os, signal, json, datetime, time, sys
from pathlib import Path

LOG_PATH    = Path("/tmp/mem-monitor.log")
STATUS_PATH = Path("/tmp/mem-status.json")
ALERT_PATH  = Path("/tmp/mem-alerts.log")

# Thresholds (usable = free + inactive; inactive pages are reclaimable)
WARN_GB   = 4.0   # log a warning
ALERT_GB  = 2.0   # log an alert + notify cheat-sheet
CRIT_GB   = 0.8   # kill ComfyUI + any other kill targets

# Processes to SIGTERM at critical level, in order
KILL_TARGETS = [
    ("ComfyUI",   ["pgrep", "-f", "ComfyUI"]),
    ("comfyui",   ["pgrep", "-fi", "comfy"]),
    ("Flux",      ["pgrep", "-f", "flux"]),
]

PAGE_SIZE = 16384  # bytes, Apple Silicon M-series

def ts():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(msg, also_alert=False):
    line = f"[{ts()}] {msg}\n"
    with open(LOG_PATH, "a") as f:
        f.write(line)
    if also_alert:
        with open(ALERT_PATH, "a") as f:
            f.write(line)
    print(line, end="", flush=True)

def vm_stat():
    out = subprocess.check_output(["vm_stat"], text=True)
    p = {}
    for line in out.splitlines():
        m = re.match(r"(.+?):\s+([\d]+)\.", line)
        if m:
            p[m.group(1).strip()] = int(m.group(2))
    def gb(key): return p.get(key, 0) * PAGE_SIZE / 1e9
    return {
        "free":       gb("Pages free"),
        "spec":       gb("Pages speculative"),
        "inactive":   gb("Pages inactive"),
        "active":     gb("Pages active"),
        "wired":      gb("Pages wired down"),
        "compressed": gb("Pages occupied by compressor"),
        "decomp":     gb("Decompressions") if "Decompressions" in p else 0,
    }

def top_procs_by_mem(n=8):
    try:
        raw = subprocess.check_output(
            ["ps", "-eo", "pid,rss,comm", "-m"],
            text=True
        ).splitlines()[1:]
        procs = []
        for line in raw:
            parts = line.split(None, 2)
            if len(parts) == 3:
                try:
                    procs.append({"pid": int(parts[0]),
                                  "mb": int(parts[1]) / 1024,
                                  "name": parts[2].strip().split("/")[-1][:40]})
                except ValueError:
                    pass
        return sorted(procs, key=lambda x: x["mb"], reverse=True)[:n]
    except Exception as e:
        return []

def kill_targets():
    killed = []
    for name, cmd in KILL_TARGETS:
        try:
            pids = subprocess.check_output(cmd, text=True).strip().split()
            for pid in pids:
                os.kill(int(pid), signal.SIGTERM)
                log(f"KILLED {name} pid={pid}", also_alert=True)
                killed.append(f"{name}:{pid}")
        except subprocess.CalledProcessError:
            pass  # pgrep returns 1 if no match
        except Exception as e:
            log(f"kill {name} error: {e}")
    return killed

def notify_macos(title, msg):
    try:
        script = f'display notification "{msg}" with title "{title}" sound name "Basso"'
        subprocess.run(["osascript", "-e", script],
                       timeout=3, capture_output=True)
    except Exception:
        pass

def check():
    v = vm_stat()
    usable = v["free"] + v["spec"] + v["inactive"]
    now    = datetime.datetime.now().isoformat()
    top    = top_procs_by_mem()

    status = {
        "ts":           now,
        "free_gb":      round(v["free"], 2),
        "inactive_gb":  round(v["inactive"], 2),
        "usable_gb":    round(usable, 2),
        "active_gb":    round(v["active"], 2),
        "wired_gb":     round(v["wired"], 2),
        "compressed_gb":round(v["compressed"], 2),
        "level":        "ok",
        "action":       None,
        "top_procs":    top,
    }

    if usable < CRIT_GB:
        status["level"] = "critical"
        msg = f"CRITICAL: {usable:.1f} GB usable — killing ComfyUI"
        log(msg, also_alert=True)
        notify_macos("⚠️ m2 Memory CRITICAL", msg)
        killed = kill_targets()
        status["action"] = f"killed: {', '.join(killed)}" if killed else "kill attempted (nothing found)"

    elif usable < ALERT_GB:
        status["level"] = "alert"
        msg = f"ALERT: {usable:.1f} GB usable, {v['compressed']:.1f} GB compressed"
        log(msg, also_alert=True)
        notify_macos("⚠️ m2 Memory Alert", msg)

    elif usable < WARN_GB:
        status["level"] = "warning"
        log(f"WARNING: {usable:.1f} GB usable, {v['compressed']:.1f} GB compressed")

    STATUS_PATH.write_text(json.dumps(status, indent=2))

if __name__ == "__main__":
    log(f"mem-monitor started (warn={WARN_GB}GB alert={ALERT_GB}GB crit={CRIT_GB}GB)")
    consecutive_ok = 0
    while True:
        try:
            check()
        except Exception as e:
            log(f"ERROR in check(): {e}")
        time.sleep(30)
