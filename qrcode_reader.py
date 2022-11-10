import cv2


def get_qr_code():
    cap, detector = abrir_cam()

    while True:
        _, img = cap.read()

        # detect and decode
        data = detector.detectAndDecode(img)
        # check if there is a QRCode in the image
        if data:
            a=data
            break

        cv2.imshow("QRCODEscanner", img)
        if cv2.waitKey(1) == ord("q"):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    return a

def abrir_cam():
    cap = cv2.VideoCapture(0)
    # initialize the cv2 QRCode detector
    detector = cv2.QRCodeDetector()
    return cap,detector