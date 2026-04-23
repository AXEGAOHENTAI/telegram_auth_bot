#!/usr/bin/env python3
"""
Script for managing authorized bot users
"""

import os
import re
import sys
from dotenv import load_dotenv

# Set UTF-8 encoding for output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        # Fallback for older Python versions
        pass

def load_env():
    """Loads environment variables"""
    load_dotenv()
    return {
        'restrict_access': os.getenv('RESTRICT_ACCESS', 'True').lower() == 'true',
        'authorized_users': os.getenv('AUTHORIZED_USERS', '').split(',')
    }

def save_env(restrict_access, authorized_users):
    """Saves settings to .env file"""
    env_content = f"""# Telegram Steam Guard Bot Configuration
# Bot token
BOT_TOKEN={os.getenv('BOT_TOKEN', 'your_bot_token_here')}

# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL={os.getenv('LOG_LEVEL', 'INFO')}

# User authorization
# RESTRICT_ACCESS=True - only authorized users
# RESTRICT_ACCESS=False - access for all users
RESTRICT_ACCESS={str(restrict_access)}

# Authorized user IDs (comma-separated)
# Get ID from @userinfobot in Telegram
AUTHORIZED_USERS={','.join(authorized_users)}
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Settings saved to .env file")
        return True
    except Exception as e:
        print(f"❌ Error saving: {e}")
        return False

def add_user():
    """Adds a new user"""
    print("\n➕ Adding new user")
    print("-" * 30)
    
    user_id = input("Enter user ID: ").strip()
    
    if not user_id.isdigit():
        print("❌ ID must be a number!")
        return False
    
    config = load_env()
    users = [u.strip() for u in config['authorized_users'] if u.strip()]
    
    if user_id in users:
        print("⚠️ User already added!")
        return False
    
    users.append(user_id)
    
    if save_env(config['restrict_access'], users):
        print(f"✅ User {user_id} added")
        return True
    return False

def remove_user():
    """Removes a user"""
    print("\n➖ Removing user")
    print("-" * 30)
    
    config = load_env()
    users = [u.strip() for u in config['authorized_users'] if u.strip()]
    
    if not users:
        print("📝 List of authorized users is empty")
        return False
    
    print("Current users:")
    for i, user_id in enumerate(users, 1):
        print(f"{i}. {user_id}")
    
    try:
        choice = int(input("\nEnter user number to remove: ")) - 1
        if 0 <= choice < len(users):
            removed_user = users.pop(choice)
            if save_env(config['restrict_access'], users):
                print(f"✅ User {removed_user} removed")
                return True
        else:
            print("❌ Invalid number!")
    except ValueError:
        print("❌ Enter a number!")
    
    return False

def list_users():
    """Shows list of users"""
    print("\n👥 List of authorized users")
    print("-" * 40)
    
    config = load_env()
    users = [u.strip() for u in config['authorized_users'] if u.strip()]
    
    if not users:
        print("📝 List is empty")
    else:
        for i, user_id in enumerate(users, 1):
            print(f"{i}. {user_id}")
    
    print(f"\n🔒 Authorization mode: {'ENABLED' if config['restrict_access'] else 'DISABLED'}")

def toggle_restriction():
    """Toggles authorization mode"""
    print("\n🔒 Toggle authorization mode")
    print("-" * 40)
    
    config = load_env()
    current = config['restrict_access']
    
    print(f"Current mode: {'ENABLED' if current else 'DISABLED'}")
    
    if current:
        print("⚠️ WARNING: Disabling authorization will give access to ALL users!")
        response = input("Disable authorization? (y/n): ").lower()
        if response == 'y':
            new_mode = False
        else:
            print("❌ Operation cancelled")
            return False
    else:
        response = input("Enable authorization? (y/n): ").lower()
        if response == 'y':
            new_mode = True
        else:
            print("❌ Operation cancelled")
            return False
    
    users = [u.strip() for u in config['authorized_users'] if u.strip()]
    
    if save_env(new_mode, users):
        print(f"✅ Authorization mode {'ENABLED' if new_mode else 'DISABLED'}")
        return True
    return False

def main():
    """Main function"""
    print("👥 Managing authorized users")
    print("=" * 50)
    
    while True:
        print("\n📋 Available actions:")
        print("1. Show list of users")
        print("2. Add user")
        print("3. Remove user")
        print("4. Toggle authorization mode")
        print("5. Exit")
        
        choice = input("\nChoose action (1-5): ").strip()
        
        if choice == '1':
            list_users()
        elif choice == '2':
            add_user()
        elif choice == '3':
            remove_user()
        elif choice == '4':
            toggle_restriction()
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main() 