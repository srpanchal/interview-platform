import csv
import cv2
import argparse

questions_start_end_time = [('1.0', '325.0')]
time_emotion = {}


def start(args):
    video, extention = str(args.video).split(".")
    bucket = {}
    for (start_time, end_time) in questions_start_end_time:
        bucket[(start_time, end_time)] = {}

    with open('data/output/'+ str(video) + '_analysis.csv', 'r+') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            time_emotion[row[2]] = row[0]
            val = row[2]

            for key in bucket:
                if key[0] <= val < key[1]:
                    if row[0] in bucket[key]:
                        bucket[key][row[0]] += 1
                    else:
                        bucket[key][row[0]] = 1

        print(bucket)

    with open('data/output/' + str(args.video) + '_final_report.csv', 'w+') as csvFile:
        writer = csv.writer(csvFile)
        ques_no = 0
        for ques in questions_start_end_time:
            out_csv = []
            ques_no += 1
            out_csv.append('Question-' + str(ques_no))
            emotions_dic = bucket[ques]
            den = sum(emotions_dic.values())
            for key in emotions_dic:
                out_csv.append(key + " : " + str(((emotions_dic[key] * 1.0) / (den * 1.0)) * 100))
            writer.writerow(out_csv)
            print(out_csv)

    # print(time_emotion)

    cap = cv2.VideoCapture('data/' + str(args.video))
    # cap.set(3, 640)
    # cap.set(4, 480)
    # cap.set(cv2.CAP_PROP_POS_MSEC, 1000)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    seconds = 1
    multiplier = fps * seconds
    frameCount = 0
    success, image = cap.read()
    while success or cap.isOpened():
        success, img = cap.read()
        frameId = cap.get(cv2.CAP_PROP_POS_FRAMES)

        pause = False
        if str(frameId / multiplier) in time_emotion:
            cv2.putText(img, str(time_emotion[str(frameId / multiplier)]),
                        (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) - 200, int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) - 50)),
                        cv2.FONT_HERSHEY_PLAIN, 2, 255, 2)
            pause = True

        cv2.imshow('interview', img)
        cv2.waitKey(fps)
        if pause:
            cv2.waitKey(500)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='input video file path')
    parser.add_argument('video', type=str, help='video file path')
    args = parser.parse_args()
    start(args)
