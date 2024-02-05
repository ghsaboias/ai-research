import tensorflow as tf

# Load the dataset
mnist = tf.keras.datasets.mnist

# Split the dataset into training and testing
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalize the data
x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)

# Create the model
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))

# Add another layer
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))

# Add the output layer
model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax)) # softmax outputs a probability distribution

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(x_train, y_train, epochs=5)

# Evaluate the model
val_loss, val_acc = model.evaluate(x_test, y_test)
print("val_loss:", val_loss, "val_acc:", val_acc)

# Save the model
model.save('handwriting.model')

# Load the model
new_model = tf.keras.models.load_model('handwriting.model')

# Make predictions
predictions = new_model.predict(x_test)

# Print the predictions
import numpy as np
print("np.argmax(predictions[0]):", np.argmax(predictions[0]))
print("np.argmax(predictions[1]):", np.argmax(predictions[1]))

# Display the image
import matplotlib.pyplot as plt
plt.imshow(x_test[0], cmap=plt.cm.binary)
plt.imshow(x_test[1], cmap=plt.cm.binary)

# Show the image
plt.show()