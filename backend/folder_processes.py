import pathlib
import shutil

class folder_processes:
    
    def get_all_categories(new_path):
        with open(new_path, 'r') as f:
            categories = f.readlines()
        categories = [category.replace('\n','') for category in categories]
        return categories
        
    def generate_folders_base_on_categories(categories,image_folder): #to generate folders base of provided categories
        for category in categories:
            pathlib.Path(image_folder+'/'+category).mkdir(parents=True, exist_ok=True)
            
        pathlib.Path(image_folder+'/'+'not_sure_image').mkdir(parents=True, exist_ok=True)
        pathlib.Path(image_folder+'/'+'image_with_no_text').mkdir(parents=True, exist_ok=True)
        
    def move_image_to_folder(image_path,new_path):
        
        try:
            
            shutil.move(str(image_path), new_path)
        except Exception as e:
            #print(e)
            pass
        
        
    def writeToFile(file_path,data):
        with open(file_path,'w') as f:
            f.write('\n'.join(data))
        

        