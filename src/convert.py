import tensorflow as tf
import keras
import os

MODEL_PATH = "models"

if __name__ == "__main__":  
  # Convert the model
  model = keras.models.load_model(os.path.join(MODEL_PATH, "500kb.keras"))
  converter = tf.lite.TFLiteConverter.from_keras_model(model) # path to the SavedModel directory
  # converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS]
  tflite_model = converter.convert()

  # Save the model
  with open(os.path.join(MODEL_PATH, "500kb.tflite"), 'wb') as f:
    f.write(tflite_model)