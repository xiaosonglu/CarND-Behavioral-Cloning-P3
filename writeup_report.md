#**Behavioral Cloning** 


---

**Behavioral Cloning Project**

The goals / steps of this project are the following:
* Use the simulator to collect data of good driving behavior
* Build a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road
* Summarize the results with a written report


[//]: # (Image References)

[image1]: ./examples/center.jpg
[image2]: ./examples/center_1.jpg "Recovery Image"
[image3]: ./examples/center_2.jpg "Recovery Image"
[image4]: ./examples/center_3.jpg "Recovery Image"
[image5]: ./examples/center_4.jpg "Normal Image"
[image6]: ./examples/center_4_flip.png "Flipped Image"

## Rubric Points
###Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/432/view) individually and describe how I addressed each point in my implementation.  

---
###Files Submitted & Code Quality

####1. Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* model.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
* model.h5 containing a trained convolution neural network 
* writeup_report.md summarizing the results

####2. Submission includes functional code
Using the Udacity provided simulator and drive.py file, the car can be driven autonomously around the track by executing 
```
python drive.py model.h5
```

####3. Submission code is usable and readable

The model.py file contains the code for training and saving the convolution neural network. The file shows the pipeline I used for training and validating the model, and it contains comments to explain how the code works.

###Model Architecture

####1. An appropriate model architecture has been employed

My model implements an NVIDIA architecture which consists of the following layers (model.py lines 48-61)

| Layer         		|     Description	        					| 
|:---------------------:|:---------------------------------------------:| 
| Input         		| 160x320x3 RGB image   						|
| Lambda         		| image normalization   						|
| Cropping         		| 70 from the top and 25 from the botttom  		|
| Convolution 5x5     	| 24 filters, 2x2 stride, valid padding        	|
| RELU					|												|
| Convolution 5x5     	| 36 filters, 2x2 stride, valid padding       	|
| RELU					|												|
| Convolution 5x5     	| 48 filters, 2x2 stride, valid padding       	|
| RELU					|												|
| Convolution 3x3     	| 64 filters, 1x1 stride, valid padding       	|
| RELU					|												|
| Convolution 3x3     	| 64 filters, 1x1 stride, valid padding     	|
| RELU					|												|
| Flatten				|												|
| Fully connected		| outputs 100        							|
| Fully connected		| outputs 50        							|
| Fully connected		| outputs 10        							|
| Fully connected		| outputs 1        			    				|


####2. Attempts to reduce overfitting in the model

The model was trained and validated on different data sets to ensure that the model was not overfitting (code line 66). The model was tested by running it through the simulator and ensuring that the vehicle could stay on the track.

####3. Model parameter tuning

The model used an adam optimizer, so the learning rate was not tuned manually (model.py line 63).

####4. Appropriate training data

Training data was chosen to keep the vehicle driving on the road. I used a combination of center lane driving,  recovering from the sides of the road and extra driving specifically around curves.

For details about how I created the training data, see the next section. 

###Creation of the Training Set & Training Process

To capture good driving behavior, I first recorded two laps on track one using center lane driving. Here is an example image of center lane driving:

![alt text][image1]

I then recorded the vehicle recovering from the sides of the road back to center so that the vehicle would learn to turn back to center when driving too close to the sides. These images show what a recovery looks like starting from left sides of the road and driving back to center :

![alt text][image2]
![alt text][image3]
![alt text][image4]

I recorded the recovering behavior specifically on curves for several laps in order to get more data points on curves.

I used all three camera images (center, left and right) to train the model. The steering measurement for left camera will be adjusted by adding 0.2 and the steering measurement for right camera will be adjusted by subtracting 0.2. 
To augment the data set, I also flipped images. For example, the images below are the normal image and the flipped image:

![alt text][image5]
![alt text][image6]

After the collection process, I had 5694 number of data points. I then added the flipped images with the total of 11388 data points. Then the data was preprocessed by a lambda layer to perform image normalization.

I finally randomly shuffled the data set and put 20% of the data into a validation set. 

I used this training data for training the model. The validation set helped determine if the model was over or under fitting. The  number of epochs was 4 and I used an adam optimizer so that manually training the learning rate wasn't necessary.

After training, the saved model.h5 was loaded to the simulator by executing 
```
python drive.py model.h5 run1
```
and a video was created by executing
```
python video.py run1
```
The recorded video was renamed as "video.mp4". The video shows that the vehicle is able to drive autonomously around the track without leaving the drivable portion of the track surface.