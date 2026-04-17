# Fz-Fetch

Highly inspired by **fastfetch** and **neofetch**

Lightweight system information display tool for Linux and Windows.

## Features

- Neofetch-style 1:1 layout (logo left, info right)
- ASCII art for 15+ Linux distributions
- Windows 10/11 support
- ANSI color output with terminal color bar

## Supported Distros

Linux Mint, Ubuntu, Fedora, Debian, Arch Linux, Gentoo, Kali Linux, Rocky Linux, RHEL, openSUSE, Pop!_OS, Elementary OS, Zorin OS, MX Linux, Linux Lite, Windows, Generic

## System Information

DateTime, Hostname, OS, Kernel, Uptime, Packages, Shell, Desktop Environment, Display, CPU, GPU, Memory, Disk

## Installation

```bash
git clone https://github.com/FixzX/fz-fetch.git
cd fz-fetch
chmod +x fz-fetch.py
```

## Usage

```bash
python3 fz-fetch.py
# or alias
alias fz='python3 /path/to/fz-fetch.py'
fz
```

## Requirements

- Python 3.6+
- Linux or Windows 10/11
- Linux: /proc filesystem (standard)
- Windows: WMI (built-in)

## Example

```
     .;;,.          DateTime: 2026-04-17 22:43:12
   .;;`,..;;.       ----------------------------------------
  .;;`'  `;;.       Hostname: fixz
 .;;. ,::, .;;.     OS: Linux Mint 22.3
 .;;.`::::'.;;.     Kernel: 6.14.0-37-generic
 .;;. ':::' .;;.    Uptime: 2h 2m
 .;;. .:::.;;.      Packages: 1869 (dpkg)
 .;;.'  ;;'.;;.     Shell: bash
  `;;. ';;';;'      DE: Xfce
    `;;.;;;'        Display: 1366x768
       .            CPU: Intel Core 2 Duo (2)
                    GPU: Intel Integrated
  LINUX MINT        Memory: 2821MB / 3817MB
                    Disk: 15GB / 109GB
```

## Customization

- Add system info: Edit `collect_info()` method
- Change colors: Modify `colors` dictionary
- Add distro logos: Edit `get_ascii_logo()` method

## Troubleshooting

- Unknown values: Some info unavailable in environment
- Wrong DE: Set DESKTOP_SESSION variable
- Package count: Managers count differently

## Links

GitHub: https://github.com/FixzX/fz-fetch

Inspired by [neofetch](https://github.com/dylanaraps/neofetch) and [fastfetch](https://github.com/LinusDierckxsens/fastfetch)

## License

MIT - Use freely
