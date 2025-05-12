import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import os

# Setup webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Hand detector
detector = HandDetector(maxHands=1)

# Game variables
timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [AI, Player]
imgAI = None  # Initialize AI image

while True:
    # Load background image
    imgBG = cv2.imread("Resources/BG.png")

    # Read webcam image
    success, img = cap.read()
    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # Detect hands
    hands, img = detector.findHands(imgScaled)

    if startGame:
        if not stateResult:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435),
                        cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 1:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)

                    # Rock
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    # Paper
                    elif fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    # Scissors
                    elif fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3

                    # AI move
                    randomNumber = random.randint(1, 3)
                    imgPath = f"Resources/{randomNumber}.png"
                    if os.path.exists(imgPath):
                        imgAI = cv2.imread(imgPath, cv2.IMREAD_UNCHANGED)
                        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    # Determine winner
                    if playerMove:
                        # Player Wins
                        if (playerMove == 1 and randomNumber == 3) or \
                           (playerMove == 2 and randomNumber == 1) or \
                           (playerMove == 3 and randomNumber == 2):
                            scores[1] += 1
                        # AI Wins
                        elif (playerMove == 3 and randomNumber == 1) or \
                             (playerMove == 1 and randomNumber == 2) or \
                             (playerMove == 2 and randomNumber == 3):
                            scores[0] += 1

    # Place webcam image in BG
    imgBG[234:654, 795:1195] = imgScaled

    # Show AI move only if defined
    if stateResult and imgAI is not None:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    # Display scores
    cv2.putText(imgBG, str(scores[0]), (410, 215),
                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215),
                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    # Show final output
    cv2.imshow("BG", imgBG)

    # Keyboard input
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        stateResult = False
        initialTime = time.time()
        imgAI = None  # Reset AI image
    elif key == ord('q'):
        break

# Release webcam and close window
cap.release()
cv2.destroyAllWindows()
