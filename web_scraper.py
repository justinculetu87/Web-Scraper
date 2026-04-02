import requests
from bs4 import BeautifulSoup as bs
import os
from urllib.parse import urljoin, urlparse
import re
import tkinter as tk
from tkinter import filedialog, ttk, Button, scrolledtext
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar
import threading

#assigning globals
root = tk.Tk()
root.title("Hyperlink Download")
root.geometry("620x520")
root.resizable(False, False)
url_var = tk.StringVar()
folder_var = tk.StringVar()
output: ScrolledText = None
btn: Button = None
progress: Progressbar = None

#begin functions
def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)

def log(msg):
    output.config(state="normal")
    output.insert(tk.END, msg + "\n")
    output.see(tk.END)
    output.config(state="disabled")

def download_start():
    url = url_var.get().strip()
    folder = folder_var.get().strip()

    if not url:
        log("Enter a URL: ")
        return
    
    if not folder:
        log("Select a download location folder: ")
        return
    
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    btn.config(state="disabled")
    progress.start()
    threading.Thread(target=run_scraper, args=(url, folder), daemon=True).start()


def run_scraper(url, folder):
    try:
        os.makedirs(folder, exist_ok=True)
        log(f"Getting: {url}")
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = bs(response.text, "html.parser")
        links = soup.find_all("a", href=True)
        log(f"Found {len(links)} hyperlinks.\n")

        downloaded, skipped = 0, 0

        for link in links:
            href = link["href"]
            url = urljoin(url, href)

            if not url.startswith(("http://", "https://")):
                skipped += 1
                continue

            path = urlparse(url).path

            filename = os.path.basename(path) or re.sub(r'\W+', '_', url)[:50]
            filepath = os.path.join(folder, filename)

            try:
                log(f"Downloading: {url}")
                file_data = requests.get(url, headers=headers, timeout=10)
                file_data.raise_for_status()
                with open(filepath, "wb") as f:
                    f.write(file_data.content)
                downloaded += 1
            except Exception as e:
                log(f'Failed: {e}')
                skipped += 1

        log(f"\n Downloaded: {downloaded} | Skipped: {skipped}")
        log(f"\n Saved to: {os.path.abspath(folder)}")

    except Exception as e:
        log(f"Error on downloading: {e}")
    finally:
        progress.stop()
        btn.config(state="normal") 


##Build app page
root = tk.Tk()
root.title("Hyperlink Download")
root.geometry("620x520")
root.resizable(False, False)

pad = {"padx": 10, "pady": 5}

tk.Label(root, text ="URL to scrape:").grid(row=0, column=0, sticky="w", **pad)
url_var = tk.StringVar()
tk.Entry(root, textvariable=url_var, width=60).grid(row=0, column=1, columnspan=2, **pad)

tk.Label(root, text="Download Folder:").grid(row=1, column=0, sticky="w", **pad)
folder_var = tk.StringVar()
tk.Entry(root, textvariable=folder_var, width=45).grid(row=1, column=1, **pad)
tk.Button(root, text="Browse", command=browse_folder).grid(row=1, column=2, **pad)

btn = tk.Button(root, text="Start Download", command=download_start,
                bg="#2563eb", fg="red", font=("Comic Sans", 11, "bold"), padx=10, pady=5)
btn.grid(row=3, column=0, columnspan=3, pady=10)

output = scrolledtext.ScrolledText(root, height=18, state="disabled", bg="#1e1e1e",
                                   fg="#d4d4d4", font=("Comic Sans", 9))

output.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()