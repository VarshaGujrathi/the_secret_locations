# Secret Location Project 🗺📸

A simple web application that extracts *location coordinates from image metadata (EXIF data)* and displays them on the website.  
Users can upload images, and both the *image and its metadata* are stored in *Firebase Cloud Database*.  

---

## 🚀 Features
- Upload an image through a simple web interface.
- Extract *GPS coordinates* from image metadata (if available).
- Store image data + metadata in *Firebase*.
- Built using *Django* framework for backend.
- Firebase handles *cloud storage & database*.
- Display uploaded images and their extracted location.

---

## 🛠 Tech Stack
- *Backend*: Django (Python)
- *Frontend*: HTML, CSS, JavaScript
- *Database/Storage*: Firebase Cloud Firestore + Firebase Storage
- *Libraries*:
  - Pillow or ExifRead → for image metadata extraction
  - firebase-admin → Firebase integration with Django

---
