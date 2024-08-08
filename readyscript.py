import cv2
from picamera2 import Picamera2
import math
import vonage
import time
import sys
from ultralytics import YOLO
import AI_gcodesender_v2 as gc
client = vonage.Client(key="cf359f43", secret="ob71tfyfyLObwGmY")
sms = vonage.Sms(client)
# Initialize the Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Load the YOLOv8 model
model = YOLO("model1.pt")

while True:
    # Capture frame-by-frame
    frame = picam2.capture_array()

    # Run YOLOv8 inference on the frame
    results = model(frame)
    for r in results:
        boxes=r.boxes
        for box in boxes:
            conf = math.ceil((box.conf[0]*100))/100
            print(conf)
            if conf>=0.6:
                responseData = sms.send_message(
                {
                "from": "Vonage APIs",
                "to": "918303420085",
                "text": "Your print has failed, please check it asap",
                }
            )

                if responseData["messages"][0]["status"] == "0":
                    print("Message sent successfully.")
                else:
                    print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
                gc.main()
                time.sleep(5)
                sys.exit()
                break

    # Visualize the results on the frame
    annotated_frame = results[0].plot()
    # print (results[0])

    # Display the resulting frame
    cv2.imshow("Camera", annotated_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Release resources and close windows
cv2.destroyAllWindows()





