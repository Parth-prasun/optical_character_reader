from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PIL import Image
import pytesseract
import cv2
import os
from fileupload.settings import MEDIA_ROOT


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Create your views here.

def index(request):
    return render(request,'basicapp/index.html')

def upload(request):
    if request.method=='POST':
        uploaded_file=request.FILES['document']
        fs= FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        imad=os.path.join(MEDIA_ROOT,uploaded_file.name)
        image = cv2.imread(imad)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


        gray = cv2.threshold(gray, 0, 255,
		    cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


        gray = cv2.medianBlur(gray, 3)

        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, gray)


        text = pytesseract.image_to_string(Image.open(filename))
        os.remove(filename)
        return render(request,'basicapp/answer.html',{'text':text})

        # print(text)
        # text_file = open("target.txt", "w")
        # n = text_file.write(text)
        # text_file.close()
            
            
            

        
    return render(request,'basicapp/upload.html')
