# import face_recognition
# import os
# import cv2  # Add this at the top with other imports

# def encode_known_faces(known_dir):
#     encodings = []
#     for filename in os.listdir(known_dir):
#         img_path = os.path.join(known_dir, filename)
#         print(f"Processing {img_path}...")
#         image = face_recognition.load_image_file(os.path.join(known_dir, filename))
#         face_enc = face_recognition.face_encodings(image)

#         if face_enc:
#             encodings.append(face_enc[0])
#         else:
#             print(f"No face found in {filename}")

#     return encodings


# #for  face matching

# def filter_images(mixed_dir, known_encodings, output_dir):
#     for filename in os.listdir(mixed_dir):
#         img_path = os.path.join(mixed_dir, filename)
#         print(f"Checking {filename}...")

#         image = face_recognition.load_image_file(img_path)
#         face_encodings = face_recognition.face_encodings(image)

#         for face_encoding in face_encodings:
#             matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
#             if True in matches:
#                 print(f"✔ Match found: {filename}")
#                 # Save image to output
#                 output_path = os.path.join(output_dir, filename)
#                 # Convert to BGR for OpenCV saving
#                 bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#                 cv2.imwrite(os.path.join(output_dir, filename), bgr_image)
#                 break  # Stop checking other faces in this image
# # Testing encoding
    
# if __name__ == "__main__":
#     known_encodings = encode_known_faces("known")
#     print(f"Encoded {len(known_encodings)} known face(s).")

#     if known_encodings:
#         filter_images("mixed", known_encodings, "output")
#         print("✅ Filtering complete. Check the 'output' folder.")
#     else:
#         print("❌ No known faces encoded. Please check your training images.")


import face_recognition
import os
import cv2

known_dir = "uploads/known"
mixed_dir = "uploads/mixed"
output_dir = "output"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

known_encodings = []
for filename in os.listdir(known_dir):
    image = face_recognition.load_image_file(os.path.join(known_dir, filename))
    encodings = face_recognition.face_encodings(image)
    if encodings:
        known_encodings.append(encodings[0])

for filename in os.listdir(mixed_dir):
    image_path = os.path.join(mixed_dir, filename)
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    for face_encoding in encodings:
        results = face_recognition.face_distance(known_encodings, face_encoding)
        if results.min() < 0.45:
            bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(os.path.join(output_dir, filename), bgr_image)
            break