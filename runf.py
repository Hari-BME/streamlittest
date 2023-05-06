# -*- coding: utf-8 -*-
"""
Created on Fri May  5 21:51:19 2023

@author: Hari
"""
import cv2
import streamlit as st
import os

class RunningAnalyzer:
    def __init__(self, video_path):
        # Open the video file and get its properties
        self.cap = cv2.VideoCapture(video_path)
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.current_frame = None
        
        # Set up the initial marker position
        self.marker_position = None
        self.marker_set = False
        
        # Set up play/pause functionality
        self.play = True
    
    def analyze(self):
        # Loop through the video frames and display them in the window
        while True:
            # Read the next frame and check if the video has ended
            ret, frame = self.cap.read()
            if not ret:
                break
                   
            # Set the current frame number and draw it on the frame
            frame_number = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            cv2.putText(frame, f"Frame: {frame_number}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
          
            # Set the current frame
            self.current_frame = frame.copy()
            
            # Display the current frame in the window
            cv2.imshow("Running Analyzer", self.current_frame)
            
            # Wait for a key press and handle it
            key = cv2.waitKey(1000) & 0xFF
            
            if key == ord("q"):
                break
            elif key == ord("s"):
                # Save a screenshot of the current frame
                cv2.imwrite("screenshot.png", self.current_frame)
            elif key == ord("b"):
                # Move backward one frame
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.cap.get(cv2.CAP_PROP_POS_FRAMES) - 4)
            elif key == ord("f"):
                # Move forward one frame
                pass  # Do nothing, the video will automatically advance to the next frame
            elif key == ord("t"):
                # Move forward 10 frames
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.cap.get(cv2.CAP_PROP_POS_FRAMES) + 9)
            elif key == ord("p"):
                # Pause the video and wait for a button press
                self.play = False
                while True:
                    key = cv2.waitKey(100) & 0xFF
                    if key == ord("p"):
                        # Resume the video
                        self.play = True
                        break
            
            # Advance to the next frame if the video is playing
            if self.play:
                self.cap.grab()
        
        # Release the video capture and close the window
        self.cap.release()
        cv2.destroyAllWindows()

# Set up the Streamlit app
st.set_page_config(page_title="Running Analyzer", page_icon=":runner:")
st.title("Running Analyzer")

# Allow the user to upload a video file
uploaded_file = st.file_uploader("Upload a video file")
if uploaded_file is not None:
    # Save the uploaded file to disk
    file_path = os.path.join(".", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    analyzer = RunningAnalyzer(file_path)
    analyzer.analyze()
    
    # Display a message when the analysis is complete
    st.success("Analysis complete!")




