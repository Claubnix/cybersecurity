import os
import struct
import hashlib
import time
import customtkinter as ctk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# -----------------------
# Crypto helpers
# -----------------------
MAGIC = b"CS1\x00"
VERSION = 1
ALGO_AESGCM = b"AESGCM"  # 6 bytes

SALT_LEN = 16
NONCE_LEN = 12
KEY_LEN = 32  # AES-256
SCRYPT_N = 2**15
SCRYPT_R = 8
SCRYPT_P = 1

ALGO_AESGCM = b"AESGCM"   # 6 bytes
ALGO_CHACHA = b"CHC20P"   # 6 bytes (ChaCha20-Poly1305)


def derive_key(password: str, salt: bytes) -> bytes:
    if not password:
        raise ValueError("Passwort darf nicht leer sein.")
    kdf = Scrypt(
        salt=salt,
        length=KEY_LEN,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
    )
    return kdf.derive(password.encode("utf-8"))

def fmt_bytes(n: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    x = float(n)
    for u in units:
        if x < 1024 or u == units[-1]:
            return f"{x:.2f} {u}" if u != "B" else f"{int(x)} {u}"
        x /= 1024
    return f"{n} B"


def encrypt_file(in_path: str, out_path: str, password: str, algo_choice: str) -> None:
    with open(in_path, "rb") as f:
        plaintext = f.read()

    salt = os.urandom(SALT_LEN)
    nonce = os.urandom(NONCE_LEN)
    key = derive_key(password, salt)

    if algo_choice == "AES-GCM (empfohlen)":
        algo_id = ALGO_AESGCM
        aead = AESGCM(key)
    elif algo_choice == "ChaCha20-Poly1305":
        algo_id = ALGO_CHACHA
        aead = ChaCha20Poly1305(key)
    else:
        raise ValueError("Unbekanntes Verfahren.")

    header = MAGIC + struct.pack(">B", VERSION) + algo_id + salt + nonce
    ciphertext = aead.encrypt(nonce, plaintext, header)

    with open(out_path, "wb") as f:
        f.write(header)
        f.write(ciphertext)


def decrypt_file(in_path: str, out_path: str, password: str) -> None:
    with open(in_path, "rb") as f:
        data = f.read()

    min_len = len(MAGIC) + 1 + 6 + SALT_LEN + NONCE_LEN + 16
    if len(data) < min_len:
        raise ValueError("Datei ist zu klein oder kein gültiges Format.")

    off = 0
    magic = data[off:off+4]; off += 4
    if magic != MAGIC:
        raise ValueError("Ungültige Datei (Magic passt nicht).")

    version = data[off]; off += 1
    if version != VERSION:
        raise ValueError(f"Nicht unterstützte Version: {version}")

    algo = data[off:off+6]; off += 6
    salt = data[off:off+SALT_LEN]; off += SALT_LEN
    nonce = data[off:off+NONCE_LEN]; off += NONCE_LEN
    header = data[:off]
    ciphertext = data[off:]

    key = derive_key(password, salt)

    if algo == ALGO_AESGCM:
        aead = AESGCM(key)
    elif algo == ALGO_CHACHA:
        aead = ChaCha20Poly1305(key)
    else:
        raise ValueError("Nicht unterstützter Algorithmus in Datei.")

    plaintext = aead.decrypt(nonce, ciphertext, header)

    with open(out_path, "wb") as f:
        f.write(plaintext)


def file_hash(path: str, algo: str) -> str:
    h = hashlib.sha256() if algo == "SHA-256" else hashlib.sha512()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def caesar(text: str, shift: int) -> str:
    # Simple Caesar for letters only; keep others unchanged
    out = []
    for ch in text:
        if "a" <= ch <= "z":
            out.append(chr((ord(ch) - 97 + shift) % 26 + 97))
        elif "A" <= ch <= "Z":
            out.append(chr((ord(ch) - 65 + shift) % 26 + 65))
        else:
            out.append(ch)
    return "".join(out)

# -----------------------
# UI
# -----------------------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class CryptoSuiteApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CryptoSuite (CustomTkinter)")
        self.geometry("900x560")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        tab = ctk.CTkTabview(self)
        tab.grid(row=0, column=0, sticky="nsew", padx=14, pady=14)

        self.tab_encrypt = tab.add("Datei schützen")
        self.tab_hash = tab.add("Hash & Verify")
        self.tab_classic = tab.add("Classic (Lernmodus)")

        self._build_encrypt_tab()
        self._build_hash_tab()
        self._build_classic_tab()

# ---- Tab 1: Encrypt/Decrypt ----
    def _build_encrypt_tab(self):
        t = self.tab_encrypt
        t.grid_columnconfigure(1, weight=1)

        self.in_path_var = ctk.StringVar(value="")
        self.out_path_var = ctk.StringVar(value="")
        self.pass_var = ctk.StringVar(value="")

        ctk.CTkLabel(t, text="Eingabedatei:").grid(row=0, column=0, sticky="w", padx=12, pady=(12,6))
        ctk.CTkEntry(t, textvariable=self.in_path_var).grid(row=0, column=1, sticky="ew", padx=12, pady=(12,6))
        ctk.CTkButton(t, text="Wählen…", command=self.pick_input_file).grid(row=0, column=2, padx=12, pady=(12,6))

        ctk.CTkLabel(t, text="Ausgabedatei:").grid(row=1, column=0, sticky="w", padx=12, pady=6)
        ctk.CTkEntry(t, textvariable=self.out_path_var).grid(row=1, column=1, sticky="ew", padx=12, pady=6)
        ctk.CTkButton(t, text="Speichern als…", command=self.pick_output_file).grid(row=1, column=2, padx=12, pady=6)

        ctk.CTkLabel(t, text="Passwort:").grid(row=2, column=0, sticky="w", padx=12, pady=6)
        ctk.CTkEntry(t, textvariable=self.pass_var, show="•").grid(row=2, column=1, sticky="ew", padx=12, pady=6)

        self.mode_var = ctk.StringVar(value="AES-GCM (empfohlen)")
        ctk.CTkLabel(t, text="Verfahren:").grid(row=3, column=0, sticky="w", padx=12, pady=6)
        ctk.CTkOptionMenu(
            t,
            values=["AES-GCM (empfohlen)", "ChaCha20-Poly1305"],
            variable=self.mode_var
        ).grid(row=3, column=1, sticky="w", padx=12, pady=6)

        btn_frame = ctk.CTkFrame(t)
        btn_frame.grid(row=4, column=0, columnspan=3, sticky="ew", padx=12, pady=(12,6))
        btn_frame.grid_columnconfigure((0,1), weight=1)

        ctk.CTkButton(btn_frame, text="Encrypt", command=self.do_encrypt).grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        ctk.CTkButton(btn_frame, text="Decrypt", command=self.do_decrypt).grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        # ✅ Benchmark label in separate row
        self.bench_var = ctk.StringVar(value="Benchmark: –")
        ctk.CTkLabel(
            t,
            textvariable=self.bench_var,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#0a5"
        ).grid(
            row=5, column=0, columnspan=3, sticky="w", padx=12, pady=(4, 6)
        )


        self.status_box = ctk.CTkTextbox(t, height=240)
        self.status_box.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=12, pady=(6,12))
        t.grid_rowconfigure(6, weight=1)

        self._log("Bereit. Tipp: Für Demo eine kleine Datei nehmen und Encrypt → Decrypt zeigen.\n")


    def _log(self, msg: str):
        self.status_box.insert("end", msg + "\n")
        self.status_box.see("end")

    def pick_input_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.in_path_var.set(path)
            # Default output suggestion
            self.out_path_var.set(path + ".cs1")

    def pick_output_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".cs1")
        if path:
            self.out_path_var.set(path)

    def do_encrypt(self):
        in_path = self.in_path_var.get().strip()
        out_path = self.out_path_var.get().strip()
        password = self.pass_var.get()
        algo = self.mode_var.get()

        if not password:
            messagebox.showwarning(
                "Passwort fehlt",
                "Bitte ein Passwort eingeben."
            )
            return

        try:
            if not in_path or not os.path.isfile(in_path):
                raise ValueError("Bitte eine gültige Eingabedatei wählen.")
            if not out_path:
                raise ValueError("Bitte eine Ausgabedatei festlegen.")

            in_size = os.path.getsize(in_path)

            t0 = time.perf_counter()
            encrypt_file(in_path, out_path, password, algo)
            t1 = time.perf_counter()

            out_size = os.path.getsize(out_path) if os.path.exists(out_path) else 0
            ms = (t1 - t0) * 1000.0

            self.bench_var.set(
                f"Benchmark: Encrypt | {algo} | {fmt_bytes(in_size)} → {fmt_bytes(out_size)} | {ms:.1f} ms"
            )

            self._log(f"[OK] Verschlüsselt: {in_path}")
            self._log(f"     → {out_path}\n")

        except Exception as e:
            messagebox.showerror("Encrypt fehlgeschlagen", str(e))
            self._log(f"[FEHLER] {e}\n")
            self.bench_var.set("Benchmark: –")


    def do_decrypt(self):
        in_path = self.in_path_var.get().strip()
        out_path = self.out_path_var.get().strip()
        password = self.pass_var.get()

        try:
            if not in_path or not os.path.isfile(in_path):
                raise ValueError("Bitte eine gültige Eingabedatei wählen.")
            if not out_path:
                raise ValueError("Bitte eine Ausgabedatei festlegen.")

            in_size = os.path.getsize(in_path)

            t0 = time.perf_counter()
            decrypt_file(in_path, out_path, password)
            t1 = time.perf_counter()

            out_size = os.path.getsize(out_path) if os.path.exists(out_path) else 0
            ms = (t1 - t0) * 1000.0

            # Algo aus Header lesen (für Anzeige)
            with open(in_path, "rb") as f:
                header = f.read(4 + 1 + 6)
            algo_id = header[5:11]
            algo_name = "AES-GCM" if algo_id == ALGO_AESGCM else ("ChaCha20-Poly1305" if algo_id == ALGO_CHACHA else "Unknown")

            self.bench_var.set(
                f"Benchmark: Decrypt | {algo_name} | {fmt_bytes(in_size)} → {fmt_bytes(out_size)} | {ms:.1f} ms"
            )

            self._log(f"[OK] Entschlüsselt: {in_path}")
            self._log(f"     → {out_path}\n")

        except Exception as e:
            messagebox.showerror("Decrypt fehlgeschlagen", str(e))
            self._log(f"[FEHLER] {e}\n")
            self.bench_var.set("Benchmark: –")


    # ---- Tab 2: Hash & Verify ----
    def _build_hash_tab(self):
        t = self.tab_hash
        t.grid_columnconfigure(1, weight=1)

        self.hash_path_var = ctk.StringVar(value="")
        self.hash_algo_var = ctk.StringVar(value="SHA-256")
        self.hash_out_var = ctk.StringVar(value="")
        self.hash_verify_var = ctk.StringVar(value="")

        ctk.CTkLabel(t, text="Datei:").grid(row=0, column=0, sticky="w", padx=12, pady=(12,6))
        ctk.CTkEntry(t, textvariable=self.hash_path_var).grid(row=0, column=1, sticky="ew", padx=12, pady=(12,6))
        ctk.CTkButton(t, text="Wählen…", command=self.pick_hash_file).grid(row=0, column=2, padx=12, pady=(12,6))

        ctk.CTkLabel(t, text="Hash:").grid(row=1, column=0, sticky="w", padx=12, pady=6)
        ctk.CTkOptionMenu(t, values=["SHA-256", "SHA-512"], variable=self.hash_algo_var).grid(row=1, column=1, sticky="w", padx=12, pady=6)

        ctk.CTkButton(t, text="Berechnen", command=self.do_hash).grid(row=2, column=0, padx=12, pady=(12,6), sticky="w")

        ctk.CTkLabel(t, text="Resultat:").grid(row=3, column=0, sticky="w", padx=12, pady=6)
        ctk.CTkEntry(t, textvariable=self.hash_out_var).grid(row=3, column=1, sticky="ew", padx=12, pady=6)
        ctk.CTkButton(t, text="Copy", command=self.copy_hash).grid(row=3, column=2, padx=12, pady=6)

        ctk.CTkLabel(t, text="Verify (erwarteter Hash):").grid(row=4, column=0, sticky="w", padx=12, pady=(16,6))
        ctk.CTkEntry(t, textvariable=self.hash_verify_var).grid(row=4, column=1, sticky="ew", padx=12, pady=(16,6))
        ctk.CTkButton(t, text="Prüfen", command=self.do_verify).grid(row=4, column=2, padx=12, pady=(16,6))

        self.hash_status = ctk.CTkLabel(t, text="")
        self.hash_status.grid(row=5, column=0, columnspan=3, sticky="w", padx=12, pady=(10,12))

    def pick_hash_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.hash_path_var.set(path)

    def do_hash(self):
        try:
            path = self.hash_path_var.get().strip()
            if not path or not os.path.isfile(path):
                raise ValueError("Bitte eine gültige Datei wählen.")
            algo = self.hash_algo_var.get()
            h = file_hash(path, algo)
            self.hash_out_var.set(h)
            self.hash_status.configure(text=f"[OK] {algo} berechnet.")
        except Exception as e:
            messagebox.showerror("Hash fehlgeschlagen", str(e))
            self.hash_status.configure(text=f"[FEHLER] {e}")

    def copy_hash(self):
        h = self.hash_out_var.get()
        if h:
            self.clipboard_clear()
            self.clipboard_append(h)
            self.hash_status.configure(text="[OK] Hash kopiert.")

    def do_verify(self):
        try:
            current = self.hash_out_var.get().strip().lower()
            expected = self.hash_verify_var.get().strip().lower()
            if not current:
                raise ValueError("Bitte zuerst einen Hash berechnen.")
            if not expected:
                raise ValueError("Bitte erwarteten Hash einfügen.")
            if current == expected:
                self.hash_status.configure(text="[OK] Hash stimmt überein (Datei unverändert).")
            else:
                self.hash_status.configure(text="[WARN] Hash stimmt NICHT überein (Datei verändert / falsche Datei).")
        except Exception as e:
            messagebox.showerror("Verify fehlgeschlagen", str(e))
            self.hash_status.configure(text=f"[FEHLER] {e}")

    # ---- Tab 3: Classic (Lernmodus) ----
    def _build_classic_tab(self):
        t = self.tab_classic
        t.grid_columnconfigure(0, weight=1)
        t.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            t,
            text="Classic Cipher (Lernmodus)\nHinweis: Caesar ist kryptografisch UNSICHER und dient nur zur Demonstration.",
            justify="left"
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(12,6))

        top = ctk.CTkFrame(t)
        top.grid(row=1, column=0, sticky="ew", padx=12, pady=6)
        top.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(top, text="Shift:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.shift_var = ctk.IntVar(value=3)
        ctk.CTkEntry(top, textvariable=self.shift_var, width=80).grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkButton(top, text="Encrypt", command=self.do_caesar_encrypt).grid(row=0, column=2, padx=10, pady=10)
        ctk.CTkButton(top, text="Decrypt", command=self.do_caesar_decrypt).grid(row=0, column=3, padx=10, pady=10, sticky="w")

        self.classic_text = ctk.CTkTextbox(t)
        self.classic_text.grid(row=2, column=0, sticky="nsew", padx=12, pady=(6,12))
        self.classic_text.insert("end", "Beispieltext…")

    def do_caesar_encrypt(self):
        try:
            s = int(self.shift_var.get())
            text = self.classic_text.get("1.0", "end-1c")
            self.classic_text.delete("1.0", "end")
            self.classic_text.insert("end", caesar(text, s))
        except Exception as e:
            messagebox.showerror("Caesar Encrypt fehlgeschlagen", str(e))

    def do_caesar_decrypt(self):
        try:
            s = int(self.shift_var.get())
            text = self.classic_text.get("1.0", "end-1c")
            self.classic_text.delete("1.0", "end")
            self.classic_text.insert("end", caesar(text, -s))
        except Exception as e:
            messagebox.showerror("Caesar Decrypt fehlgeschlagen", str(e))


if __name__ == "__main__":
    app = CryptoSuiteApp()
    app.mainloop()
