from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

model = Sequential([
    Conv2D(
        32,(3,3),
        activation='relu',
        input_shape=(32,32,3)
    ),
])
