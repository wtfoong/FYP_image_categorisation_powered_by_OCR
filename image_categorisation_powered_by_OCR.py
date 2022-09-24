import io
import json
import multiprocessing
import os
import time

from backend.image_processes import image_processes
from backend.folder_processes import folder_processes
from rapidfuzz import fuzz,process
from itertools import islice

from google.cloud import vision
from google.cloud.vision_v1 import AnnotateImageResponse

########################################## User input data ##############################################################################

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/rainy/OneDrive - Asia Pacific University/FYP/fypSystem/thinking-avenue-356203-9d7d01f4e556.json"

image_folder = 'D:/g2g/canada_model/CA(for_testing)/Alberta' #insert the file path to the images here.

categories_txtfile = None  # insert the path to the txt file that stores all the categories for the images.

#the number of subprocesses allowed
subProcessNumber=20

#the number of lines of the OCR result that should be read for comparison, if not sure just put None
lines_to_read = 7

#the percentage of accuracy the OCR result need to be with the category provided.
accuracy_percentage = 60

############################################################################################################################################

class comparison:
    def detect_text(path):
        """Detects text in the image."""
        try:
            client = vision.ImageAnnotatorClient()

            with io.open(path, 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)


            response = client.document_text_detection(image=image,image_context={"language_hints": ["id"]})
            response_json = AnnotateImageResponse.to_json(response)
            response = json.loads(response_json)
            if response['textAnnotations']:
                return response['fullTextAnnotation']['text'].split('\n')
            else:
                return None
        except:
            #print(e)
            raise 
           
    def categorise_image_by_category(image_path,lines_to_read,categories_txtfile,image_folder,accuracy_percentage,q):
        new_path=''
        results=''

        categories = folder_processes.get_all_categories(categories_txtfile)
        try:
            results = comparison.detect_text(str(image_path))
        except Exception as e:
            q.put(e)
            return e
        not_sure_image_path = "".join ([image_folder, "/", 'not_sure_image'])
        image_with_no_text = "".join ([image_folder, "/", 'image_with_no_text'])  
        
            
        if results and len(results)>2:
            if lines_to_read is None or lines_to_read==0:
                lines_to_read = len(results)
            results = results[:lines_to_read] 
            for category in categories:
                #code below decides how much should the similarity be.
                if process.extractOne(category.lower(), results,scorer=fuzz.partial_ratio, score_cutoff=accuracy_percentage):
                    # print(data.lower()+" "+" "+category.lower()+" "+" "+str(fuzz.partial_ratio(data.lower(), category.lower())))
                    # print(image_path)
                    new_path = "".join ([image_folder, "/", category])
                    folder_processes.move_image_to_folder(image_path,new_path)
                    break
            else:
                #if after all categories and results are looped no still no match, image will be moved to not sure image folder
                folder_processes.move_image_to_folder(image_path,not_sure_image_path)  
        
        else:
            # if result is None, then move image to image with no text folder
            folder_processes.move_image_to_folder(image_path,image_with_no_text)      
        q.put(False)              
                         
    def multiprocessing_image_categorisation(image_folder,subProcessNumber,categories_txtfile,lines_to_read,accuracy_percentage,signal):
        categories = folder_processes.get_all_categories(categories_txtfile)
        folder_processes.generate_folders_base_on_categories(categories,image_folder)
        flag = True
        error = None
        
        all_image_path_list = image_processes.get_all_image_path(image_folder)
        
        try:
            results = comparison.detect_text(str(all_image_path_list[0]))
        except Exception as e:
            return e
        
        Input = iter(all_image_path_list)   
        nested_image_path_list = list(iter(lambda: tuple(islice(Input, subProcessNumber)), ())) # this code seperates a large list to the small tuples of the provided subProcessNumber 
        totalProcess = len(nested_image_path_list)   
        #async process    
        for i,image_sub_list in enumerate(nested_image_path_list) :
            Pros = []
            q = multiprocessing.Queue()
            for image_path in image_sub_list:
                p1 = multiprocessing.Process(target=comparison.categorise_image_by_category,args=(image_path,lines_to_read,categories_txtfile,image_folder,accuracy_percentage,q)) 
                Pros.append(p1)
                p1.start()
                
            
            for p in Pros:
                if q.get():
                    error = q.get()
                    flag = False
                    break
                       
            if not flag:
                for z in Pros:
                    z.kill()           
                   
            for t in Pros: 
                t.join()
                
            try:
                signal.emit(i, totalProcess)
            except Exception as e:
                print(e)
                pass
            
           
        if not flag:    
            return error
        else: return None
        


if __name__ == '__main__':     
    begin = time.time()
    comparison.multiprocessing_image_categorisation(image_folder,subProcessNumber,categories_txtfile,lines_to_read,accuracy_percentage)
   
    #print(comparison.detect_text('D:/g2g/canada_model/CA(for_testing)/Alberta/not_sure_image/747427_340815.jpg'))
    end = time.time()
    print(f"Total runtime of the program is {end - begin}")
