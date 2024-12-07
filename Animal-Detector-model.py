from keras.src.applications import VGG16
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator

data_dir = "animal_data"
class_names = ["Bear", "Bird", "Cat", "Cow", "Deer", "Dog", "Dolphin", "Elephant", "Giraffe", "Horse", "Kangaroo", "Lion", "Panda", "Tiger", "Zebra"]

# Image parameters
img_height, img_width = 224, 224
batch_size = 32

datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_data_gen = datagen.flow_from_directory(
    data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

validation_data_gen = datagen.flow_from_directory(
    data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

base_model = VGG16(input_shape=(img_height, img_width, 3), include_top=False, weights='imagenet')
base_model.trainable = False

model = Sequential([
    base_model,
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(len(class_names), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

lr_reduction = ReduceLROnPlateau(monitor='val_loss', patience=3, factor=0.5, min_lr=1e-6)
early_stopping = EarlyStopping(monitor='val_loss', patience=5)

history = model.fit(
    train_data_gen,
    epochs=50,
    validation_data=validation_data_gen,
    callbacks=[early_stopping, lr_reduction]
)

loss, accuracy = model.evaluate(validation_data_gen)
print(f"Validation accuracy: {accuracy * 100:.2f}%")

model.save("animal_classifier_model.keras")