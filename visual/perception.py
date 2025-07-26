"""
Visual Perception Module Scaffold
- Processes raw visual input (e.g., frames, images)
- Extracts high-level features (e.g., NPC detection, object recognition)
- Returns structured observations for agent use
 
High-Level Overview:
--------------------
This module implements a visual perception pipeline for embodied agents. It pre-filters raw image frames (numpy arrays) and extracts structured, high-level features including:
    - Edge density (Canny)
    - Dominant color (k-means)
    - Motion and change detection (frame differencing)
    - Light/dark adaptation (average brightness)
    - Visual attention (saliency map, if available)
    - Text reading (OCR via pytesseract)
    - Object recognition (YOLOv3 via OpenCV DNN)
The output is a dictionary of features suitable for agent decision logic and direct database storage. See README for usage details.
"""

# Consolidated imports
import cv2
import numpy as np
import random

class VisualPerception:
    def __init__(self):
        # Load YOLO model (YOLOv3 as example)
        # Paths to YOLO weights and config (update these as needed)
        self.yolo_weights = "yolov3.weights"
        self.yolo_cfg = "yolov3.cfg"
        self.yolo_classes = "coco.names"
        try:
            self.net = cv2.dnn.readNet(self.yolo_weights, self.yolo_cfg)
            with open(self.yolo_classes, "r") as f:
                self.classes = [line.strip() for line in f.readlines()]
        except Exception as e:
            print(f"YOLO model not loaded: {e}")
            self.net = None
            self.classes = []

    def process_frame(self, frame):
        """
        Process a raw video frame and extract features.
        Args:
            frame: Raw image/frame data (could be numpy array, etc.)
        Returns:
            observation: dict with high-level features
        """
        observation = {}
        observation['edges'] = self.detect_edges(frame)
        observation['dominant_color'] = self.analyze_color(frame)
        observation['motion_detected'] = self.detect_motion(frame)
        observation['change_detected'] = self.detect_change(frame)
        observation['light_dark'] = self.light_dark_adaptation(frame)
        observation['visual_attention'] = self.visual_attention(frame)
        observation['text'] = self.read_text(frame)
        observation['objects'] = self.recognize_objects(frame)
        return observation
    
    def detect_change(self, frame):
        """
        Detects scene changes over time (frame differencing, but with longer memory).
        Returns True if significant change detected, else False.
        """
        if frame is None:
            return False
        # Convert to grayscale
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame
        # Store previous frame for change detection
        if not hasattr(self, '_prev_change_gray'):
            self._prev_change_gray = gray
            return False
        diff = cv2.absdiff(self._prev_change_gray, gray)
        change_pixels = np.sum(diff > 50)
        self._prev_change_gray = gray
        # Heuristic: change detected if enough pixels changed
        return change_pixels > 2000

    def read_text(self, frame):
        """
        Reads text from the frame using OCR (pytesseract).
        Returns detected text (str).
        """
        try:
            import pytesseract
        except ImportError:
            return "(pytesseract not installed)"
        if frame is None:
            return ""
        # Convert to RGB for pytesseract
        if len(frame.shape) == 2:
            rgb = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        else:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(rgb)
        return text.strip()

    def light_dark_adaptation(self, frame):
        """
        Computes average brightness to simulate light/dark adaptation.
        Returns: 'dark', 'dim', 'normal', 'bright'
        """
        if frame is None:
            return 'unknown'
        # Convert to grayscale
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame
        avg_brightness = np.mean(gray)
        if avg_brightness < 50:
            return 'dark'
        elif avg_brightness < 100:
            return 'dim'
        elif avg_brightness < 180:
            return 'normal'
        else:
            return 'bright'

    def visual_attention(self, frame):
        """
        Computes a saliency map using OpenCV's StaticSaliencySpectralResidual.
        Returns: 'low', 'medium', or 'high' attention (based on saliency map mean)
        """
        if frame is None:
            return 'unknown'
        try:
            saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
        except AttributeError:
            return '(OpenCV saliency not available)'
        # Convert to grayscale if needed
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame
        (success, saliencyMap) = saliency.computeSaliency(gray)
        if not success:
            return 'unknown'
        mean_sal = np.mean(saliencyMap)
        if mean_sal < 0.2:
            return 'low'
        elif mean_sal < 0.5:
            return 'medium'
        else:
            return 'high'

    def detect_edges(self, frame):
        """
        Detect edges in the frame using OpenCV's Canny edge detector.
        Returns a summary: 'none', 'some', or 'many' edges.
        """
        if frame is None:
            return 'none'
        # Convert to grayscale if needed
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame
        # Apply Canny edge detector
        edges = cv2.Canny(gray, 100, 200)
        # Count edge pixels
        edge_count = np.sum(edges > 0)
        # Heuristic: classify edge density
        if edge_count < 100:
            return 'none'
        elif edge_count < 1000:
            return 'some'
        else:
            return 'many'

    def analyze_color(self, frame):
        """
        Analyze the dominant color in the frame using k-means clustering.
        Returns: color name (str)
        """
        if frame is None:
            return 'unknown'
        # Resize for speed
        small = cv2.resize(frame, (50, 50))
        # Reshape to a list of pixels
        pixels = small.reshape((-1, 3))
        pixels = np.float32(pixels)
        # K-means clustering
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 1
        _, labels, centers = cv2.kmeans(pixels, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        dominant = centers[0].astype(int)
        # Map to color name (simple heuristic)
        b, g, r = dominant
        if r > g and r > b:
            return 'red'
        elif g > r and g > b:
            return 'green'
        elif b > r and b > g:
            return 'blue'
        else:
            return 'gray'

    def detect_motion(self, frame):
        """
        Detect motion between frames using simple frame differencing.
        Returns True if motion is detected, else False.
        """
        if frame is None:
            return False
        # Convert to grayscale for comparison
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame
        # Initialize previous frame storage
        if not hasattr(self, '_prev_gray'):
            self._prev_gray = gray
            return False
        # Compute absolute difference
        diff = cv2.absdiff(self._prev_gray, gray)
        # Threshold the difference
        thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
        motion_pixels = np.sum(thresh > 0)
        self._prev_gray = gray
        # Heuristic: motion detected if enough pixels changed
        return motion_pixels > 500

    def recognize_objects(self, frame):
        """
        Recognize objects in the frame using YOLO and OpenCV DNN.
        Returns: list of object names
        """
        if frame is None or self.net is None:
            return []
        # Prepare input blob for YOLO
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        # Get output layer names
        ln = self.net.getUnconnectedOutLayersNames()
        # Run forward pass
        layer_outputs = self.net.forward(ln)
        boxes = []
        confidences = []
        class_ids = []
        h, w = frame.shape[:2]
        # Parse outputs
        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * w)
                    center_y = int(detection[1] * h)
                    width = int(detection[2] * w)
                    height = int(detection[3] * h)
                    x = int(center_x - width / 2)
                    y = int(center_y - height / 2)
                    boxes.append([x, y, width, height])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        # Non-max suppression to remove duplicates
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        detected_objects = []
        if len(idxs) > 0:
            for i in idxs.flatten():
                label = self.classes[class_ids[i]] if class_ids[i] < len(self.classes) else str(class_ids[i])
                detected_objects.append(label)
        return detected_objects

if __name__ == "__main__":
    vp = VisualPerception()
    # Load a test image
    image_path = "test_image.jpg"  # Change to your image filename
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Failed to load image: {image_path}")
    else:
        obs = vp.process_frame(frame)
        print("Observation from image:")
        for k, v in obs.items():
            print(f"{k}: {v}")
