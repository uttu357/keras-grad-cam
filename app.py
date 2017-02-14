from __future__ import print_function
from shutil import copyfile
import cvfy
import subprocess
import sys
import os

app = cvfy.register('nongh:0.0.0.0:9396698:5001:9003:0.0.0.0:5001')
BASE_IMAGE_URL = './result/cam'
BASE_IMAGE_EXTENSION = '.jpg'

dir = os.path.dirname(BASE_IMAGE_URL)

try:
    os.stat(dir)
except:
    os.mkdir(dir)

@cvfy.crossdomain
@app.listen()
def getResponse():

	## recieving the images
	index = 0;
	allImage = cvfy.getImageArray()

	## processing the data
	for image in allImage:
		try:
			retcode = subprocess.call(['python', 'grad-cam.py', image])
			if retcode < 0:
	        		print('Child was terminated by signal', -retcode, file = sys.stderr)
			else:
				print('Child returned', retcode, file=sys.stderr)
		except OSError as e:
			print('Execution failed:', e, file=sys.stderr) 

		copyfile('./cam.jpg', BASE_IMAGE_URL + str(index) + BASE_IMAGE_EXTENSION)
		index = index + 1

	resultImages = []
	for num in range(0, index):
		resultImages.append(BASE_IMAGE_URL + str(num) + BASE_IMAGE_EXTENSION)

	cvfy.sendImageArray(resultImages, 'file_path')
	
	for image in resultImages:
		os.remove(image)
	
	os.remove('./cam.jpg')	
    
	return 'OK'

app.run()
