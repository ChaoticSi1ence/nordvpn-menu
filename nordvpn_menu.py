#!/usr/bin/env python3
"""
Interactive NordVPN CLI Menu
Provides an easy way to connect to NordVPN servers
"""

import subprocess
import sys


def run_nordvpn_command(cmd):
    """Execute a nordvpn command and return the output"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None


def get_countries():
    """Get list of available countries from NordVPN"""
    output = run_nordvpn_command("nordvpn countries")
    if output:
        # Parse countries, filter out the virtual location note
        countries = []
        for line in output.split('\n'):
            if line.strip() and not line.startswith('*'):
                # Split by whitespace and add each country
                countries.extend([c.strip() for c in line.split() if c.strip()])
        return sorted(countries)
    return []


def get_groups():
    """Get list of available server groups from NordVPN"""
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
        # Filter out location-based groups
        groups = [g for g in groups if g not in location_groups]
        return sorted(groups)
    return []


def display_menu(title, items, back_option=True):
    """Display a numbered menu and get user choice"""
    print(f"\n{'='*50}")
    print(f"{title:^50}")
    print(f"{'='*50}")
    
    for idx, item in enumerate(items, 1):
        print(f"{idx:3d}. {item}")
    
    if back_option:
        print(f"  0. Back to main menu")
    else:
        print(f"  0. Exit")
    
    print(f"{'='*50}")
    
    while True:
        try:
            choice = input("\nEnter your choice: ").strip()
            choice_num = int(choice)
            if 0 <= choice_num <= len(items):
                return choice_num
            else:
                print(f"Please enter a number between 0 and {len(items)}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            sys.exit(0)


def connect_quick():
    """Quick connect to the best server"""
    print("\nConnecting to the best available server...")
    output = run_nordvpn_command("nordvpn connect")
    if output:
        print(output)


def connect_country():
    """Connect to a specific country"""
    countries = get_countries()
    if not countries:
        print("Failed to retrieve country list")
        return
    
    choice = display_menu("Select a Country", countries)
    if choice == 0:
        return
    
    country = countries[choice - 1]
    print(f"\nConnecting to {country.replace('_', ' ')}...")
    output = run_nordvpn_command(f"nordvpn connect {country}")
    if output:
        print(output)


def connect_group():
    """Connect to a specific server group"""
    groups = get_groups()
    if not groups:
        print("Failed to retrieve groups list")
        return
    
    choice = display_menu("Select a Server Group", groups)
    if choice == 0:
        return
    
    group = groups[choice - 1]
    print(f"\nConnecting to {group.replace('_', ' ')} servers...")
    output = run_nordvpn_command(f"nordvpn connect --group {group}")
    if output:
        print(output)


def autoconnect_off():
    """Disable auto-connect"""
    print("\nDisabling auto-connect...")
    output = run_nordvpn_command("nordvpn set autoconnect off")
    if output:
        print(output)


def autoconnect_country():
    """Set auto-connect to a specific country"""
    countries = get_countries()
    if not countries:
        print("Failed to retrieve country list")
        return
    
    choice = display_menu("Select a Country for Auto-Connect", countries)
    if choice == 0:
        return
    
    country = countries[choice - 1]
    print(f"\nSetting auto-connect to {country.replace('_', ' ')}...")
    output = run_nordvpn_command(f"nordvpn set autoconnect on {country}")
    if output:
        print(output)


def autoconnect_group():
    """Set auto-connect to a specific server group"""
    groups = get_groups()
    if not groups:
        print("Failed to retrieve groups list")
        return
    
    choice = display_menu("Select a Server Group for Auto-Connect", groups)
    if choice == 0:
        return
    
    group = groups[choice - 1]
    print(f"\nSetting auto-connect to {group.replace('_', ' ')} servers...")
    output = run_nordvpn_command(f"nordvpn set autoconnect on {group}")
    if output:
        print(output)


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
        print("\nEnabling auto-connect to best server...")
        output = run_nordvpn_command("nordvpn set autoconnect on")
        if output:
            print(output)
        input("\nPress Enter to continue...")
    elif choice == 2:
        autoconnect_country()
        input("\nPress Enter to continue...")
    elif choice == 3:
        autoconnect_group()
        input("\nPress Enter to continue...")
    elif choice == 4:
        autoconnect_off()
        input("\nPress Enter to continue...")


def main_menu():
    """Display the main menu"""
    options = [
        "Quick Connect (best server)",
        "Connect to Country",
        "Connect to Server Group",
        "Auto-Connect Settings"
    ]
    
    while True:
        choice = display_menu("NordVPN Quick Connect", options, back_option=False)
        
        if choice == 0:
            print("\nExiting...")
            sys.exit(0)
        elif choice == 1:
            connect_quick()
            input("\nPress Enter to continue...")
        elif choice == 2:
            connect_country()
        elif choice == 3:
            connect_group()
        elif choice == 4:
            autoconnect_menu()


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
