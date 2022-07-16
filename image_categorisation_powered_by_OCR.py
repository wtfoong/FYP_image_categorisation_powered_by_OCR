import io
import json
import multiprocessing
import os
import pathlib
import shutil
import time
from rapidfuzz import fuzz,process
from itertools import islice

from google.cloud import vision
from google.cloud.vision_v1 import AnnotateImageResponse

########################################## User input data ##############################################################################

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/rainy/OneDrive - Asia Pacific University/FYP/system/thinking-avenue-356203-9d7d01f4e556.json"

image_folder = 'D:/g2g/canada_model/CA(for_testing)/Alberta' #insert the file path to the images here.

categories_txtfile = 'categories.txt'  # insert the path to the txt file that stores all the categories for the images.

#the number of subprocesses allowed
subProcessNumber=20

#the number of lines of the OCR result that should be read for comparison, if not sure just put None
lines_to_read = 7

#the percentage of accuracy the OCR result need to be with the category provided.
accuracy_percentage = 60

############################################################################################################################################


class image_processes:
    
    def get_all_image_path(image_folder_path):
        ext = ['*.png', '*.jpg', '*.gif','*.jpeg']    # Add image formats here
        all_image_path_list = []

        [all_image_path_list.extend(pathlib.Path(image_folder_path).rglob(e)) for e in ext] #To get iamges of different formats 
        all_image_path_list = sorted(all_image_path_list) #list that consist of all image path for the images in the folder
        return all_image_path_list


class folder_processes:
    def get_all_categories(new_path):
        with open(new_path, 'r') as f:
            categories = f.readlines()
        categories = [category.replace('\n','') for category in categories]
        return categories
        
    def generate_folders_base_on_categories(categories): #to generate folders base of provided categories
        for category in categories:
            pathlib.Path(image_folder+'/'+category).mkdir(parents=True, exist_ok=True)
            
        pathlib.Path(image_folder+'/'+'not_sure_image').mkdir(parents=True, exist_ok=True)
        pathlib.Path(image_folder+'/'+'image_with_no_text').mkdir(parents=True, exist_ok=True)
        
    def move_image_to_folder(image_path,new_path):
        
        try:
            
            shutil.move(str(image_path), new_path)
        except Exception as e:
            print(e)
            pass
        

class comparison:
    def detect_text(path):
        """Detects text in the image."""


        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)


        response = client.document_text_detection(image=image,image_context={"language_hints": ["id"]})
        response_json = AnnotateImageResponse.to_json(response)
        response = json.loads(response_json)

        try:
            if response['textAnnotations']:
                return response['fullTextAnnotation']['text'].split('\n')
            else:
                return None
        except Exception as e:
            print(e)
            raise SystemExit("Error")
           
    def categorise_image_by_category(image_path,lines_to_read):
        new_path=''
        results=''

        categories = folder_processes.get_all_categories(categories_txtfile)
        
        results = comparison.detect_text(str(image_path))
        not_sure_image_path = "".join ([image_folder, "/", 'not_sure_image'])
        image_with_no_text = "".join ([image_folder, "/", 'image_with_no_text'])
        break_flag = False   
        
            
        if results:
            if lines_to_read is None:
                lines_to_read = len(results)
            
            # for i,data in enumerate(results):
                
            #     #the if else below decides how many rows of the OCR data will be read
            #     if i>lines_to_read:
            #         #move image to not sure image folder if no match is found within the lines to read
            #         folder_processes.move_image_to_folder(image_path,not_sure_image_path)
            #         break
            #     else:
                    
            #         for category in categories:
            #             #code below decides how much should the similarity be.
            #             if fuzz.partial_ratio(data.lower(), category.lower())>=accuracy_percentage:
            #                 new_path = "".join ([image_folder, "/", category])
            #                 folder_processes.move_image_to_folder(image_path,new_path)
            #                 break_flag = True
            #                 break
            #         if break_flag:
            #             break
            # else:
            #     #if after all categories and results are looped no still no match, image will be moved to not sure image folder
            #     folder_processes.move_image_to_folder(image_path,not_sure_image_path) 
            results = results[:lines_to_read] 
            for category in categories:
                #code below decides how much should the similarity be.
                if process.extractOne(category.lower(), results,scorer=fuzz.partial_ratio, score_cutoff=accuracy_percentage):
                    # print(data.lower()+" "+" "+category.lower()+" "+" "+str(fuzz.partial_ratio(data.lower(), category.lower())))
                    # print(image_path)
                    new_path = "".join ([image_folder, "/", category])
                    folder_processes.move_image_to_folder(image_path,new_path)
                    break_flag = True
                    break
            else:
                #if after all categories and results are looped no still no match, image will be moved to not sure image folder
                folder_processes.move_image_to_folder(image_path,not_sure_image_path)  
        
        else:
            # if result is None, then move image to image with no text folder
            folder_processes.move_image_to_folder(image_path,image_with_no_text)                    
                         
    def multiprocessing_image_categorisation(image_folder,subProcessNumber):
        categories = folder_processes.get_all_categories(categories_txtfile)
        folder_processes.generate_folders_base_on_categories(categories)
        
        all_image_path_list = image_processes.get_all_image_path(image_folder)
        
        # nested_image_path_list = []
        # start_of_sub_list = 0
        
        # # to split the list of image paths to smaller list for async process
        # for i in range(subProcessNumber):
        #     if start_of_sub_list>=len(all_image_path_list):
        #         break
        #     end_of_sub_list = start_of_sub_list+(len(all_image_path_list)//subProcessNumber)+1
        #     nested_image_path_list.append(all_image_path_list[start_of_sub_list:end_of_sub_list])
        #     start_of_sub_list = end_of_sub_list
        Input = iter(all_image_path_list)   
        nested_image_path_list = list(iter(lambda: tuple(islice(Input, subProcessNumber)), ())) # this code seperates a large list to the small tuples of the provided size 
            
        #async process    
        for image_sub_list in nested_image_path_list:
            Pros = []
            for image_path in image_sub_list:
                p1 = multiprocessing.Process(target=comparison.categorise_image_by_category,args=(image_path,lines_to_read)) 
                Pros.append(p1)
                p1.start()
                
            for t in Pros:
                t.join()
            
        print("Image all categorised")
        






#print(comparison.detect_text('D:/g2g/canada_model/CA(for_testing)/Yukon/selfie/883190_394352_selfie.jpg'))

if __name__ == '__main__':     
    begin = time.time()
    #comparison.multiprocessing_image_categorisation(image_folder,subProcessNumber)
   
    print(comparison.detect_text('D:/g2g/canada_model/CA(for_testing)/Alberta/not_sure_image/826142_372089_selfie.jpg'))
    end = time.time()
    print(f"Total runtime of the program is {end - begin}")
