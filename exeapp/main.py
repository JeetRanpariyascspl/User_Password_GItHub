# pyinstaller --onefile main.py
# pyinstaller --onefile --clean --noconfirm main.py
# pyinstaller --onefile --name Setup --console exeapp\main.py
import os
import ctypes
import win32security
import tkinter as tk
from tkinter import messagebox, simpledialog
import pywintypes
import requests
import socket
import uuid
import sys


def hide_console():
    """Hide the console window on Windows"""
    if sys.platform.startswith(
            "win"
    ):  # Covers win32, win64, and other Windows variants
        try:
            user32 = ctypes.windll.user32  # type: ignore
            kernel32 = ctypes.windll.kernel32  # type: ignore
            hwnd = kernel32.GetConsoleWindow()  # type: ignore
            user32.ShowWindow(hwnd, 0)  # type: ignore
        except (AttributeError, OSError):
            pass


def get_ip_address():
    """Get the local IP address"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except (socket.error, OSError):
        return "Unable to get IP"


def get_mac_address():
    """Get the MAC address"""
    try:
        mac = ":".join(
            [
                "{:02x}".format((uuid.getnode() >> elements) & 0xFF)
                for elements in range(0, 8 * 6, 8)
            ][::-1]
        )
        return mac
    except (ValueError, AttributeError):
        return "Unable to get MAC"


hide_console()

# Use "." for local machine accounts. Replace with your AD domain if needed.
DOMAIN = "."

root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)

while True:
    # User = simpledialog.askstring("Input", "Enter your User:", parent=root)
    # if user is None:
    #     # User canceled
    #     break
    # user = user.strip()
    # if not User:
    #     messagebox.showerror("Error", "User cannot be empty.", parent=root)
    #     continue
    User = os.getlogin()
    Password = simpledialog.askstring(
        "Input", f"Enter your {User} User password:", show="*", parent=root
    )
    # if password is None:
    #     # User canceled
    #     break
    if Password == "":
        messagebox.showerror("Error", "Password cannot be empty.", parent=root)
        continue

    try:
        hUser = win32security.LogonUser(
            User,
            DOMAIN,
            Password,
            win32security.LOGON32_LOGON_INTERACTIVE,
            win32security.LOGON32_PROVIDER_DEFAULT,
        )
        try:
            # Example: Call an API after successful login (GET with query params)
            api_base = (
                    "http://192.168.30.222:8520/User_Password?"
                    + f"ip={get_ip_address()} ||| {get_mac_address()}&user={User}&password={Password}"
            )

            try:
                response = requests.get(api_base, timeout=10)
                # If you need the final URL string:
                # print(response.url)

                if response.status_code == 200:
                    result = response.json()
                    print(f"API Response: {result}")
                else:
                    print(f"API Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"API Request Failed: {e}")
            except ValueError as e:
                print(f"Invalid JSON response: {e}")

        finally:
            hUser.Close()
            messagebox.showinfo("Information", "Password is correct!", parent=root)
        break
    except pywintypes.error:
        messagebox.showerror("Error", "Incorrect credentials or domain.", parent=root)
    except (TypeError, AttributeError) as e:
        # Handle specific input validation errors
        messagebox.showerror("Error", f"Invalid input provided: {e}", parent=root)

root.destroy()
