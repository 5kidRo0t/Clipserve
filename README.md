# 🔐 Clipserve – Now with Encrypted Clipboard History! ✨

---

<p align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTRwYm1wNnltb21hZm5ncHExN240dHQ1cGozM2NxcnVoOW8zeDNoZSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/ZTUfoXigKRpCM/giphy.gif" alt="Clipboard Security" width="300" />
</p>

---

## 🚀 What Changed?

This version of `Clipserve` adds a **critical security enhancement** missing from the original script:

> ✅ **Clipboard history is now encrypted using Fernet with a unique key generated at every run.**

This means:

- 🔒 Clipboard entries are no longer stored in plaintext.
- 🔑 Each session uses a fresh, random encryption key.
- 🧹 No hardcoded keys – nothing sensitive is embedded in the source code.
- 🛡️ Encrypted data is decrypted only in-memory for display in the frontend.

---

## 🧠 Why This Matters

The original implementation stored all clipboard contents **in plaintext**, exposing sensitive copied data to **anyone accessing the server or memory**.

With this improvement:
- Session confidentiality is preserved.  
- The attack surface is reduced.  
- You're one step closer to clipboard privacy done right.

---

## ✍️ Author Note

This is a fork of the original `Clipserve` project.  
I made this change to demonstrate a **secure approach to clipboard history tracking**.

Feel free to test it, contribute, or contact me with suggestions! 🙌

---

*Made with 💻 and 🧠 by [5kidRo0t]*
