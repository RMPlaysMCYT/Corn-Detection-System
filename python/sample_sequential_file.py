from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

model = Sequential([
    Conv2D(
        32,(3,3),
        activation='relu',
        input_shape=(32,32,3)
    ),

    MaxPooling2D((2,2)),
    Conv2D(
        64,(3,3),
        activation='relu'
    ),

    MaxPooling2D((2,2)),
    Conv2D(128,(3,3),activation='relu'),
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(10,activation='softmax')
])


