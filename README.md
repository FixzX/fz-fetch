# Fz-Fetch - System Information Tool

A lightweight Python script that displays system information in a neofetch-style format. Works on **Linux** (Mint, Ubuntu, Fedora, Debian, etc.) and **Windows**.

## Features

- **Beautiful ASCII Art**: Large, detailed neofetch-style logos for each Linux distribution
- **Windows Support**: Works on Windows 10/11 with Windows logo display
- **1:1 Layout**: Logo on the left, system info on the right (just like neofetch)
- **Color Bar**: Shows terminal color capabilities at the bottom
- **OS Detection**: Automatically detects your operating system and distribution
- **System Information**:
  - Operating System name and version
  - Kernel version
  - System uptime
  - CPU model and core count
  - RAM usage
  - Desktop Environment (GNOME, KDE, XFCE, MATE, etc.)
  - Default shell
  - Installed packages count
  - Hostname
- **Color Output**: Nicely formatted with ANSI colors
- **Distro Logos**: Includes artwork for:
  - Linux Mint 🍃
  - Ubuntu
  - Fedora
  - Debian
  - Arch Linux
  - Windows 10/11
  - Generic Linux fallback

## Installation

1. **Clone or download** the script:
   ```bash
   git clone https://github.com/FixzX/fz-fetch.git
   cd fz-fetch
   ```

2. **Make it executable**:
   ```bash
   chmod +x fz-fetch.py
   ```

## Usage

### Run directly:
```bash
python3 fz-fetch.py
```

### Or as a command:
```bash
./fz-fetch.py
```

### Create an alias (optional):
Add this to your `~/.bashrc` or `~/.bash_aliases`:
```bash
alias fz='python3 /path/to/fz-fetch.py'
```

Then reload:
```bash
source ~/.bashrc
```

And use it anywhere:
```bash
fz
```

## Supported Distributions

**Linux:**
- **Linux Mint** 🍃 (with custom logo)
- **Ubuntu** ◯
- **Fedora**
- **Debian** ◈
- **Arch Linux** and derivatives
- **And all other Linux distributions!**

**Windows:**
- **Windows 10** and **Windows 11** ⊞

## Requirements

- Python 3.6+
- **Linux** or **Windows 10/11** operating system
- For **Linux**: Standard utilities (pre-installed):
  - `/proc/uptime`
  - `/proc/cpuinfo`
  - `/proc/meminfo`
  - `/proc/os-release`
- For **Windows**: WMI (built-in)

## Example Output

```
     .;;,.          Hostname: fixz
   .;;`,..;;.       ----------------------------------------
  .;;`'  `;;.       OS: Linux Mint 22.3
 .;;. ,::, .;;.     Kernel: 6.14.0-37-generic
 .;;.`::::'.;;.     Uptime: 1h 43m
 .;;. ':::' .;;.    Packages: 1869 (dpkg)
 .;;. .:::.;;.      Shell: bash
 .;;.'  ;;'.;;.     DE: Xfce
  `;;. ';;';;'      CPU: Intel(R) Celeron(R) CPU B820 @ 1.70GHz (2)
    `;;.;;;'        Memory: 2787MB / 3817MB
       .            
                    
  LINUX MINT        [Color Bar with 8 colors]
```

## Customization

You can modify the script to add more information or customize colors:

1. **Add more system info**: Edit the `collect_info()` method
2. **Change colors**: Modify the color codes in the `colors` dictionary
3. **Add distribution logos**: Add more entries to the `get_ascii_logo()` method

## Troubleshooting

- **"Unknown" values**: Some information might not be available in your environment
- **Wrong Desktop Environment**: Set the `DESKTOP_SESSION` environment variable if it's not detected correctly
- **Package count wrong**: Different package managers count packages differently

## Repository

**GitHub:** https://github.com/FixzX/fz-fetch

Feel free to fork, star, and contribute!

## License

MIT License - Feel free to use and modify for personal or commercial projects.
