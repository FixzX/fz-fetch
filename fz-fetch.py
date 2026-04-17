#!/usr/bin/env python3

import os
import sys
import platform
import subprocess
import re
from pathlib import Path
from datetime import datetime, timedelta


class SystemInfo:
    def __init__(self):
        self.info = {}
        self.is_windows = platform.system() == "Windows"
        self.colors = {
            'reset': '\033[0m',
            'bold': '\033[1m',
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
        }

    def run_command(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            return result.stdout.strip()
        except Exception:
            return "Unknown"

    def get_os_info(self):
        if self.is_windows:
            try:
                version = self.run_command("wmic os get caption | findstr /r .")
                version = version.replace("Caption", "").strip()
                return version if version else platform.system()
            except:
                return platform.system()
        else:
            try:
                if Path('/etc/os-release').exists():
                    with open('/etc/os-release') as f:
                        lines = f.readlines()
                        os_info = {}
                        for line in lines:
                            key, value = line.strip().split('=', 1)
                            os_info[key] = value.strip('"')
                        
                        name = os_info.get('NAME', 'Linux')
                        version = os_info.get('VERSION', '')
                        pretty_name = os_info.get('PRETTY_NAME', f"{name} {version}")
                        return pretty_name
                else:
                    return platform.system()
            except Exception:
                return platform.system()

    def get_kernel(self):
        return platform.release()

    def get_uptime(self):
        if self.is_windows:
            return "Unknown"
        else:
            try:
                with open('/proc/uptime') as f:
                    uptime_seconds = int(float(f.read().split()[0]))
                    uptime = timedelta(seconds=uptime_seconds)
                    
                    days = uptime.days
                    hours, remainder = divmod(uptime.seconds, 3600)
                    minutes, _ = divmod(remainder, 60)
                    
                    parts = []
                    if days > 0:
                        parts.append(f"{days}d")
                    if hours > 0:
                        parts.append(f"{hours}h")
                    if minutes > 0:
                        parts.append(f"{minutes}m")
                    
                    return ' '.join(parts) if parts else "0m"
            except Exception:
                return "Unknown"

    def get_cpu(self):
        try:
            cpu_count = os.cpu_count() or 1
            
            if self.is_windows:
                model = self.run_command("wmic cpu get name | findstr /r .")
                model = model.replace("Name", "").strip()
                if model:
                    return f"{model} ({cpu_count})"
            else:
                try:
                    with open('/proc/cpuinfo') as f:
                        for line in f:
                            if 'model name' in line:
                                model = line.split(':', 1)[1].strip()
                                model = re.sub(r'\s+', ' ', model)
                                return f"{model} ({cpu_count})"
                except Exception:
                    pass
            
            return f"{cpu_count} cores"
        except Exception:
            return "Unknown"

    def get_memory(self):
        if self.is_windows:
            try:
                mem_info = self.run_command("wmic os get totalvisibleMemorySize,freephysicalmemory | findstr /r .")
                if mem_info and mem_info != "Unknown":
                    parts = mem_info.split()
                    if len(parts) >= 2:
                        total = int(parts[0]) // 1024
                        free = int(parts[1]) // 1024
                        used = total - free
                        return f"{used}MB / {total}MB"
                return "Unknown"
            except:
                return "Unknown"
        else:
            try:
                with open('/proc/meminfo') as f:
                    meminfo = {}
                    for line in f:
                        key, value = line.split(':', 1)
                        meminfo[key.strip()] = int(value.split()[0])
                
                total_mb = meminfo.get('MemTotal', 0) // 1024
                available_mb = meminfo.get('MemAvailable', 0) // 1024
                used_mb = total_mb - available_mb
                
                return f"{used_mb}MB / {total_mb}MB"
            except Exception:
                return "Unknown"

    def get_desktop_environment(self):
        if self.is_windows:
            return "Windows Desktop"
        else:
            de_vars = ['GNOME_DESKTOP_SESSION_ID', 'KDE_FULL_SESSION', 'TDE_FULL_SESSION', 
                       'MATE_DESKTOP_SESSION_ID', 'XFCE_DESKTOP_SESSION', 'LXSESSION_PID',
                       'DESKTOP_SESSION']
            
            for var in de_vars:
                if os.environ.get(var):
                    if 'gnome' in var.lower():
                        return "GNOME"
                    elif 'kde' in var.lower():
                        return "KDE"
                    elif 'mate' in var.lower():
                        return "MATE"
                    elif 'xfce' in var.lower():
                        return "XFCE"
                    elif 'lx' in var.lower():
                        return "LXDesktop"
            
            desktop_session = os.environ.get('DESKTOP_SESSION', '').lower()
            if desktop_session:
                return desktop_session.title()
            
            try:
                processes = self.run_command("ps aux | grep -E '(gnome-shell|kwin|mate-panel|xfwm4|lxde)' | grep -v grep")
                if 'gnome' in processes.lower():
                    return "GNOME"
                elif 'kwin' in processes.lower():
                    return "KDE"
                elif 'mate' in processes.lower():
                    return "MATE"
                elif 'xfwm' in processes.lower():
                    return "XFCE"
            except Exception:
                pass
            
            return "Unknown"

    def get_shell(self):
        if self.is_windows:
            return "PowerShell" if "POWERSHELL" in os.environ.get('PROMPT', '').upper() else "CMD"
        else:
            shell = os.environ.get('SHELL', 'Unknown')
            return Path(shell).name if shell != 'Unknown' else shell

    def get_hostname(self):
        return platform.node()

    def get_packages(self):
        if self.is_windows:
            try:
                count = self.run_command("powershell -Command \"(Get-WmiObject -Class Win32_Product | Measure-Object).Count\"")
                return f"{count} (WMI)" if count != "Unknown" else "Unknown"
            except:
                return "Unknown"
        else:
            commands = [
                ("dpkg -l | grep '^ii' | wc -l", "dpkg"),
                ("rpm -qa | wc -l", "rpm"),
                ("pacman -Q | wc -l", "pacman"),
                ("xbps-query -l | wc -l", "xbps"),
            ]
            
            for cmd, name in commands:
                try:
                    check = self.run_command(f"which {name.split()[0]} 2>/dev/null")
                    if check and check != "Unknown":
                        result = self.run_command(cmd)
                        if result and result != "Unknown":
                            return f"{result} ({name})"
                except Exception:
                    pass
            
            return "Unknown"

    def collect_info(self):
        self.info = {
            'OS': self.get_os_info(),
            'Kernel': self.get_kernel(),
            'Uptime': self.get_uptime(),
            'CPU': self.get_cpu(),
            'Memory': self.get_memory(),
            'DE': self.get_desktop_environment(),
            'Shell': self.get_shell(),
            'Packages': self.get_packages(),
            'Hostname': self.get_hostname(),
        }
        return self.info

    def get_ascii_logo(self, os_name):
        logos = {
            'Windows': [
                "  ┌─────────────────┐  ",
                "  │ ┌─────┐ ┌─────┐ │  ",
                "  │ │     │ │     │ │  ",
                "  │ │  █  │ │  █  │ │  ",
                "  │ │     │ │     │ │  ",
                "  │ ├─────┤ ├─────┤ │  ",
                "  │ │ ┌─────────────┐ │ ",
                "  │ │ │     │     │ │ │ ",
                "  │ │ │  █  │  █  │ │ │ ",
                "  │ │ │     │     │ │ │ ",
                "  │ │ └─────────────┘ │ ",
                "  │ └─────┘ └─────┘ │  ",
                "  └─────────────────┘  ",
                "                       ",
                "      WINDOWS          ",
                "                       ",
                "                       ",
                "                       ",
                "                       ",
                "                       ",
            ],
            'Linux Mint': [
                "       .;;,.        ",
                "     .;;`,..;;.     ",
                "    .;;`'  `;;.     ",
                "   .;;. ,::, .;;.   ",
                "   .;;.`::::'.;;.   ",
                "   .;;. ':::' .;;.  ",
                "   .;;. .:::.;;.    ",
                "   .;;.'  ;;'.;;.   ",
                "    `;;. ';;';;'    ",
                "      `;;.;;;'      ",
                "         .          ",
                "                    ",
                "    LINUX MINT      ",
                "                    ",
                "                    ",
                "                    ",
                "                    ",
                "                    ",
                "                    ",
                "                    ",
            ],
            'Ubuntu': [
                "           ...      ",
                "         .MMMMM.    ",
                "        .MMMMMMM.   ",
                "       .MMMMMMMM.   ",
                "      .MMMMMMMMM.   ",
                "     .MMMM    MMM.  ",
                "    .MMMM  MM  MMM. ",
                "    .MMM   MM   MMM.",
                "    .MMM   MM   MMM.",
                "    .MMM   MM   MMM.",
                "    .MMMM      MMM. ",
                "     .MMMM  MMMM.   ",
                "      .MMMMMMMM.    ",
                "       .MMMMMMM.    ",
                "        .MMMMM.     ",
                "         .MMM.      ",
                "          .M.       ",
                "                    ",
                "       UBUNTU       ",
                "                    ",
            ],
            'Fedora': [
                "        /@@@@\\      ",
                "       /@@@@@@\\     ",
                "      |@@@@@@@@|    ",
                "     |@@@@@@@@@|    ",
                "     |@@@@@@@@@|    ",
                "    |@@@@@ ^ @@@|   ",
                "    |@@@@  > @@@@|  ",
                "   |@@@@      @@@@| ",
                "   |@@@@  ####@@@@| ",
                "   |@@@@  ####@@@@| ",
                "    |@@@@@@@@@@@|   ",
                "    |@@@@@@@@@@@|   ",
                "     |@@@@@@@@@|    ",
                "      |@@@@@@@|     ",
                "       |@@@@@|      ",
                "        \\@@@/       ",
                "                    ",
                "       FEDORA       ",
                "                    ",
                "                    ",
            ],
            'Debian': [
                "       .------.     ",
                "      /  _____ \\    ",
                "     /  /     \\ \\   ",
                "    |  |  o o  | |  ",
                "    |  |   <>  | |  ",
                "    |  | \\___/ | |  ",
                "     \\  \\     / /   ",
                "      \\  '---'  /   ",
                "       '------'     ",
                "         | |        ",
                "        /   \\       ",
                "       | _ _ |      ",
                "        \\ - /       ",
                "        / | \\       ",
                "       /  |  \\      ",
                "      |   |   |     ",
                "     /    |    \\    ",
                "                    ",
                "    DEBIAN GNU      ",
                "                    ",
            ],
            'Arch Linux': [
                "           /\\       ",
                "          /  \\      ",
                "         /    \\     ",
                "        /      \\    ",
                "       /        \\   ",
                "      /          \\  ",
                "     /    /\\      \\ ",
                "    /    /  \\      \\",
                "   /    /    \\      \\",
                "  /    /______\\      \\",
                " /    /        \\      \\",
                "/____/          \\______\\",
                "\\    \\          /    / ",
                " \\    \\        /    /  ",
                "  \\    \\______/    /   ",
                "   \\            /      ",
                "    \\__________/       ",
                "                       ",
                "    ARCH LINUX         ",
                "                       ",
            ],
            'Gentoo': [
                "           \\  /      ",
                "            \\/       ",
                "            /\\       ",
                "           /  \\      ",
                "          /    \\     ",
                "         /______\\    ",
                "        /        \\   ",
                "       /  \\    /  \\  ",
                "      /    \\  /    \\ ",
                "     /______\\/______\\",
                "    /  \\        /  \\ ",
                "   /    \\      /    \\",
                "  /______\\____/______\\",
                "                    ",
                "                    ",
                "                    ",
                "       GENTOO       ",
                "                    ",
                "                    ",
                "                    ",
            ],
            'Kali Linux': [
                "      ___________   ",
                "     / \\  K A L I / ",
                "    /   \\________/  ",
                "   / |  |\\        \\ ",
                "  /  |  | \\        \\",
                " /   |  |  \\        \\",
                "|    |  |   |        |",
                "|    |  |   |        |",
                "|    \\  |  /        /",
                " \\   |  | /        / ",
                "  \\ |  |/        /  ",
                "   \\|  |        /   ",
                "    |  |       /    ",
                "    |  |______/     ",
                "    |   LINUX       ",
                "    |               ",
                "    |               ",
                "                    ",
                "   KALI LINUX       ",
                "                    ",
            ],
            'default': [
                "     ___            ",
                "    /   \\           ",
                "   | o o |          ",
                "   |  >  |          ",
                "   |     |          ",
                "    \\ - /           ",
                "     | |            ",
                "    _| |_           ",
                "   / | | \\          ",
                "  |  | |  |         ",
                "  | _| | _|         ",
                " _|/ | | \\|_        ",
                "/ |  | |  | \\       ",
                "  |  | |  |         ",
                "  \\  | |  /         ",
                "   \\ | | /          ",
                "    \\| |/           ",
                "     | |            ",
                "     LINUX          ",
                "                    ",
            ]
        }
        
        if self.is_windows or 'Windows' in os_name:
            return logos['Windows']
        
        for key in logos:
            if key.lower() in os_name.lower():
                return logos[key]
        
        return logos['default']

    def display(self):
        self.collect_info()
        
        os_name = self.info['OS']
        logo_lines = self.get_ascii_logo(os_name)
        
        info_lines = []
        
        info_labels = {
            'Hostname': self.info.get('Hostname', 'Unknown'),
            'OS': self.info.get('OS', 'Unknown'),
            'Kernel': self.info.get('Kernel', 'Unknown'),
            'Uptime': self.info.get('Uptime', 'Unknown'),
            'Packages': self.info.get('Packages', 'Unknown'),
            'Shell': self.info.get('Shell', 'Unknown'),
            'DE': self.info.get('DE', 'Unknown'),
            'CPU': self.info.get('CPU', 'Unknown'),
            'Memory': self.info.get('Memory', 'Unknown'),
        }
        
        separator = f"{self.colors['white']}{'-' * 40}{self.colors['reset']}"
        
        for i, (label, value) in enumerate(info_labels.items()):
            if i == 1:
                info_lines.append(separator)
            
            label_colored = f"{self.colors['white']}{label}:{self.colors['reset']}"
            value_colored = f"{self.colors['cyan']}{value}{self.colors['reset']}"
            info_lines.append(f"{label_colored} {value_colored}")
        
        print(f"\n{self.colors['reset']}", end="")
        
        max_lines = max(len(logo_lines), len(info_lines))
        
        for i in range(max_lines):
            if i < len(logo_lines):
                logo_line = f"{self.colors['cyan']}{logo_lines[i]}{self.colors['reset']}"
            else:
                logo_line = " " * 20
            
            if i < len(info_lines):
                info_line = info_lines[i]
            else:
                info_line = ""
            
            print(f"  {logo_line}  {info_line}")
        
        sys.stdout.flush()
        color_bar = f"\n  \033[40m  \033[0m\033[41m  \033[0m\033[42m  \033[0m\033[43m  \033[0m\033[44m  \033[0m\033[45m  \033[0m\033[46m  \033[0m\033[47m  \033[0m\n"
        print(color_bar, flush=True)


def main():
    system_info = SystemInfo()
    system_info.display()


if __name__ == '__main__':
    main()
