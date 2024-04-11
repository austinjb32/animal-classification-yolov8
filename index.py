from animals import callback
import streamlit as st
import time
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer
import av
import supervision as sv
from inference.models.utils import get_roboflow_model
import pygame

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

animal_log={}

st.title('Welcome to Wildlife Detection App')

st.subheader('Video Upload and Display')

start_button = st.button("Start Video")

flip = st.checkbox("Flip Camera")
def video_frame_callback(frame):
        img = frame.to_ndarray(format="bgr24")

        img, detected_class_id = callback(img, 0, model, tracker, box_annotator, label_annotator, trace_annotator, names, sound_files, animal_log)

        if detected_class_id is not None:
            sound_file = sound_files.get(detected_class_id)
            if sound_file is not None:
                pygame.mixer.init()
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play()
                pygame.time.wait(300)
                pygame.mixer.music.stop()

        flipped = img[::-1,:,:] if flip else img

        return av.VideoFrame.from_ndarray(flipped, format="bgr24")
   

webrtc_streamer(key="example", video_frame_callback=video_frame_callback)

method = st.sidebar.radio('Go To ->', options=['Webcam', 'Image'])

