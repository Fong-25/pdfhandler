import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PyPDF2 import PdfReader, PdfWriter

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === CORE FUNCTIONS ===

def split_pdf(path):
    reader = PdfReader(path)
    filename = os.path.basename(path)
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        out_path = os.path.join(OUTPUT_DIR, f"{filename}_page_{i+1}.pdf")
        with open(out_path, "wb") as f:
            writer.write(f)
    messagebox.showinfo("Done", f"Split into {len(reader.pages)} pages.")

def merge_pdfs(paths):
    writer = PdfWriter()
    for path in paths:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    output_path = os.path.join(OUTPUT_DIR, "merged_output.pdf")
    with open(output_path, "wb") as f:
        writer.write(f)
    messagebox.showinfo("Done", "PDFs merged successfully.")

def extract_pages(path):
    reader = PdfReader(path)
    total_pages = len(reader.pages)
    pages_input = simpledialog.askstring("Extract Pages", f"Enter page numbers (1–{total_pages}, comma-separated):")
    if not pages_input:
        return
    try:
        page_nums = [int(p.strip()) - 1 for p in pages_input.split(',') if p.strip().isdigit()]
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid page numbers.")
        return

    writer = PdfWriter()
    for p in page_nums:
        if 0 <= p < total_pages:
            writer.add_page(reader.pages[p])

    filename = os.path.basename(path)
    out_path = os.path.join(OUTPUT_DIR, f"{filename}_extracted.pdf")
    with open(out_path, "wb") as f:
        writer.write(f)
    messagebox.showinfo("Done", "Pages extracted successfully.")

# === GUI SETUP ===

def select_and_split():
    file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file:
        split_pdf(file)

def select_and_merge():
    files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if files:
        merge_pdfs(files)

def select_and_extract():
    file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file:
        extract_pages(file)

# === MAIN WINDOW ===

root = tk.Tk()
root.title("PDF Toolkit")
root.geometry("300x200")

tk.Label(root, text="PDF Toolkit", font=("Helvetica", 16)).pack(pady=10)

tk.Button(root, text="Split PDF", width=20, command=select_and_split).pack(pady=5)
tk.Button(root, text="Merge PDFs", width=20, command=select_and_merge).pack(pady=5)
tk.Button(root, text="Extract Pages", width=20, command=select_and_extract).pack(pady=5)

tk.Label(root, text="Output folder: /output", fg="gray").pack(pady=10)

root.mainloop()
