# Traffic

An AI to identify which traffic sign appears in a photograph.

This is a summary of all different parameters that have been applied to my model.

In most cases, the model has the following structure:

1. Conv2D layer, ReLU activation
2. MaxPooling2D, 2x2 kernel
3. Hidden layer, ReLU activation, 0.3 dropout
4. Output layer, Softmax activation

Most of the effort was finding out the optimal configuration for the number of
filters in the 1st layer (Conv2D) and its kernel size. 

## Background

As research continues in the development of self-driving cars, one of the key challenges is computer vision,
allowing these cars to develop an understanding of their environment from digital images. In particular, this
involves the ability to recognize and distinguish road signs – stop signs, speed limit signs, yield signs, and more.

In this project, you’ll use TensorFlow to build a neural network to classify road signs based on an image of
those signs. To do so, you’ll need a labeled dataset: a collection of images that have already been categorized
by the road sign represented in them.

Several such data sets exist, but for this project, we’ll use the German Traffic Sign Recognition Benchmark (GTSRB)
dataset, which contains thousands of images of 43 different kinds of road signs.

## Getting Started

- Download the [data set](https://cdn.cs50.net/ai/2020/x/projects/5/gtsrb.zip) for this project and unzip it. Move the resulting gtsrb directory inside of your traffic directory.

- In windows 10, inside of the traffic directory, `run pip install -r requirements.txt` to install this project’s dependencies:
  opencv-python for image processing, scikit-learn for ML-related functions, and tensorflow for neural networks.

## Usage
```bash
$ python traffic.py gtsrb/
Epoch 1/10
500/500 [==============================] - 56s 106ms/step - loss: 2.9349 - accuracy: 0.2015
Epoch 2/10
500/500 [==============================] - 62s 123ms/step - loss: 1.2906 - accuracy: 0.5711
Epoch 3/10
500/500 [==============================] - 56s 112ms/step - loss: 0.6995 - accuracy: 0.7733
Epoch 4/10
500/500 [==============================] - 55s 110ms/step - loss: 0.3827 - accuracy: 0.8843
Epoch 5/10
500/500 [==============================] - 55s 110ms/step - loss: 0.2714 - accuracy: 0.9217
Epoch 6/10
500/500 [==============================] - 53s 106ms/step - loss: 0.2282 - accuracy: 0.9376
Epoch 7/10
500/500 [==============================] - 51s 103ms/step - loss: 0.1937 - accuracy: 0.9484
Epoch 8/10
500/500 [==============================] - 52s 105ms/step - loss: 0.1648 - accuracy: 0.9565
Epoch 9/10
500/500 [==============================] - 53s 105ms/step - loss: 0.1623 - accuracy: 0.9590
Epoch 10/10
500/500 [==============================] - 51s 102ms/step - loss: 0.1610 - accuracy: 0.9603
333/333 - 5s - loss: 0.0411 - accuracy: 0.9881 - 5s/epoch - 16ms/step
```

## Result
The final result is average 0.9881 accuracy.