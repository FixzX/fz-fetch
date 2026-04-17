#!/usr/bin/env python3
"""
Fz-Fetch - System Information Display Tool
A lightweight neofetch-like tool that works on Linux Mint, Ubuntu, Fedora, and other Linux distributions
"""

import os
import platform
import subprocess
import re
from pathlib import Path
from datetime import datetime, timedelta


class SystemInfo:
    def __init__(self):
        self.info = {}
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
        """Run a command and return output"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            return result.stdout.strip()
        except Exception:
            return "Unknown"

    def get_os_info(self):
        """Get OS information"""
        try:
            # Try to read os-release first (works on all modern distros)
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
        """Get kernel version"""
        return platform.release()

    def get_uptime(self):
        """Get system uptime"""
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
        """Get CPU information"""
        try:
            cpu_count = os.cpu_count() or 1
            
            # Try to get CPU model
            try:
                with open('/proc/cpuinfo') as f:
                    for line in f:
                        if 'model name' in line:
                            model = line.split(':', 1)[1].strip()
                            # Clean up the model name
                            model = re.sub(r'\s+', ' ', model)
                            return f"{model} ({cpu_count})"
            except Exception:
                pass
            
            return f"{cpu_count} cores"
        except Exception:
            return "Unknown"

    def get_memory(self):
        """Get memory information"""
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
        """Get desktop environment"""
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
        
        # Try to detect from processes
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
        """Get shell information"""
        shell = os.environ.get('SHELL', 'Unknown')
        return Path(shell).name if shell != 'Unknown' else shell

    def get_hostname(self):
        """Get hostname"""
        return platform.node()

    def get_packages(self):
        """Count installed packages"""
        # Try different package managers
        commands = [
            ("dpkg -l | grep '^ii' | wc -l", "dpkg"),  # Debian/Ubuntu/Mint (only installed)
            ("rpm -qa | wc -l", "rpm"),   # Fedora/RHEL
            ("pacman -Q | wc -l", "pacman"),  # Arch
            ("xbps-query -l | wc -l", "xbps"),  # Void
        ]
        
        for cmd, name in commands:
            try:
                # Check if package manager exists
                check = self.run_command(f"which {name.split()[0]} 2>/dev/null")
                if check and check != "Unknown":
                    result = self.run_command(cmd)
                    if result and result != "Unknown":
                        return f"{result} ({name})"
            except Exception:
                pass
        
        return "Unknown"

    def collect_info(self):
        """Collect all system information"""
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
        """Return ASCII art logo for the OS - Neofetch style"""
        logos = {
            'Linux Mint': [
                "       .;;,.       ",
                "     .;;`,..;;.    ",
                "    .;;`'  `;;.    ",
                "   .;;. ,::, .;;.  ",
                "   .;;.`::::'.;;.  ",
                "   .;;. ':::' .;;. ",
                "   .;;. .:::.;;.   ",
                "    `;;. ';;';;'   ",
                "      `;;.;;;'     ",
                "          .        ",
                "      LINUX MINT   ",
            ],
            'Ubuntu': [
                "          .----. ",
                "        / Ubuntu \\ ",
                "       |  o    o | ",
                "       |    <>    | ",
                "       |  \\____/ | ",
                "        \\        / ",
                "         '------' ",
                "                  ",
                "                  ",
                "       UBUNTU     ",
            ],
            'Fedora': [
                "         ,-. ",
                "        /   \\ ",
                "       | o o | ",
                "       |  >  | ",
                "       | --- | ",
                "        \\___/ ",
                "         | | ",
                "        /   \\ ",
                "       /     \\ ",
                "        FEDORA ",
            ],
            'Debian': [
                "    ___           ",
                "   /   \\__        ",
                "  |  o  o  \\      ",
                "  |    >    |     ",
                "  |  \\___/  |     ",
                "   \\      _/      ",
                "    '----'        ",
                "                  ",
                "                  ",
                "     DEBIAN       ",
            ],
            'Arch Linux': [
                "       /\\         ",
                "      /  \\        ",
                "     /    \\       ",
                "    /      \\      ",
                "   /   /\\   \\     ",
                "  /   /  \\   \\    ",
                " /   /____\\   \\   ",
                "/   /      \\   \\  ",
                "    ARCH LINUX    ",
            ],
            'default': [
                "      .-----.     ",
                "     /  o o  \\    ",
                "    |    >    |   ",
                "    |  \\___/  |   ",
                "     \\       /    ",
                "      '-._.-'     ",
                "                  ",
                "       LINUX      ",
            ]
        }
        
        for key in logos:
            if key.lower() in os_name.lower():
                return logos[key]
        
        return logos['default']

    def display(self):
        """Display system information in neofetch style"""
        self.collect_info()
        
        os_name = self.info['OS']
        logo_lines = self.get_ascii_logo(os_name)
        
        # Build info lines with better formatting
        info_lines = []
        max_label_len = max(len(label) for label in self.info.keys())
        
        for label, value in self.info.items():
            label_str = f"{label}:".ljust(max_label_len + 1)
            info_lines.append(f"{self.colors['magenta']}{label_str}{self.colors['cyan']}{value}{self.colors['reset']}")
        
        # Print logo and info side by side like neofetch
        print()
        max_lines = max(len(logo_lines), len(info_lines))
        
        for i in range(max_lines):
            # Logo line
            if i < len(logo_lines):
                logo_line = f"{self.colors['cyan']}{logo_lines[i]}{self.colors['reset']}"
            else:
                logo_line = " " * 20
            
            # Info line
            if i < len(info_lines):
                info_line = info_lines[i]
            else:
                info_line = ""
            
            print(f"  {logo_line}  {info_line}")
        
        print()


def main():
    """Main function"""
    system_info = SystemInfo()
    system_info.display()


if __name__ == '__main__':
    main()
