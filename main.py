import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import json

BLOCKLIST_TXT = "blocklist.txt"
BLOCKLIST_JSON = "blocklist.json"

# Function to load blocklist
def load_blocklist():
    try:
        with open(BLOCKLIST_TXT, "r") as file:
            return set(line.strip() for line in file.readlines())
    except FileNotFoundError:
        return set()

# Function to save blocklist
def save_blocklist(blocklist):
    with open(BLOCKLIST_TXT, "w") as file:
        for domain in sorted(blocklist):
            file.write(domain + "\n")
    with open(BLOCKLIST_JSON, "w") as json_file:
        json.dump({"blocked_sites": sorted(blocklist)}, json_file, indent=4)
    messagebox.showinfo("Saved", "Blocklist saved successfully!")

# Function to run update_blocklist.py
def update_blocklist():
    try:
        subprocess.run(["python", "update_blocklist.py"], check=True)
        messagebox.showinfo("Update", "Blocklist updated successfully!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to update blocklist!")

# Function to add domain or IP
def add_domain():
    domain = entry.get().strip()
    if domain and domain not in blocklist:
        blocklist.add(domain)
        listbox.insert(tk.END, domain)
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Domain already in blocklist or invalid!")

# Function to remove selected domain
def remove_selected():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "No domain selected!")
        return
    for index in reversed(selected):
        domain = listbox.get(index)
        blocklist.remove(domain)
        listbox.delete(index)

# Function to refresh listbox
def refresh_listbox():
    listbox.delete(0, tk.END)
    for domain in sorted(blocklist):
        listbox.insert(tk.END, domain)

# GUI Setup
root = tk.Tk()
root.title("Blocklist Manager")
root.geometry("500x500")

frame = tk.Frame(root)
frame.pack(pady=10)

entry = tk.Entry(frame, width=30)
entry.pack(side=tk.LEFT, padx=5)

tk.Button(frame, text="Add", command=add_domain).pack(side=tk.LEFT)

tk.Button(root, text="Remove Selected", command=remove_selected).pack(pady=5)

tk.Button(root, text="Update Blocklist", command=update_blocklist).pack(pady=5)

listbox = tk.Listbox(root, width=60, height=15)
listbox.pack(pady=10)

tk.Button(root, text="Save Changes", command=lambda: save_blocklist(blocklist)).pack(pady=5)

# Load blocklist into listbox
blocklist = load_blocklist()
refresh_listbox()

root.mainloop()
