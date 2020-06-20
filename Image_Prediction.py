import cv2
from keras.models import load_model
import numpy as np
from keras.preprocessing import image

class Prediction:
	def __init__(self,model_name):
		self.model=load_model(model_name)

	def load_model(self):
		self.model.compile(loss='categorical_crossentropy',
			optimizer='rmsprop',metrics=['accuracy'])

	def predict(self,img):
		x = image.img_to_array(img)
		x = np.expand_dims(x, axis=0)
		classes = self.model.predict_classes(x, batch_size=10)
		return classes

