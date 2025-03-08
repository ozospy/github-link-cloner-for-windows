import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def choose_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        directory_var.set(folder_selected)

def clone_repo():
    repo_url = url_var.get().strip()
    save_path = directory_var.get().strip()

    if not repo_url:
        messagebox.showwarning("Uyarı", "Lütfen bir GitHub URL'si girin!")
        return

    if not save_path:
        messagebox.showwarning("Uyarı", "Lütfen bir klasör seçin!")
        return

    output_text.delete(1.0, tk.END)  # Önceki çıktıyı temizle
    output_text.insert(tk.END, f"🔄 Klonlama başlıyor...\n📁 Kayıt yeri: {save_path}\n\n")

    try:
        process = subprocess.Popen(
            ["git", "clone", repo_url],
            cwd=save_path,  # Depoyu bu klasöre klonlar
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in process.stdout:
            output_text.insert(tk.END, line)  # Terminal çıktısını göster
            output_text.see(tk.END)  # Otomatik olarak aşağı kaydır

        process.wait()  # İşlemin tamamlanmasını bekle

        if process.returncode == 0:
            messagebox.showinfo("Başarılı", "Depo başarıyla klonlandı!")
        else:
            messagebox.showerror("Hata", "Klonlama başarısız oldu!")
    
    except Exception as e:
        messagebox.showerror("Hata", f"Beklenmedik hata: {str(e)}")

# Tkinter GUI oluşturma
root = tk.Tk()
root.title("GitHub Klonlayıcı")
root.geometry("500x400")

url_var = tk.StringVar()
directory_var = tk.StringVar()

tk.Label(root, text="GitHub Depo URL'si:").pack(pady=5)
tk.Entry(root, textvariable=url_var, width=50).pack(pady=5)

tk.Label(root, text="Kaydetme Konumu:").pack(pady=5)
tk.Entry(root, textvariable=directory_var, width=40).pack(pady=5)
tk.Button(root, text="Klasör Seç", command=choose_directory).pack(pady=2)

tk.Button(root, text="Klonla", command=clone_repo).pack(pady=10)

output_text = scrolledtext.ScrolledText(root, width=60, height=10)
output_text.pack(pady=5)

root.mainloop()