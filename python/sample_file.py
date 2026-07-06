#### This is a sample file to test my neovim skill at least, go F the purist/haters, pick a tool to perform well
#### This must not be Neovim vs VSCode or any as long as it delivers the job


import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.preprocessing.image import ImageDataGenerator

(x_train, y_train), (x_test, y_test) = cifar10.load_data()

x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0
