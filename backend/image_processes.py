import pathlib

class image_processes:
    
    def get_all_image_path(image_folder_path):
        ext = ['*.png', '*.jpg', '*.gif','*.jpeg']    # Add image formats here
        all_image_path_list = []

        [all_image_path_list.extend(pathlib.Path(image_folder_path).rglob(e)) for e in ext] #To get iamges of different formats 
        all_image_path_list = sorted(all_image_path_list) #list that consist of all image path for the images in the folder
        return all_image_path_list