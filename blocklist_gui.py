import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import json
import os

BLOCKLIST_TXT = "blocklist.txt"
BLOCKLIST_JSON = "blocklist.json"

def load_blocklist():
    blocklist = set()
    try:
        with open(BLOCKLIST_TXT, "r", encoding="utf-8") as file:
            blocklist.update(line.strip() for line in file.readlines())
    except FileNotFoundError:
        pass

    return blocklist

def save_blocklist(blocklist):
    try:
        with open(TXT_FILE, "r", encoding="utf-8") as f:
            txt_entries = set(f.read().splitlines())
    except FileNotFoundError:
        txt_entries = set()
    except UnicodeDecodeError:
        print("⚠️ Warning: blocklist.txt contains unreadable characters. File will be skipped.")
        txt_entries = set()

    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            json_entries = set(data.get("blocked_sites", []))
    except (FileNotFoundError, json.JSONDecodeError):
        json_entries = set()

    return txt_entries.union(json_entries)

def update_blocklist():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "update_blocklist.py")
        subprocess.run(["python", script_path], check=True)
        messagebox.showinfo("Update", "Blocklist updated successfully!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to update blocklist!")

def add_domain():
    domain = entry.get().strip()
    if domain and domain not in blocklist:
        blocklist.add(domain)
        refresh_listbox()
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Domain already in blocklist or invalid!")

def remove_selected():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "No domain selected!")
        return
    for index in reversed(selected):
        domain = listbox.get(index)
        blocklist.remove(domain)
        listbox.delete(index)

def refresh_listbox():
    listbox.delete(0, tk.END)
    search_query = search_entry.get().strip().lower()
    for domain in sorted(blocklist):
        if search_query in domain.lower():  # Filter by search
            listbox.insert(tk.END, domain)

# GUI Setup
root = tk.Tk()
root.title("Blocklist Manager")
root.geometry("600x500")

root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)

# Input & Add Button
frame = tk.Frame(root)
frame.grid(row=0, column=0, pady=5, padx=5, sticky="ew")
frame.columnconfigure(0, weight=1)

entry = tk.Entry(frame)
entry.grid(row=0, column=0, sticky="ew", padx=5)
tk.Button(frame, text="Add", command=add_domain).grid(row=0, column=1, padx=5)

# Search Bar
search_frame = tk.Frame(root)
search_frame.grid(row=1, column=0, pady=5, padx=5, sticky="ew")
search_frame.columnconfigure(0, weight=1)

search_entry = tk.Entry(search_frame)
search_entry.grid(row=0, column=0, sticky="ew", padx=5)
search_entry.bind("<KeyRelease>", lambda event: refresh_listbox())  # Dynamische filtering
tk.Label(search_frame, text="🔍 Search:").grid(row=0, column=1, padx=5)

# Listbox with Scrollbar
list_frame = tk.Frame(root)
list_frame.grid(row=2, column=0, pady=5, padx=5, sticky="nsew")
list_frame.rowconfigure(0, weight=1)
list_frame.columnconfigure(0, weight=1)

listbox = tk.Listbox(list_frame)
listbox.grid(row=0, column=0, sticky="nsew")

scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
listbox.config(yscrollcommand=scrollbar.set)

# Buttons
button_frame = tk.Frame(root)
button_frame.grid(row=3, column=0, pady=5, padx=5, sticky="ew")
button_frame.columnconfigure([0, 1, 2], weight=1)

tk.Button(button_frame, text="Remove Selected", command=remove_selected).grid(row=0, column=0, padx=5, sticky="ew")
tk.Button(button_frame, text="Update Blocklist", command=update_blocklist).grid(row=0, column=1, padx=5, sticky="ew")
tk.Button(button_frame, text="Save Changes", command=lambda: save_blocklist(blocklist)).grid(row=0, column=2, padx=5, sticky="ew")


# Load blocklist into listbox
blocklist = load_blocklist()
refresh_listbox()

root.mainloop()
