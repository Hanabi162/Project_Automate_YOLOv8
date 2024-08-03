# YOLOv8 Predictor

## Overview
This project utilizes YOLOv8 for object detection and prediction in images. It reads images from a specified input folder, uses the YOLOv8 model for detection, and saves the results to an output folder. Additionally, the results are stored in a SQL Server database.

## Features
- **Object Detection:** Detects objects in images using YOLOv8.
- **Model Selection:** Chooses the appropriate model based on the CCTV ID from the database.
- **Database Integration:** Saves detection results to a SQL Server database.
- **Image Management:** Handles image input and output efficiently.

## Usage
1. **Prepare Your Images:** Place your images in the designated input folder.

2. **Run the Prediction Script:**
    ```bash
    Project_Detection.py
    or
    Project_Segmentation.py
    ```

3. **Database Configuration:** Ensure that the database connection details are configured correctly. Note that the database connection details are not shown in the script for security reasons.

4. **Check Results:** Predicted images will be saved in the output folder, and detection results will be recorded in the database.

## Details
- **YOLOv8 Model:** Utilized for detecting objects in images with customizable parameters.
- **Database Integration:** Retrieves model parameters from a SQL Server database and inserts detection results into the database.
- **Image Handling:** Processes images from an input directory, runs predictions, and saves results to a specified output directory.
- **Counting Detected Classes:** Uses Python's `collections.Counter` to count and manage the number of detected objects of each class.

## Code Explanation
- **Database Connection:** The connection details are kept confidential and are not displayed in the script.
- **SQL Queries:** Constructed SQL queries are not shown for security reasons but are used to insert detection results and manage image data.
- **String Concatenation:** The script builds SQL queries dynamically based on detection results, but these details are not explicitly shown.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
