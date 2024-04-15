import numpy as np
import supervision as sv
import pygame
from check import sendEmail
from database import client
import datetime

collection = client['main']['animal_log']


def create_log(class_name):
    animal_log = {
        "class": class_name,
        "timestamp":datetime.datetime.now()
    }
    return collection.insert_one(animal_log)

def create_mail_state(frame, name):
    data = collection.find({"timestamp": {"$gte": (datetime.datetime.now() - datetime.timedelta(minutes=10))}})
    if data.count() == 0: 
        sendEmail(frame,name+" Detected", "A "+name+"  was Detected" )

     

def callback(frame: np.ndarray, _: int, model, tracker, box_annotator, label_annotator, trace_annotator, names, sound_files, animal_log) -> np.ndarray:
    pygame.mixer.init()
    results = model.infer(frame)[0]
    detections = sv.Detections.from_inference(results)
    detections = tracker.update_with_detections(detections)

    labels = [
        f"#{tracker_id} {names[class_id]}"
        for class_id, tracker_id
        in zip(detections.class_id, detections.tracker_id)
    ]
    if len(detections.confidence) > 0 and detections.confidence[0] > 0.8:
        if(len(detections.class_id)>0 and detections.class_id[0] == 0 or 1):
            class_id = detections.class_id[0]
            create_mail_state(frame, names[class_id])
            annotated_frame = box_annotator.annotate(frame.copy(), detections=detections)
            annotated_frame = label_annotator.annotate(annotated_frame, detections=detections, labels=labels)
            return trace_annotator.annotate(annotated_frame, detections=detections), class_id
    else:
        return frame, None



