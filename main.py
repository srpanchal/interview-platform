import cv2
import numpy as np
import detect_emption

def start():
    face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')
    eye_cascade = cv2.CascadeClassifier('data/haarcascade_eye.xml')

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, img = cap.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detect_faces(face_cascade, img)

        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            cv2.imshow('video', img)
            # cv2.imwrite("frame.jpg", img)
            # emotion = detect_emption.predict_emotion('tf/retrained_graph.pb', 'frame.jpg', 'tf/retrained_labels.txt', 299, 299, 0, 255, 'Placeholder', 'final_result')
            # print(emotion)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


def detect_faces(face_cascade, colored_img, scaleFactor=1.2):
    img_copy = np.copy(colored_img)
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5);

    return faces

if __name__ == '__main__':
    start()