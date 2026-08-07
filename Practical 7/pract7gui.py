import heapq
from collections import Counter
import tkinter as tk
from tkinter import ttk, messagebox


class Node:
    def __init__(self, char=None, freq=None):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(frequencies):
    heap = [Node(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    return heap[0]


def generate_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}

    if node:
        if node.char is not None:
            codebook[node.char] = prefix if prefix else "0"

        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)

    return codebook


def huffman_encoding(data):
    if not data:
        return "", {}

    frequencies = Counter(data)
    root = build_huffman_tree(frequencies)
    codebook = generate_codes(root)
    encoded_data = "".join(codebook[ch] for ch in data)

    return encoded_data, codebook


def huffman_decoding(encoded_data, codebook):
    reverse = {v: k for k, v in codebook.items()}
    decoded = ""
    current = ""

    for bit in encoded_data:
        current += bit
        if current in reverse:
            decoded += reverse[current]
            current = ""

    return decoded


def encode_text():
    text = input_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning("Warning", "Please enter text.")
        return

    global codebook

    encoded, codebook = huffman_encoding(text)
    decoded = huffman_decoding(encoded, codebook)

    freq = Counter(text)

    frequency_box.config(state="normal")
    frequency_box.delete("1.0", tk.END)
    for ch, f in freq.items():
        frequency_box.insert(tk.END, f"'{ch}' : {f}\n")
    frequency_box.config(state="disabled")

    codebook_box.config(state="normal")
    codebook_box.delete("1.0", tk.END)
    for ch, code in codebook.items():
        codebook_box.insert(tk.END, f"'{ch}' : {code}\n")
    codebook_box.config(state="disabled")

    encoded_var.set(encoded)
    decoded_var.set(decoded)


root = tk.Tk()
root.title("Huffman Coding Visualizer")
root.geometry("800x650")
root.resizable(False, False)

codebook = {}

title = tk.Label(
    root,
    text="Huffman Coding GUI",
    font=("Arial", 18, "bold"),
    fg="navy"
)
title.pack(pady=10)

tk.Label(root, text="Enter Text:", font=("Arial", 12)).pack()

input_text = tk.Text(root, height=5, width=70)
input_text.pack(pady=5)

ttk.Button(root, text="Encode & Decode", command=encode_text).pack(pady=10)

tk.Label(root, text="Character Frequencies", font=("Arial", 12, "bold")).pack()

frequency_box = tk.Text(root, height=8, width=35)
frequency_box.pack()
frequency_box.config(state="disabled")

tk.Label(root, text="Huffman Codebook", font=("Arial", 12, "bold")).pack()

codebook_box = tk.Text(root, height=8, width=35)
codebook_box.pack()
codebook_box.config(state="disabled")

encoded_var = tk.StringVar()
decoded_var = tk.StringVar()

tk.Label(root, text="Encoded Binary:", font=("Arial", 12, "bold")).pack(pady=5)
tk.Entry(root, textvariable=encoded_var, width=90).pack()

tk.Label(root, text="Decoded Text:", font=("Arial", 12, "bold")).pack(pady=5)
tk.Entry(root, textvariable=decoded_var, width=90).pack()

root.mainloop()
