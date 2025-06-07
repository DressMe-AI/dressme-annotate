import os
import random
import streamlit as st
from PIL import Image

# Config
image_folder = "./data/images"
output_file = "./data/combination_scored.txt"

# Get filenames
top_images = sorted([f for f in os.listdir(image_folder) if f.startswith('top_') and f.endswith('.jpeg')])
bottom_images = sorted([f for f in os.listdir(image_folder) if f.startswith('bottom_') and f.endswith('.jpeg')])

shown_pairs = set()
if os.path.exists(output_file):
    with open(output_file, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) >= 2:
                top_id = parts[0].split(":")[1]
                bottom_id = parts[1].split(":")[1]
                shown_pairs.add((f"{top_id}.jpeg", f"{bottom_id}.jpeg"))

# Session state
if "current_pair" not in st.session_state:
    st.session_state.current_pair = None

def get_next_pair():
    all_combinations = [(t, b) for t in top_images for b in bottom_images]
    random.shuffle(all_combinations)
    for pair in all_combinations:
        if pair not in shown_pairs:
            return pair
    return None

def show_next_pair():
    st.session_state.current_pair = get_next_pair()

if st.session_state.current_pair is None:
    show_next_pair()

pair = st.session_state.current_pair
if pair is None:
    st.write("✅ All unique combinations have been shown.")
    st.stop()

top_path = os.path.join(image_folder, pair[0])
bottom_path = os.path.join(image_folder, pair[1])
top_img = Image.open(top_path).rotate(-90, expand=True)
bottom_img = Image.open(bottom_path).rotate(-90, expand=True)

st.image(top_img, caption=pair[0], width=300)
st.image(bottom_img, caption=pair[1], width=300)

top_id = pair[0].replace(".jpeg", "")
bottom_id = pair[1].replace(".jpeg", "")
st.markdown(f"**Recommendation:** top:{top_id}, bottom:{bottom_id}")

col1, col2 = st.columns(2)
if col1.button("👍 Good"):
    with open(output_file, "a") as f:
        f.write(f"top:{top_id},bottom:{bottom_id},1\n")
    shown_pairs.add(pair)
    show_next_pair()
    st.experimental_rerun()

if col2.button("👎 Bad"):
    with open(output_file, "a") as f:
        f.write(f"top:{top_id},bottom:{bottom_id},0\n")
    shown_pairs.add(pair)
    show_next_pair()
    st.experimental_rerun()
