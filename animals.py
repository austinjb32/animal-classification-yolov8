import numpy as np
import supervision as sv
from inference.models.utils import get_roboflow_model
from playsound import playsound
import pygame
import cv2

sound_files = {
    0: 'Gunshot.mp3',
    1: 'Bees.mp3',
 
}

model = get_roboflow_model(model_id="animal-classification-tima/5", api_key="69m1zkCJhpHpTvN4WOIV")
tracker = sv.ByteTrack()
box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()
trace_annotator = sv.TraceAnnotator()
names=["Boar", "Elephant", "Giraffe", "Horse", "Lion", "Polar Bear", "Tiger", "Zebra"]

cap = cv2.VideoCapture(0)

animal_log={}

def callback(frame: np.ndarray, _: int) -> np.ndarray:
    pygame.mixer.init()
    results = model.infer(frame)[0]
    detections = sv.Detections.from_inference(results)
    detections = tracker.update_with_detections(detections)

    labels = [
        f"#{tracker_id} {names[class_id]}"
        for class_id, tracker_id
        in zip(detections.class_id, detections.tracker_id)
    ]
    if len(detections.confidence) > 0 and detections.confidence[0] > 0.7:
        if(len(detections.class_id)>0):
            class_id = detections.class_id[0]
        if class_id in sound_files:
            pygame.mixer.music.load(sound_files[class_id])
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.5)
            animal_log['id'] = detections.tracker_id[0]
            animal_log['class'] = names[detections.class_id[0]]
            animal_log['image'] = frame
            print(animal_log)
            pygame.time.wait(500)
        annotated_frame = box_annotator.annotate(frame.copy(), detections=detections)
        annotated_frame = label_annotator.annotate(annotated_frame, detections=detections, labels=labels)
        pygame.mixer.music.stop()
        return trace_annotator.annotate(annotated_frame, detections=detections)
    else:
        return frame



while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret:
        annotated_frame = callback(frame, 0)
        cv2.imshow('frame', annotated_frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()