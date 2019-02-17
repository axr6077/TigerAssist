'''
@author : Ayush Rout
'''
import cv2
import numpy as np
import util
import re
import NeuralNet_train as networkTrain

model = networkTrain.NeuralNet_train(17)

'''
init and configure camera src
'''
cap = cv2.VideoCapture(0)
ret = cap.set(3, 1920)
ret = cap.set(4, 1080)
font = cv2.FONT_HERSHEY_SIMPLEX

'''
text initializations
'''
text = " "
temp = 0
previousLabel = None
label = None

'''
main logic
'''
def main():
    while(cap.isOpened()):
        ret, img = cap.read()
        img1 = cv2.flip(img, 1)
        cv2.rectangle(img, (900, 100), (1300, 500), (255, 0, 0), 5)
        img1 = img[100:500, 900:1300]
        img_ycrcb = cv2.cvtColor(img1, cv2.COLOR_BGR2YCR_CB)
        blur = cv2.GaussianBlur(img_ycrcb, (11, 11), 0)
        skin_ycrcb_min = np.array((0,138,67))
        skin_ycrcb_max = np.array((255, 173, 133))
        mask = cv2.inRange(blur, skin_ycrcb_min, skin_ycrcb_max)
        contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, 2)
        cnt = util.getMaxContour(contours, 4000)
        if cnt.any() != None:
            gesture, label = util.getGestureImg(cnt, img1, mask, model)
            if(label != None):
                if (temp == 0):
                    previousLabel = label
                if (previousLabel == label):
                    previousLabel = label
                    temp += 1
                else:
                    temp = 0
                if (temp == 40):
                    if (label == 'P'):
                        label = "Beer" #challenged by Constellation

                    text = text + label

                    if (label == 'Q'):
                        words = re.split(" +", text)
                        words.pop()
                        text = " ".join(words)

            if (gesture.any()):
                cv2.imshow('Predicted Gesture', gesture)
            else:
                print('No gesture predicted')
            cv2.putText(img, label, (50,150), font, 8, (0, 125, 155), 2)
            cv2.putText(img, text, (50, 540), font, 3, (0, 0, 255), 2)
        cv2.imshow('Frame', img)
        cv2.imshow('Mask', mask)
        k = 0xFF & cv2.waitKey(10)
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()