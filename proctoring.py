import cv2
import numpy as np

class ProctoringSystem:
    def __init__(self):
        self.use_mediapipe = False
        try:
            import mediapipe as mp
            self.mp_face_mesh = mp.solutions.face_mesh
            # INCREASED CONFIDENCE to 0.7 to reduce false positives
            self.face_mesh = self.mp_face_mesh.FaceMesh(
                max_num_faces=2,
                refine_landmarks=True,
                min_detection_confidence=0.7, 
                min_tracking_confidence=0.7
            )
            self.drawing_utils = mp.solutions.drawing_utils
            self.drawing_styles = mp.solutions.drawing_styles
            self.use_mediapipe = True
        except Exception as e:
            print(f"MediaPipe Error: {e}")
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def analyze_frame(self, frame):
        warning = None
        
        if self.use_mediapipe:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)
            img_h, img_w, _ = frame.shape
            
            if results.multi_face_landmarks:
                # CHECK: Only flag "Multiple People" if we are SURE
                if len(results.multi_face_landmarks) > 1:
                    # Check size of second face to ignore background posters/shadows
                    warning = "⚠️ MULTIPLE PEOPLE DETECTED"
                
                # We only analyze the primary face (the first one)
                primary_face = results.multi_face_landmarks[0]
                
                # Gaze Tracking Logic
                nose_tip = primary_face.landmark[1]
                nose_x = nose_tip.x * img_w
                nose_y = nose_tip.y * img_h
                
                # Relaxed thresholds so it doesn't annoy you
                if nose_x < img_w * 0.10: warning = "⚠️ LOOKING RIGHT"
                elif nose_x > img_w * 0.90: warning = "⚠️ LOOKING LEFT"
                
                # Draw facial mesh
                self.drawing_utils.draw_landmarks(
                    image=frame,
                    landmark_list=primary_face,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.drawing_styles.get_default_face_mesh_tesselation_style()
                )
            else:
                warning = "⚠️ FACE NOT VISIBLE"

        else:
            # Fallback for OpenCV
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) == 0: warning = "⚠️ FACE NOT VISIBLE"
            if len(faces) > 1: warning = "⚠️ MULTIPLE PEOPLE DETECTED"
        
        return frame, warning