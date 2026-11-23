import os
import threading
import numpy as np

from PIL import Image, ImageOps
from django.conf import settings
from ai_edge_litert.interpreter import Interpreter

MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "detector",
    "ml_models",
    "modelo_billetes_mobilenetv2_2026.tflite"
)

LABELS_PATH = os.path.join(
    settings.BASE_DIR,
    "detector",
    "ml_models",
    "labels.txt"
)

EXPECTED_CLASSES = ["20", "50", "100", "200", "500", "nada"]

interpreter = None
input_details = None
output_details = None
model_lock = threading.Lock()

try:
    interpreter = Interpreter(
        model_path=MODEL_PATH,
        num_threads=1
    )
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    if tuple(input_details[0]["shape"]) != (1, 224, 224, 3):
        raise ValueError("Forma de entrada incorrecta")

    if output_details[0]["shape"][-1] != 6:
        raise ValueError("El modelo no tiene seis salidas")

    print("Modelo MobileNetV2 2026 cargado correctamente.")

except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    interpreter = None
    input_details = None
    output_details = None


CLASS_NAMES = []

if os.path.exists(LABELS_PATH):
    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                parts = line.strip().split(maxsplit=1)
                label = parts[-1].strip()

                if label.lower().startswith("class "):
                    label = label[6:].strip()

                CLASS_NAMES.append(label)

if CLASS_NAMES != EXPECTED_CLASSES:
    print("Error: las etiquetas no coinciden con el modelo.")
    interpreter = None


def predict_bill(image_path):

    if interpreter is None:
        return "Error: Modelo no cargado", 0.0

    try:
        with Image.open(image_path) as original:
            img = ImageOps.exif_transpose(original).convert("RGB")

        if img.height > img.width:
            rotated = img.rotate(90, expand=True)
            img.close()
            img = rotated

        resized = img.resize(
            (224, 224),
            Image.Resampling.BILINEAR
        )
        img.close()

        # IMPORTANTE:
        # El entrenamiento utiliza valores RGB de 0 a 255.
        # La normalizacion [-1, 1] ya esta dentro del modelo.
        img_array = np.asarray(
            resized,
            dtype=np.float32
        )
        resized.close()

        img_array = np.expand_dims(img_array, axis=0)

        with model_lock:
            interpreter.set_tensor(
                input_details[0]["index"],
                img_array
            )

            interpreter.invoke()

            predictions = interpreter.get_tensor(
                output_details[0]["index"]
            )

        output_scale, output_zero_point = (
            output_details[0]["quantization"]
        )

        if predictions.dtype in (np.uint8, np.int8):
            probabilities = (
                predictions[0].astype(np.float32) - output_zero_point
            ) * output_scale
        else:
            probabilities = predictions[0].astype(np.float32)

        if not np.all(np.isfinite(probabilities)):
            return "Error: Prediccion invalida", 0.0

        predicted_index = int(np.argmax(probabilities))

        if predicted_index >= len(CLASS_NAMES):
            return "Error: Clase desconocida", 0.0

        confidence = float(
            np.clip(probabilities[predicted_index], 0.0, 1.0)
        ) * 100

        denomination = CLASS_NAMES[predicted_index]

        if denomination.lower() == "nada":
            return "No se detecto un billete valido", round(confidence, 1)

        denomination = "".join(
            character for character in denomination
            if character.isdigit()
        )

        if not denomination:
            return "Error: Etiqueta invalida", 0.0

        return f"{denomination} MXN", round(confidence, 1)

    except Exception as e:
        print(f"Error en la prediccion: {e}")
        return "Error al procesar", 0.0
