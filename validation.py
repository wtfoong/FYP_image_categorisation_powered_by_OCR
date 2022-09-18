import pathlib
import imghdr
from backend.image_processes import image_processes
from backend.folder_processes import folder_processes
from PyQt6.QtWidgets import QMessageBox

class validator:
    
    def validatePath(path,message):
        if not pathlib.Path(path).exists():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText(message)
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            retval = msg.exec()
            return pathlib.Path(path).exists()
        else: 
            return pathlib.Path(path).exists()
            
    
    def validateImageFolderPath(image_folder_path):
        result = image_processes.get_all_image_path(image_folder_path)
        if result:
            return True
        else:
            return False #"No image in folder path provided."
    
    def chkIfIstxtFile(file_path):
        if pathlib.Path(file_path).suffix!=".txt":
                return False # "File is not txt file."
        else: return True
        
    def validateCategories_txt(file_path):
        try:
            result=folder_processes.get_all_categories(file_path)
            
            if result:
                return True
            else:
                return False #"No category in txt file"
        except Exception as e:
            return False
        
    def validateAccuracyPercentage(percentage):
        if percentage>100 or percentage<0:
            return False
        else: return True
    
    def validateImage(image_path,message):
        if imghdr.what(image_path):
            return True
        else: 
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText(message)
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            retval = msg.exec()
            return False
        
        
if __name__ == "__main__":       
    print(validator.validateImage("D:\g2g\canada_model\CA(for_testing)\Yukon\image_with_no_text\883190_394352_selfie.jpg"))