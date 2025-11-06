# NordVPN Menu

An interactive CLI menu for managing NordVPN connections on Linux.

## Features

- **Quick Connect** - Connect to the best available server
- **Connect by Country** - Browse and select from available countries
- **Connect by Server Group** - Choose specialized server groups (P2P, Double VPN, etc.)
- **Auto-Connect Settings** - Configure automatic connection on startup
  - Enable/disable auto-connect
  - Set auto-connect to specific countries
  - Set auto-connect to specific server groups

## Prerequisites

- Linux operating system
- [NordVPN CLI](https://support.nordvpn.com/Connectivity/Linux/1325531132/Installing-and-using-NordVPN-on-Debian-Ubuntu-Raspberry-Pi-Elementary-OS-and-Linux-Mint.htm) installed and configured
- Python 3.6 or higher
- Active NordVPN subscription

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/nordvpn-menu.git
cd nordvpn-menu
```

2. Make the script executable:
```bash
chmod +x nordvpn_menu.py
```

3. (Optional) Create a symlink to run from anywhere:
```bash
sudo ln -s $(pwd)/nordvpn_menu.py /usr/local/bin/nordvpn-menu
```

## Usage

Run the script:
```bash
./nordvpn_menu.py
```

Or if you created a symlink:
```bash
nordvpn-menu
```

Navigate through the menus using numbers and follow the prompts.

## Menu Options

### Main Menu
1. Quick Connect (best server)
2. Connect to Country
3. Connect to Server Group
4. Auto-Connect Settings
0. Exit

### Auto-Connect Settings
1. Enable Auto-Connect (best server)
2. Enable Auto-Connect to Country
3. Enable Auto-Connect to Server Group
4. Disable Auto-Connect
0. Back to main menu

## Requirements

- `nordvpn` - NordVPN CLI client

## License

MIT License - feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
