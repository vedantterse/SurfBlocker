from pathlib import Path
import sys
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import tkinter as tk
from tkinter import messagebox
import os
import ctypes
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except AttributeError:
        # _MEIPASS is not available, use the local path
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

EXCLUDED_SITES = [
    "192.168.0.102 host.docker.internal",
    "192.168.0.102 gateway.docker.internal",
    "127.0.0.1 host.docker.internal"
]
def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def run_as_admin():
    """Re-run the script with administrative privileges if not already running as admin."""
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
        sys.exit()

run_as_admin()
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Tkinter-Designer\build\assets\frame0")

from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Toplevel, messagebox
import os
import ctypes

# Define the function to modify the hosts file
def show_messagebox(type, title, message):
    """Helper function to show message boxes in the foreground."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    root.attributes("-topmost", True)

    if type == "info":
        messagebox.showinfo(title, message, parent=root)
    elif type == "warning":
        messagebox.showwarning(title, message, parent=root)
    elif type == "error":
        messagebox.showerror(title, message, parent=root)

    root.destroy()  # Destroy the root window


def modify_hosts(action, website):
    if not website:
        show_messagebox("warning", "Input Error", "Please enter a website.")
        return

    hosts_path = r"C:\Windows\System32\drivers\etc\hosts" if os.name == 'nt' else "/etc/hosts"

    try:
        with open(hosts_path, 'r') as file:
            lines = file.readlines()

        with open(hosts_path, 'w') as file:
            for line in lines:
                if action == "add" and line.strip().startswith("127.0.0.1") and website in line:
                    continue
                elif action == "remove" and line.strip().startswith("127.0.0.1") and website in line:
                    continue
                file.write(line)

            if action == "add":
                file.write(f"127.0.0.1 {website}\n")
                show_messagebox("info", "Success", f"{website} has been blocked.")
            elif action == "remove":
                show_messagebox("info", "Success", f"{website} has been unblocked.")
    except PermissionError:
        show_messagebox("error", "Permission Error", "You need to run this script as an administrator.")
    except Exception as e:
        show_messagebox("error", "Error", str(e))

# Function to create the popup window for blocking a site
def block_site_window():
    def on_block_button_click():
        site = site_entry.get().strip()
        if site:
            modify_hosts("add", site)
            site_entry.delete(0, tk.END)  # Clear the text box after blocking

    # Create a new window
    block_window = Toplevel()
    block_window.title("Block Site")
    block_window.attributes('-topmost', True)

    tk.Label(block_window, text="Enter the website to block:").pack(pady=10)
    site_entry = tk.Entry(block_window, width=50)
    site_entry.pack(pady=5)

    block_button = tk.Button(block_window, text="Block Site", command=on_block_button_click)
    block_button.pack(pady=10)

    # Center the window on the screen
    block_window.update_idletasks()  # Update "requested size" from geometry manager
    width, height = block_window.winfo_width(), block_window.winfo_height()
    screen_width, screen_height = block_window.winfo_screenwidth(), block_window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    block_window.geometry(f'{width}x{height}+{x}+{y}')



def view_blocked_sites():
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts" if os.name == 'nt' else "/etc/hosts"
    blocked_sites = []

    try:
        with open(hosts_path, 'r') as file:
            for line in file:
                if line.strip().startswith("127.0.0.1") and line.strip() not in EXCLUDED_SITES:
                    site = line.strip().split(" ")[1]
                    blocked_sites.append(site)
        return blocked_sites
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return []

# Function to create the popup window for removing a blocked site
def remove_site_window():
    def on_remove_button_click():
        selected_site = site_listbox.get(tk.ACTIVE)
        if selected_site:
            modify_hosts("remove", selected_site)
            site_listbox.delete(tk.ACTIVE)  # Remove the site from the listbox

    # Create a new window
    remove_window = Toplevel()
    remove_window.title("Remove Blocked Site")
    remove_window.attributes('-topmost', True)

    tk.Label(remove_window, text="Select the website to unblock:").pack(pady=10)

    site_listbox = tk.Listbox(remove_window, width=50)
    site_listbox.pack(pady=5)

    blocked_sites = view_blocked_sites()
    for site in blocked_sites:
        site_listbox.insert(tk.END, site)

    remove_button = tk.Button(remove_window, text="Unblock Site", command=on_remove_button_click)
    remove_button.pack(pady=10)

    # Center the window on the screen
    remove_window.update_idletasks()  # Update "requested size" from geometry manager
    width, height = remove_window.winfo_width(), remove_window.winfo_height()
    screen_width, screen_height = remove_window.winfo_screenwidth(), remove_window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    remove_window.geometry(f'{width}x{height}+{x}+{y}')
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.title("SITE-BLOCKER (BETA-1.1)")

window.geometry("676x434")
window.configure(bg = "#F7F7F7")



canvas = Canvas(
    window,
    bg="#F7F7F7",
    height=434,
    width=676,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Load images using resource_path
image_image_1 = PhotoImage(file=resource_path("assets\\frame0\\image_1.png"))
canvas.create_image(
    338.0,
    217.0,
    image=image_image_1
)

image_image_2 = PhotoImage(file=resource_path("assets\\frame0\\image_2.png"))
canvas.create_image(
    159.0,
    207.999993003717,
    image=image_image_2
)

button_image_1 = PhotoImage(file=resource_path("assets\\frame0\\button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: block_site_window(),
    relief="flat"
)
button_1.place(
    x=34.0,
    y=165.0,
    width=249.66305541992188,
    height=80.0
)

image_image_3 = PhotoImage(file=resource_path("assets\\frame0\\image_3.png"))
canvas.create_image(
    507.0,
    207.999993003717,
    image=image_image_3
)

button_image_2 = PhotoImage(file=resource_path("assets\\frame0\\button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: remove_site_window(),
    relief="flat"
)
button_2.place(
    x=377.0,
    y=164.0,
    width=259.0,
    height=80.90230560302734
)

canvas.create_text(
    1.0,
    402.0,
    anchor="nw",
    text="cc@vedantterse",
    fill="#000000",
    font=("Megrim", 20 * -1)
)

window.resizable(False, False)
window.mainloop()