from picamera2 import Picamera2
import cv2
# initialize the camera and grab a reference to the raw camera capture
camera = Picamera2()
camera.preview_configuration.main.size=(1280,720)
camera.preview_configuration.main.format="RGB888"
camera.preview_configuration.align()
camera.configure("preview")
camera.start()
while True:
    frame=camera.capture_array()
    cv2.imshow("pi",frame)
    if cv2.waitKey(1)==ord('q'):
        break
cv2.destroyAllWindows()

