# Using YOLOv8 For Predictor

## Overview
This project uses YOLOv8 for object detection and prediction in images. The system reads images from a specified input folder, uses a YOLOv8 model for detection, and saves the results to an output folder. Additionally, the results are stored in a SQL Server database.

## Features
- **Object Detection:** Detects objects in images using YOLOv8.
- **Model Selection:** Chooses the appropriate model based on the CCTV ID from the database.
- **Database Integration:** Saves detection results to a SQL Server database.
- **Image Management:** Handles image input and output effectively.

## Details
- **YOLOv8 Model:** Utilized for detecting objects in images with customizable parameters.
- **Database Integration:** Retrieves model parameters from a SQL Server database and inserts detection results into the database.
- **Image Handling:** Processes images from an input directory, runs predictions, and saves results to a specified output directory.
- **Counting Detected Classes:** Uses Python's `collections.Counter` to count and manage the number of detected objects of each class.

## Usage
1. **Prepare Your Images:** Place your images in the designated input folder.

2. **Run the Prediction Script:**
    ```bash
    python predict.py --model <path-to-model> --source <path-to-images>
    ```

3. **Database Configuration:** Ensure the database connection details are configured in the `DatabaseConnect.py` file.

4. **Check Results:** Predicted images will be saved in the output folder, and detection results will be recorded in the database.

## Configuration
- **Model Path:** Path to the YOLOv8 model file.
- **Source Path:** Path to the folder containing images for prediction.
- **Output Path:** Path where the results will be saved.
- **Database Details:** Configure your SQL Server connection in `DatabaseConnect.py`.

## Additional Information
- **Counting Detected Objects:** The `Counter` class from Python's `collections` module is used to count the number of objects detected of each class. This helps in aggregating and managing detection results efficiently.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
