#!/usr/bin/env python3
"""
Interactive NordVPN CLI Menu
Provides an easy way to connect to NordVPN servers with caching and optimization
"""

import subprocess
import sys
import time
from typing import Optional, List, Dict, Tuple, Any


# Cache configuration
CACHE_TTL = 300  # 5 minutes
COMMAND_TIMEOUT = 10  # seconds


class Cache:
    """Simple cache with TTL for reducing redundant API calls"""
    def __init__(self):
        self._cache: Dict[str, Tuple[Any, float]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < CACHE_TTL:
                return value
            del self._cache[key]
        return None
    
    def set(self, key: str, value: Any):
        self._cache[key] = (value, time.time())
    
    def clear(self):
        self._cache.clear()


# Global cache instance
cache = Cache()


def run_nordvpn_command(cmd: str, timeout: int = COMMAND_TIMEOUT) -> Optional[str]:
    """Execute a nordvpn command with timeout and return the output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"Error: Command timed out after {timeout} seconds")
        print("Tip: Check your network connection or try again")
        return None
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else "Unknown error"
        print(f"Error: {error_msg}")
        if "not logged in" in error_msg.lower():
            print("Tip: Run 'nordvpn login' to authenticate")
        elif "not installed" in error_msg.lower():
            print("Tip: Install nordvpn CLI from https://nordvpn.com/download/linux/")
        return None
    except FileNotFoundError:
        print("Error: nordvpn command not found")
        print("Tip: Install nordvpn CLI and ensure it's in your PATH")
        return None


def check_nordvpn_available() -> bool:
    """Check if nordvpn CLI is installed and accessible"""
    try:
        result = subprocess.run(
            ["which", "nordvpn"],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            # Verify we can actually run it
            result = subprocess.run(
                ["nordvpn", "--version"],
                capture_output=True,
                text=True,
                timeout=2
            )
            return result.returncode == 0
        return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def get_status() -> Optional[str]:
    """Get current VPN connection status"""
    return run_nordvpn_command("nordvpn status")


def display_status():
    """Display current connection status"""
    print("\n" + "="*50)
    print("CURRENT STATUS".center(50))
    print("="*50)
    status = get_status()
    if status:
        # Parse and display key information
        lines = status.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['status:', 'current server:', 'country:', 'city:', 'ip:']):
                print(line)
    else:
        print("Unable to retrieve status")
    print("="*50)


def get_countries() -> List[str]:
    """Get list of available countries from NordVPN with caching"""
    cached = cache.get('countries')
    if cached:
        return cached
    
    output = run_nordvpn_command("nordvpn countries")
    if output:
        countries = []
        for line in output.split('\n'):
            if line.strip() and not line.startswith('*'):
                countries.extend([c.strip() for c in line.split() if c.strip()])
        countries = sorted(countries)
        cache.set('countries', countries)
        return countries
    return []


def get_groups() -> List[str]:
    """Get list of available server groups from NordVPN with caching"""
    cached = cache.get('groups')
    if cached:
        return cached
    
    output = run_nordvpn_command("nordvpn groups")
    if output:
        # Filter out location-based groups
        location_groups = {
            'Africa_The_Middle_East_And_India',
            'Asia_Pacific',
            'Europe',
            'The_Americas'
        }
        groups = []
        for line in output.split('\n'):
            if line.strip():
                groups.extend([g.strip() for g in line.split() if g.strip()])
        groups = [g for g in groups if g not in location_groups]
        groups = sorted(groups)
        cache.set('groups', groups)
        return groups
    return []


def filter_items(items: List[str], prompt: str = "Enter search term (or press Enter to skip): ") -> List[str]:
    """Filter a list of items based on user input"""
    search = input(prompt).strip().lower()
    if not search:
        return items
    return [item for item in items if search in item.lower()]


def display_menu(title: str, items: List[str], back_option: bool = True, show_filter: bool = False) -> int:
    """Display a numbered menu and get user choice"""
    current_items = items
    
    while True:
        print(f"\n{'='*50}")
        print(f"{title:^50}")
        print(f"{'='*50}")
        
        if not current_items:
            print("No items match your filter.")
            print("\nOptions:")
            print("  r. Reset filter")
            print("  0. Back")
            choice = input("\nEnter your choice: ").strip().lower()
            if choice == 'r':
                current_items = items
                continue
            elif choice == '0':
                return 0
            continue
        
        # Display items in columns if many items
        if len(current_items) > 20:
            mid = (len(current_items) + 1) // 2
            for i in range(mid):
                left = f"{i+1:3d}. {current_items[i]}"
                if i + mid < len(current_items):
                    right = f"{i+mid+1:3d}. {current_items[i+mid]}"
                    print(f"{left:35s} {right}")
                else:
                    print(left)
        else:
            for idx, item in enumerate(current_items, 1):
                print(f"{idx:3d}. {item}")
        
        print()
        if show_filter:
            print("  f. Filter list")
        if back_option:
            print("  0. Back to main menu")
        else:
            print("  0. Exit")
        
        print(f"{'='*50}")
        
        try:
            choice = input("\nEnter your choice: ").strip().lower()
            
            if choice == 'f' and show_filter:
                filtered = filter_items(current_items)
                if filtered:
                    current_items = filtered
                else:
                    print("No matches found. Showing all items.")
                continue
            
            choice_num = int(choice)
            if 0 <= choice_num <= len(current_items):
                return choice_num
            else:
                print(f"Please enter a number between 0 and {len(current_items)}")
        except ValueError:
            print("Please enter a valid number (or 'f' to filter)")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            sys.exit(0)


def execute_connection(connection_type: str, target: Optional[str] = None, is_group: bool = False):
    """Generic function to execute connection commands"""
    if target:
        display_name = target.replace('_', ' ')
        if is_group:
            print(f"\nConnecting to {display_name} servers...")
            output = run_nordvpn_command(f"nordvpn connect --group {target}")
        else:
            print(f"\nConnecting to {display_name}...")
            output = run_nordvpn_command(f"nordvpn connect {target}")
    else:
        print(f"\nConnecting to the best available server...")
        output = run_nordvpn_command("nordvpn connect")
    
    if output:
        print(output)
        # Clear cache after successful connection
        cache.clear()


def execute_autoconnect(target: Optional[str] = None, is_group: bool = False, enable: bool = True):
    """Generic function to configure autoconnect"""
    if not enable:
        print("\nDisabling auto-connect...")
        output = run_nordvpn_command("nordvpn set autoconnect off")
    elif target:
        display_name = target.replace('_', ' ')
        if is_group:
            print(f"\nSetting auto-connect to {display_name} servers...")
            output = run_nordvpn_command(f"nordvpn set autoconnect on {target}")
        else:
            print(f"\nSetting auto-connect to {display_name}...")
            output = run_nordvpn_command(f"nordvpn set autoconnect on {target}")
    else:
        print("\nEnabling auto-connect to best server...")
        output = run_nordvpn_command("nordvpn set autoconnect on")
    
    if output:
        print(output)


def connect_quick():
    """Quick connect to the best server"""
    execute_connection("quick")


def disconnect():
    """Disconnect from VPN"""
    print("\nDisconnecting from VPN...")
    output = run_nordvpn_command("nordvpn disconnect")
    if output:
        print(output)
        cache.clear()


def connect_country():
    """Connect to a specific country"""
    countries = get_countries()
    if not countries:
        print("Failed to retrieve country list")
        return
    
    choice = display_menu("Select a Country", countries, show_filter=True)
    if choice == 0:
        return
    
    country = countries[choice - 1]
    execute_connection("country", country)


def connect_group():
    """Connect to a specific server group"""
    groups = get_groups()
    if not groups:
        print("Failed to retrieve groups list")
        return
    
    choice = display_menu("Select a Server Group", groups, show_filter=True)
    if choice == 0:
        return
    
    group = groups[choice - 1]
    execute_connection("group", group, is_group=True)


def autoconnect_country():
    """Set auto-connect to a specific country"""
    countries = get_countries()
    if not countries:
        print("Failed to retrieve country list")
        return
    
    choice = display_menu("Select a Country for Auto-Connect", countries, show_filter=True)
    if choice == 0:
        return
    
    country = countries[choice - 1]
    execute_autoconnect(country)


def autoconnect_group():
    """Set auto-connect to a specific server group"""
    groups = get_groups()
    if not groups:
        print("Failed to retrieve groups list")
        return
    
    choice = display_menu("Select a Server Group for Auto-Connect", groups, show_filter=True)
    if choice == 0:
        return
    
    group = groups[choice - 1]
    execute_autoconnect(group, is_group=True)


def autoconnect_menu():
    """Display auto-connect submenu"""
    options = [
        "Enable Auto-Connect (best server)",
        "Enable Auto-Connect to Country",
        "Enable Auto-Connect to Server Group",
        "Disable Auto-Connect"
    ]
    
    choice = display_menu("Auto-Connect Settings", options)
    
    if choice == 0:
        return
    elif choice == 1:
        execute_autoconnect()
        input("\nPress Enter to continue...")
    elif choice == 2:
        autoconnect_country()
        input("\nPress Enter to continue...")
    elif choice == 3:
        autoconnect_group()
        input("\nPress Enter to continue...")
    elif choice == 4:
        execute_autoconnect(enable=False)
        input("\nPress Enter to continue...")


def main_menu():
    """Display the main menu"""
    options = [
        "Show Status",
        "Quick Connect (best server)",
        "Connect to Country",
        "Connect to Server Group",
        "Disconnect",
        "Auto-Connect Settings"
    ]
    
    while True:
        choice = display_menu("NordVPN Quick Connect", options, back_option=False)
        
        if choice == 0:
            print("\nExiting...")
            sys.exit(0)
        elif choice == 1:
            display_status()
            input("\nPress Enter to continue...")
        elif choice == 2:
            connect_quick()
            input("\nPress Enter to continue...")
        elif choice == 3:
            connect_country()
            input("\nPress Enter to continue...")
        elif choice == 4:
            connect_group()
            input("\nPress Enter to continue...")
        elif choice == 5:
            disconnect()
            input("\nPress Enter to continue...")
        elif choice == 6:
            autoconnect_menu()


def main():
    """Main entry point with startup checks"""
    print("NordVPN Interactive Menu")
    print("Checking NordVPN CLI availability...")
    
    if not check_nordvpn_available():
        print("\nError: NordVPN CLI is not installed or not accessible")
        print("\nPlease install NordVPN CLI:")
        print("  Visit: https://nordvpn.com/download/linux/")
        print("  Or run: sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)")
        sys.exit(1)
    
    print("✓ NordVPN CLI detected\n")
    
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
