"""
User management CLI tool.

Usage:
    python manage_users.py add <username> <password>
    python manage_users.py list
    python manage_users.py deactivate <username>

Examples:
    python manage_users.py add police 123 
    python manage_users.py add rahi 5096
    python manage_users.py list
    python manage_users.py deactivate police123
"""

import sys
from user import create_user, list_users, deactivate_user

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) != 4:
            print("Usage: python manage_users.py add <username> <password>")
            return
        create_user(sys.argv[2], sys.argv[3])

    elif command == "list":
        rows = list_users()
        if not rows:
            print("No users found.")
            return
        print(f"\n{'ID':<5} {'Username':<20} {'Active':<8} {'Created At'}")
        print("-" * 60)
        for row in rows:
            status = "✅ Yes" if row["is_active"] else "❌ No"
            print(f"{row['id']:<5} {row['username']:<20} {status:<8} {row['created_at']}")

    elif command == "deactivate":
        if len(sys.argv) != 3:
            print("Usage: python manage_users.py deactivate <username>")
            return
        deactivate_user(sys.argv[2])
        print(f"✅ User '{sys.argv[2]}' deactivated.")

    else:
        print(f"Unknown command: {command}")
        print(__doc__)

if __name__ == "__main__":
    main()