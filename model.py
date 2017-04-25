import csv
import cv2
import numpy as np
lines = []
with open('./data/driving_log.csv') as csvfile:
	reader = csv.reader(csvfile)
	for line in reader:
		lines.append(line)
		
images = []
measurements = []

for line in lines:
    # use all three camera images to train the model
	for i in range(3):
		source_path = line[i]
		filename = source_path.split('\\')[-1]
		current_path = './data/IMG/' + filename
		image = cv2.imread(current_path)
		images.append(image)
		# create adjusted steering measurements for the side camera images
		# left camera + 0.2 and right camera - 0.2
		if i == 0:
			measurement = float(line[3])
		elif i == 1:
			measurement = float(line[3]) + 0.2
		elif i == 2:
			measurement = float(line[3]) - 0.2
		measurements.append(measurement)
### Data augmentation by flipping images and steering measurements.
augmented_images, augmented_measurements = [], []
for image,measurement in zip(images, measurements):
	augmented_images.append(image)
	augmented_measurements.append(measurement)
	augmented_images.append(cv2.flip(image,1))
	augmented_measurements.append(measurement*-1.0)
		
X_train = np.array(augmented_images)
y_train = np.array(augmented_measurements)

from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, Cropping2D
from keras.layers import Convolution2D
from keras.layers.pooling import MaxPooling2D

model = Sequential()
# a lambda layer is used for image normalization.
model.add(Lambda(lambda x: x/255.0 - 0.5, input_shape=(160,320,3)))
# a cropping layer to crop the input images.
model.add(Cropping2D(cropping=((70,25),(0,0))))
# a NVIDIA architecture
model.add(Convolution2D(24,5,5,subsample=(2,2),activation="relu"))
model.add(Convolution2D(36,5,5,subsample=(2,2),activation="relu"))
model.add(Convolution2D(48,5,5,subsample=(2,2),activation="relu"))
model.add(Convolution2D(64,3,3,activation="relu"))
model.add(Convolution2D(64,3,3,activation="relu"))
model.add(Flatten())
model.add(Dense(100))
model.add(Dense(50))
model.add(Dense(10))
model.add(Dense(1))

model.compile(loss='mse',optimizer='adam')
# the last 20% of the data for validation 
# the data will be randomly shuffled at each epoch
model.fit(X_train, y_train, validation_split=0.2, shuffle=True, nb_epoch=4)

model.save('model.h5')
exit()
