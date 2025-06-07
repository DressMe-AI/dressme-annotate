import os
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Configuration
image_folder = "./data/images"
output_file = "./data/combination_scored.txt"

# Prepare image lists
top_images = sorted([f for f in os.listdir(image_folder) if f.startswith("top_") and f.endswith(".jpeg")])
bottom_images = sorted([f for f in os.listdir(image_folder) if f.startswith("bottom_") and f.endswith(".jpeg")])
shown_pairs = set()

# Load existing log
if os.path.exists(output_file):
    with open(output_file, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) >= 2:
                top_id = parts[0].split(":")[1]
                bottom_id = parts[1].split(":")[1]
                shown_pairs.add((f"{top_id}.jpeg", f"{bottom_id}.jpeg"))

# GUI setup
root = tk.Tk()
root.title("Image Pair Rating")

# Image display labels
top_img_label = tk.Label(root)
top_img_label.pack(pady=10)

bottom_img_label = tk.Label(root)
bottom_img_label.pack(pady=10)

# Global pair state
current_pair = [None, None]


def load_image(path):
    try:
        img = Image.open(path)
        img.thumbnail((300, 300))
        img = img.rotate(-90, expand=True)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None


def get_next_pair():
    all_combinations = [(t, b) for t in top_images for b in bottom_images]
    random.shuffle(all_combinations)
    for pair in all_combinations:
        if pair not in shown_pairs:
            return pair
    return None


def update_images():
    pair = get_next_pair()
    if not pair:
        messagebox.showinfo("Done", "All unique combinations have been shown.")
        root.quit()
        return

    current_pair[0], current_pair[1] = pair
    top_path = os.path.join(image_folder, current_pair[0])
    bottom_path = os.path.join(image_folder, current_pair[1])

    top_img = load_image(top_path)
    bottom_img = load_image(bottom_path)

    if top_img:
        top_img_label.configure(image=top_img)
        top_img_label.image = top_img
    if bottom_img:
        bottom_img_label.configure(image=bottom_img)
        bottom_img_label.image = bottom_img

    top_id = current_pair[0].replace(".jpeg", "")
    bottom_id = current_pair[1].replace(".jpeg", "")
    print(f"\nRecommendation: top:{top_id}, bottom:{bottom_id}")


def rate_pair(score):
    top_id = current_pair[0].replace(".jpeg", "")
    bottom_id = current_pair[1].replace(".jpeg", "")
    with open(output_file, "a") as f:
        f.write(f"top:{top_id},bottom:{bottom_id},{score}\n")
    shown_pairs.add((current_pair[0], current_pair[1]))
    print("Saved feedback. Showing next...\n")
    update_images()


# Control buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

good_button = tk.Button(button_frame, text="Good (1)", width=15, command=lambda: rate_pair(1))
good_button.pack(side="left", padx=10)

bad_button = tk.Button(button_frame, text="Bad (0)", width=15, command=lambda: rate_pair(0))
bad_button.pack(side="left", padx=10)

quit_button = tk.Button(button_frame, text="Quit (q)", width=15, command=root.quit)
quit_button.pack(side="left", padx=10)

# Start first pair
update_images()

# Launch GUI
root.mainloop()

