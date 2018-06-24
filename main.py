import cv2
import numpy as np
import detect_emotion
import imutils
import csv
import argparse


def start(args):
    face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')
    eye_cascade = cv2.CascadeClassifier('data/frontalEyes35x16.xml')

    graph_face = detect_emotion.load_graph('tf_cropped/retrained_graph.pb')
    labels_face = detect_emotion.load_labels('tf_cropped/retrained_labels.txt')

    graph_eyes = detect_emotion.load_graph('tf_eyes/retrained_graph.pb')
    labels_eyes = detect_emotion.load_labels('tf_eyes/retrained_labels.txt')

    video, extention = str(args.video).split(".")
    writeFile = open('data/output/'+ str(video) + '_analysis.csv', 'w')

    cap = cv2.VideoCapture('data/' + str(args.video))
    cap.set(3, 640)
    cap.set(4, 480)
    # cap.set(cv2.CAP_PROP_POS_MSEC, 1000)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    seconds = 1
    multiplier = fps * seconds
    frameCount = 0
    success, image = cap.read()

    with writeFile:
        writer = csv.writer(writeFile)
        while success:
            success, img = cap.read()
            frameId = cap.get(cv2.CAP_PROP_POS_FRAMES)

            if frameId % multiplier == 0:
                frameCount += 1
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    cropped_face = img[y:y + h, x:x + w]
                    cropped_face_gray = gray[y:y + h, x:x + w]

                    # eyes = eye_cascade.detectMultiScale(cropped_face_gray)
                    # for (ex, ey, ew, eh) in eyes:
                    #     #cv2.rectangle(cropped_face, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                    #     cropped_eyes = cropped_face[ey: ey + eh, ex:ex + ew]
                    #     cropped_eyes = cv2.resize(cropped_eyes, (299, 299))
                    #     focus, probability_foc = detect_emotion.predict_emotion_custom(graph_eyes, cropped_eyes, labels_eyes,
                    #                                                                    299, 299, 0,
                    #                                                                    255, 'Placeholder',
                    #                                                                    'final_result')
                    #     cv2.putText(img, str(focus) + ' : ' + str(probability_foc), (ex, ey), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)

                    cropped_face_array = imutils.resize(cropped_face, width=299, height=299)
                    emotion, probability_emo = detect_emotion.predict_emotion_custom(graph_face, cropped_face_array,
                                                                                     labels_face, 299, 299, 0,
                                                                                     255, 'Placeholder',
                                                                                     'final_result')

                    cv2.putText(img, str(emotion) + ' : ' + str(probability_emo), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                255)
                    # cv2.imshow('img', img)
                    writer.writerow([emotion, probability_emo, str(frameId / fps)])
                    print(str(emotion) + ' : ' + str(probability_emo) + ' @ ' + str(frameId / fps))
                    #cv2.imwrite('data/output/' + str(video) + '/' + str(frameId / fps) + ".jpg", img)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()


def detect_faces(face_cascade, colored_img, scaleFactor=1.2):
    img_copy = np.copy(colored_img)
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5)

    return faces


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='input video file path')
    parser.add_argument('video', type=str, help='video file path')
    args = parser.parse_args()
    start(args)
