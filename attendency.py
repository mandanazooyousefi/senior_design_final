import face_recognition
import cv2
import os

# Define image paths
image_paths = [
    '/Users/mandanazy/desktop/mandana.jpeg',
    '/Users/mandanazy/desktop/sahand.jpeg',
    '/Users/mandanazy/desktop/amin.jpeg',
    '/Users/mandanazy/desktop/fahime.jpeg',
    '/Users/mandanazy/desktop/majid.jpeg'
]

# Check if image files exist
for path in image_paths:
    if not os.path.isfile(path):
        print(f"File not found: {path}")
        exit()

known_faces = []

# Load known faces
for path in image_paths:
    try:
        image = face_recognition.load_image_file(path)
        face_encoding = face_recognition.face_encodings(image)

        if len(face_encoding) > 0:
            known_faces.append(face_encoding[0])
        else:
            print(f"No face detected in {path}")
            exit()

    except Exception as e:
        print(f"Error loading or encoding image {path}: {e}")
        exit()

# Define the path for the captured image
captured_image_path = '/Users/mandanazy/desktop/captured_image.jpg'

# Capture an image from the MacOS camera
cap = cv2.VideoCapture(0)

ret, frame = cap.read()
if not ret:
    print("Failed to capture image")
    cap.release()
    exit()

# Save the captured image
cv2.imwrite(captured_image_path, frame)
cap.release()
cv2.destroyAllWindows()

# Ensure the image file was saved
if not os.path.isfile(captured_image_path):
    print(f"Failed to save the captured image at {captured_image_path}")
    exit()

# Load the captured image and encode the face
try:
    captured_image = face_recognition.load_image_file(captured_image_path)
    captured_face_encodings = face_recognition.face_encodings(captured_image)

    if len(captured_face_encodings) > 0:
        captured_face_encoding = captured_face_encodings[0]
    else:
        print("No face detected in the captured image.")
        exit()

except Exception as e:
    print(f"Error loading or encoding captured image: {e}")
    exit()

# Compare the captured face with known faces
results = face_recognition.compare_faces(known_faces, captured_face_encoding)

# Print the result
for i in range(len(results)):
    if results[i]:
        print(f"The captured image matches {image_paths[i]}")
        break
else:
    print("No match found")
