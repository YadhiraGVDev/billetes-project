import os
import numpy as np
import tensorflow as tf
from PIL import Image
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, 'detector', 'ml_models', 'modelo_billetes.tflite')
LABELS_PATH = os.path.join(settings.BASE_DIR, 'detector', 'ml_models', 'labels.txt')

try:
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print("Modelo TFLite cargado correctamente.")
except Exception as e:
    print(f"Error al cargar el modelo TFLite: {e}")
    interpreter = None

CLASS_NAMES = []
if os.path.exists(LABELS_PATH):
    with open(LABELS_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                CLASS_NAMES.append(line.strip().split(' ', 1)[-1])
if not CLASS_NAMES:
    CLASS_NAMES = ['20', '50', '100', '200', '500', '1000']

def predict_bill(image_path):
    if interpreter is None:
        return "Error: Modelo no cargado", 0.0

    try:
        img = Image.open(image_path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        if img.height > img.width:
            img = img.rotate(90, expand=True)

        img = img.resize((224, 224)) 
        
        input_dtype = input_details[0]['dtype']
        if input_dtype == np.uint8:
            img_array = np.array(img, dtype=np.uint8)
        else:
            img_array = np.array(img, dtype=np.float32) / 255.0
            
        img_array = np.expand_dims(img_array, axis=0)

        interpreter.set_tensor(input_details[0]['index'], img_array)
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]['index'])
        
        predicted_class_index = np.argmax(predictions[0])
        
        # Calcular la confianza (siempre multiplicar por 100)
        raw_confidence = float(np.max(predictions[0]))
        confidence = raw_confidence * 100
        
        # Asegurarnos de que no pase de 100
        if confidence > 100:
            confidence = 100.0

        denominacion = CLASS_NAMES[predicted_class_index]
        denominacion = "".join(c for c in denominacion if c.isdigit())
        
        return f"{denominacion} MXN", round(confidence, 1)

    except Exception as e:
        import traceback
        print("Error en la predicción:")
        traceback.print_exc()
        return "Error al procesar", 0.0
