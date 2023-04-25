import cv2
import numpy as np
from pyzbar.pyzbar import decode
import datetime
import csv

cap = cv2.VideoCapture(0);
cap.set(3, 640)
cap.set(4, 480)

with open('list.txt') as f:
	mydataList = f.read().splitlines()	


csv_file_path = 'data.csv'

recorded_qr_codes = set()


while True:
	success, img = cap.read()
	for barcode in decode(img):
		# print(barcode.data)
		mydata = barcode.data.decode('utf-8')

		wanted = mydata.splitlines()
		displayData = wanted[0]

		print(mydata)

		if displayData in mydataList and displayData not in recorded_qr_codes:
			myOut = 'Available'
			myColor = (0, 255, 0)

			with open(csv_file_path, 'a') as csv_file:
				writer = csv.writer(csv_file)
				now = datetime.datetime.now()
				timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
				writer.writerow([displayData, timestamp])

			recorded_qr_codes.add(displayData)

		else:
			myOut = 'Non Available'
			myColor = (0, 0, 255)

		pts = np.array([barcode.polygon], np.int32)
		pts = pts.reshape((-1, 1, 2))
		cv2.polylines(img, [pts], True, (255, 0, 0), 5)
		pts2 = barcode.rect
		cv2.putText(img, myOut, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0),2)

	cv2.imshow('Preview', img)
	cv2.waitKey(1)