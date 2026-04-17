# Fz-Fetch - System Information Tool

A lightweight Python script that displays system information in a neofetch-style format. Works on Linux Mint, Ubuntu, Fedora, Debian, and other Linux distributions.

## Features

- **OS Detection**: Automatically detects your Linux distribution
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
- **Beautiful ASCII Art**: Shows a logo based on your Linux distribution
- **Color Output**: Nicely formatted with colors

## Installation

1. **Clone or download** the script:
   ```bash
   git clone <repository-url>
   cd fahh
   ```

   Or if you already have the file, navigate to its directory.

2. **Make it executable**:
   ```bash
   chmod +x neofetch.py
   ```

## Usage

### Run directly:
```bash
python3 neofetch.py
```

### Or as a command:
```bash
./neofetch.py
```

### Create an alias (optional):
Add this to your `~/.bashrc` or `~/.bash_aliases`:
```bash
alias nf='python3 /path/to/neofetch.py'
```

Then reload:
```bash
source ~/.bashrc
```

And use it anywhere:
```bash
nf
```

## Supported Distributions

- **Linux Mint** 🍃 (with custom logo)
- **Ubuntu** ◯
- **Fedora**
- **Debian** ◈
- **Arch Linux** and derivatives
- **And all other Linux distributions!**

## Requirements

- Python 3.6+
- Linux operating system
- Standard Linux tools (should be pre-installed):
  - `/proc/uptime`
  - `/proc/cpuinfo`
  - `/proc/meminfo`
  - `/proc/os-release`

## Example Output

```
    ╔═════════════════╗
    ║   🍃 LINUX     ║
    ║    MINT        ║
    ╚═════════════════╝

  OS:       Linux Mint 22.3
  Kernel:   6.14.0-37-generic
  Uptime:   1h 10m
  CPU:      Intel(R) Celeron(R) CPU B820 @ 1.70GHz (2)
  Memory:   1858MB / 3817MB
  DE:       Xfce
  Shell:    bash
  Packages: 1865 (dpkg)
  Hostname: fixz
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

## License

Free to use and modify for personal or commercial projects.
