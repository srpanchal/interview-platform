import cv2
import numpy as np
import detect_emotion
import imutils


def start():
    face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')
    eye_cascade = cv2.CascadeClassifier('data/haarcascade_eye.xml')

    cap = cv2.VideoCapture(0)
    graph = detect_emotion.load_graph('tf/retrained_graph.pb')
    labels = detect_emotion.load_labels('tf/retrained_labels.txt')

    while cap.isOpened():
        success, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cropped_face = img[y:y + h, x:x + w]
            cropped_face_array = imutils.resize(cropped_face, width=299, height=299)
            emotion, probability = detect_emotion.predict_emotion_custom(graph, cropped_face_array, labels, 299, 299, 0, 255, 'Placeholder',
                                                            'final_result')

            cv2.putText(img, str(emotion) + ' : ' + str(probability), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
            cv2.imshow('img', img)
            print(emotion)
        if cv2.waitKey(5) & 0xFF == ord('q'):
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
