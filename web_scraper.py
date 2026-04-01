import requests
from bs4 import BeautifulSoup as bs
import os
from urllib.parse import urljoin, urlparse
import re
import tkinter as tk
from tkinter import filedialog, ttk, Button
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

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



