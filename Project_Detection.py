from ultralytics import YOLO
import os
from pathlib import Path
import time
import pyodbc
from collections import Counter
from ultralytics.engine.predictor import BasePredictor
from ultralytics.engine.results import Results
from ultralytics.utils import ops

# Input
input_folder = r"C:\ML\Project_Automate_YOLOv8\Process_and_Results\Input_And_Detect\input"
model_folder = r"C:\ML\KOCRv8\model_pt"

# Parameters
save_to_project = r'C:\ML\Project_Automate_YOLOv8\Process_and_Results\Input_And_Detect\detect'
name_new_folder = r'Predict_Image'
v_save = True
v_conf = 0.70
v_iou = 0.45 
v_exite = True # For saving all prediction images in one folder.
image_size = (640,640)
source_path = Path(input_folder)

# Function for reading infinite loop format values ​​from a folder.
def read_images(input_folder):
    while True:
        if os.path.exists(input_folder):
            files = os.listdir(input_folder)
            time.sleep(2)
            if files:
                for file in files:
                    try:
                        image_path = os.path.join(input_folder, file)
                        source_name = os.path.basename(image_path)
                        cctv_id = os.path.basename(file)[:11]
                        choose_model(cctv_id, image_path, source_name)
                    except Exception as e:
                        print(f"Missing Image: {e}")
                print("\n All detections in the set are complete, waiting for the next set of images. \n")
            else:
                print("The folder is empty.")
                time.sleep(2)
        else:
            print("This folder doesn't actually exist.")
            break

# Function for selecting models from a database based on CCTV cameras, predicting results, and deleting images.
def choose_model(cctv_id, image_path, source_name):
    try:
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+db_server+';DATABASE='+db_database+';UID='+db_username+';PWD='+ db_password)
        cursor = cnxn.cursor()

        query = """SELECT m.[mm_param_code] FROM [dbo].[ocr_system_param] s
        JOIN [dbo].[ocr_ml_model_param] m ON s.[sys_val_int] = m.[mm_code]
        WHERE s.[sys_param_code] = ?""" 
        cursor.execute(query, cctv_id)

        model_param = cursor.fetchone()

        if model_param:
            model_param_code = model_param[0]
            model_kocr = find_model_file(model_param_code, model_folder)
            print(f"CCTV-ID: {cctv_id} Model Requirements (from Database): {model_param_code}")
            print(f"Model Actually (from files): {model_kocr}") #[22:]
            predict_loop(model_kocr, image_path, cctv_id, source_name)
            os.remove(image_path)
            print("Predicting success and deleting predictions")

        else:
            print(f"No model parameter code found for CCTV ID {cctv_id}")
            model_param_code = None
            os.remove(image_path)
            print("Delete images that do not have a model in the database")

        cursor.close()
        cnxn.close()
    except Exception as e:
        print(f"Error accessing database or the model file was not found in the folder : {e}")
        os.remove(image_path)
        print("Remove unpredictable images")

# Function for finding models whose names match values ​​retrieved from the database.
def find_model_file(model_param_code, model_folder):
    for root, dirs, files in os.walk(model_folder):
        for file in files:
            if file.startswith(model_param_code):
                return os.path.join(root, file)
    return None

# Class for predicting image results and concatenate strings to enter the database.
class DetectionPredictorDB(BasePredictor):
    def __init__(self, overrides=None, cctv_id=None, source_name=None):
        super().__init__(overrides=overrides)
        self.cctv_id = cctv_id
        self.source_name = source_name

    def postprocess(self, preds, img, orig_imgs):
        preds = ops.non_max_suppression(
            preds,
            self.args.conf,
            self.args.iou,
            agnostic=self.args.agnostic_nms,
            max_det=self.args.max_det,
            classes=self.args.classes,
        )

        if not isinstance(orig_imgs, list):  
            orig_imgs = ops.convert_torch2numpy_batch(orig_imgs)

        results = []
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+db_server+';DATABASE='+db_database+';UID='+db_username+';PWD='+ db_password)
        cursor = cnxn.cursor()
        for i, pred in enumerate(preds):
            orig_img = orig_imgs[i]
            pred[:, :4] = ops.scale_boxes(img.shape[2:], pred[:, :4], orig_img.shape)
            img_path = self.batch[0][i]
            if len(pred) == 0: 
                otran_sqlstr = f"""
                INSERT INTO OCR_TRANSACTIONS (
                    otrans_id, otrans_cctv_id, otrans_source_path, otrans_source_name, otrans_sys_info, otrans_detects
                ) VALUES (
                    NEXT VALUE FOR OTRANS_SEQ, '{self.cctv_id}', '{source_path}', '{self.source_name}', '{sys_info}', 0
                )
                """
            else: 
                class_set_index = set()
                for clsi in pred[:, 5]: 
                    class_index = int(clsi)
                    if class_index not in class_set_index: 
                        class_set_index.add(class_index)
                otrans_classes_idx = [f"otrans_class_{idx:02}" if idx < 10 else f"otrans_class_{idx}" for idx in sorted(class_set_index)]
                class_indices = [int(clsn) for clsn in pred[:, 5]]
                class_counts = Counter(class_indices)
                counts_list = [class_counts[idx] for idx in sorted(class_set_index)]
                otrans_classes_idx_str = ', '.join(otrans_classes_idx)
                otrans_classes_num = ', '.join(map(str, counts_list))
                trans_detects_All = sum(counts_list)

                otran_sqlstr = f"""
                INSERT INTO OCR_TRANSACTIONS (
                    otrans_id, otrans_cctv_id, otrans_source_path, otrans_source_name, otrans_sys_info, {otrans_classes_idx_str}, otrans_detects
                ) VALUES (
                    NEXT VALUE FOR OTRANS_SEQ, '{self.cctv_id}', '{source_path}', '{self.source_name}', '{sys_info}', {otrans_classes_num}, {trans_detects_All}
                )
                """
            #print(otran_sqlstr) # for test
            cursor.execute(otran_sqlstr)
            cnxn.commit()

            results.append(Results(orig_img, path=img_path, names=self.model.names, boxes=pred))
        cursor.close()
        cnxn.close()
        return results 

# Functions for retrieving and passing parameters to prediction classes.
def predict_loop(model_kocr, image_path, cctv_id, source_name):
    args = dict(model=model_kocr, conf=v_conf, iou=v_iou, source=image_path, save=v_save, project=save_to_project, name=name_new_folder, exist_ok=v_exite, imgsz=image_size)
    predictor = DetectionPredictorDB(overrides=args, cctv_id=cctv_id, source_name=source_name)
    predictor.predict_cli()

if __name__ == "__main__":
    read_images(input_folder)
