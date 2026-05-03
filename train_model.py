import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

IMG_SIZE = 128
BATCH_SIZE = 32

# 🔥 Data generator
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train = train_datagen.flow_from_directory(
    "dataset",
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',   # 🔥 IMPORTANT
    subset='training'
)

val = train_datagen.flow_from_directory(
    "dataset",
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# 🔥 Check labels (VERY IMPORTANT)
print("Class indices:", train.class_indices)

# 🔥 Model
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
    MaxPooling2D(2,2),

    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),

    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(2,2),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),

    Dense(2, activation='softmax')  # 🔥 KEY CHANGE
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',   # 🔥 match softmax
    metrics=['accuracy']
)

# 🔥 Train
model.fit(
    train,
    validation_data=val,
    epochs=10
)

# 🔥 Save model
model.save("mask_model.h5")

print("✅ Model trained and saved")