import tensorflow as tf
import keras
import os

MODEL_PATH = "model_path"

# Convert the model
model = keras.models.load_model("model_data/best.keras")
converter = tf.lite.TFLiteConverter.from_keras_model(model) # path to the SavedModel directory
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]
tflite_model = converter.convert()

# Save the model
with open('model_data/model.tflite', 'wb') as f:
  f.write(tflite_model)