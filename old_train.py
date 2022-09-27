import pickle #to open saved files
import time
from keras.models import Sequential
#help in creating the convulted images, maxpooling and flatten and hidden layers
#done in backend
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.callbacks import TensorBoard
import tensorboard

# TRAINING MODEL
X = pickle.load(open('X.pkl', 'rb')) #contains images (array format)
Y = pickle.load(open('Y.pkl', 'rb')) #contains label (0 or 1 for dog or cat)

X = X/225 #converting all values to smaller numbers to increase performance
print(X.shape) # (tot images, height, width, 3 colors rgb)

# STEP 1: Convulted Image
# Input image * feature detector(filter) == (0 or 1) feature map(convoluted image) ==> CONVOLUTION
# section of matrix completes a value * value of a feature detector to get 
#   either 0 or 1. This will determine what the value is on the feature map
# STEP 2: Rectifier
# have several feature maps (convolutional layer) for a specific image and 
#   process it via a rectifier to get another convulted image
# STEP 3: Max Pooling (2x2 - feature map)
# Max Pooling --> Feture map into a smaller pooled feature map (smaller image)
# STEP 4: Flatten
# Change max pooling feature map into a flat array 1 after the other
# pass to hidden layers of the neural network to produce the output (cat or dog)

model = Sequential()

model.add(Conv2D(64, (3,3), activation='relu'))
model.add(MaxPooling2D((2,2)))

#Second Copy
model.add(Conv2D(64, (3,3), activation='relu'))
model.add(MaxPooling2D((2,2)))

#Flatten
model.add(Flatten())


model.add(Dense(128, input_shape = X.shape[1:], activation='relu'))

model.add(Dense(2, activation='softmax'))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# used for results below, we are altering fit for better optimization below
# model.fit(X, Y, epochs=5, validation_split=0.1)

"""
Validation Accuracy and Losses
Results from initial run:
Epoch 1/5 (647) 
loss: 0.6551 - accuracy: 0.6218 - val_loss: 0.5950 - val_accuracy: 0.6843
Epoch 2/5 (647)
loss: 0.5384 - accuracy: 0.7303 - val_loss: 0.5360 - val_accuracy: 0.7309
Epoch 3/5 (647)
loss: 0.4460 - accuracy: 0.7893 - val_loss: 0.5136 - val_accuracy: 0.7570
Epoch 4/5 (647)
loss: 0.3477 - accuracy: 0.8462 - val_loss: 0.5491 - val_accuracy: 0.7596
Epoch 5/5 (647)
loss: 0.2148 - accuracy: 0.9126 - val_loss: 0.5897 - val_accuracy: 0.7748
Results end of part 2: Prior to optimization
"""

# OPTIMIZATION
# tensorboard --> used for visualization for models especially when having several models

NAME = f'cat-dog-prediction-{int(time.time())}'

# logs will be correctly formatted
tensorboard = TensorBoard(log_dir=f'logs\\{NAME}\\') # logs folder will hold logs of models 

# will save logs in folder logs
model.fit(X, Y, epochs=5, validation_split=0.1, batch_size=32, callbacks=tensorboard)
