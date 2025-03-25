import streamlit as st
import cv2
import numpy as np
import os
from PIL import Image

def logistic_map(r, x, n):
    sequence = []
    for _ in range(n):
        x = r * x * (1 - x)
        sequence.append(x)
    return np.array(sequence)

def encrypt_image(image, x0, r=3.99):
    M, N = image.shape
    num_pixels = M * N
    chaotic_seq = logistic_map(r, x0, num_pixels)
    chaotic_seq = (chaotic_seq * 255).astype(np.uint8).reshape(M, N)
    encrypted_image = cv2.bitwise_xor(image, chaotic_seq)
    return encrypted_image, chaotic_seq

def decrypt_image(encrypted_image, chaotic_seq):
    decrypted_image = cv2.bitwise_xor(encrypted_image, chaotic_seq)
    return decrypted_image

st.set_page_config(page_title="Image Encryption & Decryption", page_icon="🔒", layout="centered")

st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            padding: 10px;
        }
        .stDownloadButton>button {
            background-color: #008CBA;
            color: white;
            border-radius: 8px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🔐 Image Encryption & Decryption using Logistic Map")
st.write("Secure your images with chaotic encryption")

uploaded_file = st.file_uploader("📂 Upload an image", type=["jpg", "png", "jpeg"], help="Choose an image to encrypt and decrypt")

x0 = st.number_input("🔢 Enter initial value (x0)", min_value=0.0, max_value=1.0, value=0.56789, step=0.00001)
r = st.slider("🎚 Select r value", min_value=3.5, max_value=4.0, value=3.99, step=0.01)

if uploaded_file:
    with st.spinner("Processing image..."):
        image = Image.open(uploaded_file).convert("L")
        image = np.array(image)
        image = cv2.resize(image, (256, 256))
        
        st.image(image, caption="🖼 Original Image", use_column_width=True, channels="L")
        
        encrypted_image, chaotic_seq = encrypt_image(image, x0, r)
        decrypted_image = decrypt_image(encrypted_image, chaotic_seq)
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(encrypted_image, caption="🔏 Encrypted Image", use_column_width=True, channels="L")
        with col2:
            st.image(decrypted_image, caption="🔓 Decrypted Image", use_column_width=True, channels="L")
        
        cv2.imwrite("encrypted_image.jpg", encrypted_image)
        cv2.imwrite("decrypted_image.jpg", decrypted_image)
        
        st.success("✅ Image encryption & decryption completed!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("⬇ Download Encrypted Image", data=open("encrypted_image.jpg", "rb").read(), file_name="encrypted_image.jpg", mime="image/jpeg")
        with col2:
            st.download_button("⬇ Download Decrypted Image", data=open("decrypted_image.jpg", "rb").read(), file_name="decrypted_image.jpg", mime="image/jpeg")
