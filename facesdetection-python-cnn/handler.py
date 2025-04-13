import os
import cv2
import base64
import numpy as np
from urllib.request import urlopen

def handle(req):
    # Obtener la imagen desde la URL
    img_from_url = urlopen(req)
    img = cv2.imdecode(np.asarray(bytearray(img_from_url.read()), dtype=np.uint8), cv2.IMREAD_COLOR)
    
    # Cargar el modelo
    prototxt_file = os.environ.get('PROTOTXT_FILE')
    caffe_model_file = os.environ.get('CAFFE_MODEL_FILE')
    net = cv2.dnn.readNetFromCaffe(prototxt_file, caffe_model_file)
    
    # Obtener las dimensiones de la imagen
    h, w = img.shape[:2]
    
    # Preprocesar la imagen antes de enviarla a la red neuronal
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (600, 600)), 1.0, (600, 600), (104.0, 177.0, 123.0))
    
    # Configurar la entrada de la red neuronal
    net.setInput(blob)
    
    # Realizar las detecciones de las caras
    detections = net.forward()

    # Dibujar rectángulos alrededor de las caras detectadas
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence >= 0.85:  
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(img, (startX, startY), (endX, endY), (0, 0, 255), 2)  # Rectángulo rojo

    # Codificar la imagen resultante 
    _, imagen_jpeg = cv2.imencode('.jpeg', img)
    imagen_base64 = base64.b64encode(imagen_jpeg).decode('utf-8')
    return imagen_base64
