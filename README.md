## README

### Overview
- This project consists of two scripts for image processing using YOLO models: one for bounding box detection and another for segmentation tasks. Both scripts perform predictions on images from a specified folder and save the results to a database. The models used are selected based on CCTV camera IDs stored in a database.

### Prerequisites
- Python 3.x
- ultralytics library
- pyodbc library
- Other dependencies (install via pip)

### Input
- **Input Folder:** C:\input (Folder containing images to be processed)
- **Model Folder:** C:\model_pt (Folder containing YOLO model files)

### Parameters
- **save_to_project:** Directory to save prediction results.
- **name_new_folder:** Subdirectory name for saving images.
- **v_save:** Boolean flag to save prediction images.
- **v_conf:** Confidence threshold for predictions (0.70).
- **v_iou:** IoU threshold for non-max suppression (0.45).
- **v_exite:** Boolean flag for saving all predictions in one folder.
- **image_size:** Size of the images for YOLO (640x640).

### Scripts

#### 1. Bounding Box Detection
- **Description:** Processes images to detect bounding boxes using YOLO models and saves results to a database.
- **Functions:**
  - **read_images(input_folder):** Continuously reads images from the input folder and processes them.
  - **choose_model(cctv_id, image_path, source_name):** Selects the appropriate YOLO model based on CCTV ID from the database, performs prediction, and deletes the image after processing.
  - **find_model_file(model_param_code, model_folder):** Finds the YOLO model file based on the model parameter code.
  - **predict_loop(model_ocr, image_path, cctv_id, source_name):** Executes predictions using the selected model and parameters.
- **Class:**
  - **DetectionPredictorDB:** Custom YOLO predictor class that processes predictions and saves results to the database.

#### 2. Segmentation
- **Description:** Processes images to perform segmentation tasks using YOLO models and saves results to a database.
- **Functions:**
  - **read_images(input_folder):** Continuously reads images from the input folder and processes them.
  - **choose_model(cctv_id, image_path, source_name):** Selects the appropriate YOLO model based on CCTV ID from the database, performs prediction, and deletes the image after processing.
  - **find_model_file(model_param_code, model_folder):** Finds the YOLO model file based on the model parameter code.
  - **predict_loop(model_ocr, image_path, cctv_id, source_name):** Executes predictions using the selected model and parameters.
- **Class:**
  - **SegmentationPredictorDB:** Custom YOLO predictor class for segmentation that processes predictions, applies masks, and saves results to the database.

### Example Usage
- To start processing images with bounding box detection, run:
  ```bash
  Project_Detection.py
- To Start processing image with segmentation, run:
   ```bash
  Project_Segmentaion.py
  
