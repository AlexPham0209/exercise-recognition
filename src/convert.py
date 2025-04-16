import tensorflow as tf
import keras
import os

MODEL_PATH = "model_path"

# Convert the model
model = keras.models.load_model("model_data/best_smaller.keras")
converter = tf.lite.TFLiteConverter.from_keras_model(model) # path to the SavedModel directory
# converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS]
tflite_model = converter.convert()

# Save the model
with open('model_data/model_smaller.tflite', 'wb') as f:
  f.write(tflite_model)