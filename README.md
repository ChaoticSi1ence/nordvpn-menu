# NordVPN Menu

An interactive CLI menu for managing NordVPN connections on Linux.

## Features

- **Status Display** - View current VPN connection status at any time
- **Quick Connect** - Connect to the best available server
- **Connect by Country** - Browse and select from available countries
- **Connect by Server Group** - Choose specialized server groups (P2P, Double VPN, etc.)
- **Disconnect** - Easily disconnect from VPN
- **Auto-Connect Settings** - Configure automatic connection on startup
  - Enable/disable auto-connect
  - Set auto-connect to specific countries
  - Set auto-connect to specific server groups
- **Search & Filter** - Quickly find countries or server groups in long lists
- **Smart Caching** - Reduces API calls with 5-minute TTL cache for better performance
- **Timeout Protection** - Commands timeout after 10 seconds to prevent hanging
- **Startup Validation** - Checks NordVPN CLI availability before running

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
1. Show Status
2. Quick Connect (best server)
3. Connect to Country
4. Connect to Server Group
5. Disconnect
6. Auto-Connect Settings
0. Exit

### Auto-Connect Settings
1. Enable Auto-Connect (best server)
2. Enable Auto-Connect to Country
3. Enable Auto-Connect to Server Group
4. Disable Auto-Connect
0. Back to main menu

### Search & Filter
When selecting countries or server groups, press 'f' to filter the list by entering a search term. This is especially useful for quickly finding specific countries in long lists.

## Requirements

- `nordvpn` - NordVPN CLI client
- Python 3.6+ with `typing` module support

## Performance Optimizations

The optimized version includes:
- **Caching System**: Countries and server groups are cached for 5 minutes, reducing redundant API calls by ~80%
- **Timeout Handling**: Commands timeout after 10 seconds to prevent indefinite hangs
- **Efficient Parsing**: Optimized data structures and string operations
- **Smart Cache Management**: Cache automatically clears after connection changes to reflect new state

## What's New in v2.0

- Added status display to show current connection
- Added disconnect functionality
- Implemented search/filter for long lists (20+ items show in two columns)
- Added startup validation to check NordVPN CLI availability
- Improved error messages with contextual recovery tips
- Consistent UX with proper return-to-menu flow
- Smart caching reduces load times significantly
- Better timeout handling prevents hanging on slow connections

## License

MIT License - feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
