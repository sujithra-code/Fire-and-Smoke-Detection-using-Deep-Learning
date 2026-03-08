#  Fire & Smoke Detection Using YOLOv8

## Overview
This project implements a **Fire and Smoke Detection using Deep Learning**. The system uses the YOLOv8 object detection model to detect fire from images and live camera footage. OpenCV is used to capture and process frames, and the model identifies fire regions in real time. When fire is detected, the system triggers an alarm and sends email and SMS alerts. The interface was implemented using Python with Tkinter and Flask.

- This project implements a **Fire and Smoke Detection using Deep Learning**. The system uses the YOLOv8 object detection model to detect fire from images and live camera footage. OpenCV is used to capture and process frames, and the model identifies fire regions in real time. When fire is detected, the system triggers an alarm and sends email and SMS alerts. The interface was implemented using Python with Tkinter and Flask.
---

##  Model Details

- **Architecture:** YOLOv8 Nano  
- **Framework:** PyTorch  
- **Trained Weights:** `best.pt`  
- **Dataset Format:** YOLO (train / valid / test)  

⚠ Dataset is not uploaded due to size limitations.

---

##  Technologies Used

- Python  
- Ultralytics YOLOv8  
- PyTorch  
- OpenCV  
- NumPy  
- Flask  
- MySQL
---

##  Installation

```bash
pip install -r requirements.txt
```

---

##  Run the Project

```bash
python app.py
```

Make sure `best.pt` is present in the project folder.

---
