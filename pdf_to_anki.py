import cv2
import numpy as np
import os
import time
from glob import glob

import pdf2image
from pdf2image import convert_from_path as cfp
import time



try:
	os.mkdir("images")
except:
	pass

try:
	os.mkdir("images_final")
except:
	pass
	
def convert_to_image(path_to_pdf , deck_name):
	print("Starting to load pdf")
	images = cfp(path_to_pdf)
	print("pdf loaded to memory")

	for i in range(len(images)):
		images[i].save("./images/" +deck_name + str(i) + str(time.time()) + ".jpg" , "JPEG" )
		if i % 10 == 0:
			print("saved" , i)


convert_to_image( "sample.pdf" , "deck_name" )


file_list = glob('./images/*.jpg')
#print(file_list)

rand_int = time.time()
rand_int = round(rand_int)


complete_list = []


import ntpath

direct_copy = True

#direct_path = "./home/amritpal/.local/share/Anki2/User 1/collection.media/"


for filename in file_list: 
	#filename = './images/Flashcards-0.jpg'
	image = cv2.imread(filename)

	def crop_doublet_anki_notes(image , x , y):
		a = int(x*(image.shape[0])/(x+y))
		img1 = image[ 0:a , 0:image.shape[0]]
		img2 = image[ a:image.shape[0] , 0:image.shape[0] ]
		return(img1 , img2 )

	img1 , img2 = crop_doublet_anki_notes(image , 14,13.5)

	#print(img1)
	#print(type(img1))
	filename = ntpath.basename(filename)

	a1 = filename[0:-4] + str(rand_int) + "_01" + ".jpg"
	a2 = filename[0:-4] + str(rand_int) + "_02" + ".jpg"
	name1 = "<img src='" + a1 + "'>"
	name2 = "<img src='" + a2 + "'>"
	cv2.imwrite( "./images_final/" + a1 , img1)
	cv2.imwrite("./images_final/" + a2 , img2) 
	#print("./images_final/" + a1 )
	
	complete_list.append([name1 , name2])

import pandas as pd
df = pd.DataFrame(complete_list)
#print(df)

df.to_csv("output.csv", index = None,header=False)

