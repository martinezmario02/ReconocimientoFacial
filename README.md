# Práctica 2: Implementación del reconocimiento facial mediante funciones como servicio

**Mario Martínez Sánchez**

## Configuración de la plataforma para el servicio de funciones FaaS en OpenFaaS

Para esta práctica se ha utilizado **OpenFaaS** como plataforma FaaS desplegada sobre **Kubernetes** con ayuda de **Minikube** y **Arkade**.

### Requisitos previos

- Tener `minikube` instalado y funcionando
- Tener `kubectl` instalado
- Tener `arkade` instalado
- Tener `faas-cli` instalado

### Pasos seguidos (siguiendo la sesión 7 de la asignatura):

1. Instalación de OpenFaaS y faas-cli.
2. Conectarse a Docker Hub

## Implementación de la función de detección facial

### Lenguaje y plantilla utilizados

- Lenguaje: **Python 3**
- Plantilla personalizada: `python3-flask-debian`

### Descripción de la función

La función `facesdetection-python`:

- Recibe una imagen mediante una **URL** proporcionada en la solicitud.
- Descarga y procesa la imagen utilizando OpenCV.
- Detecta rostros mediante un modelo Haar Cascade.
- Dibuja rectángulos sobre los rostros encontrados.
- Devuelve la imagen resultante codificada en **Base64**.

En el archivo `requirements.txt` se estableció el siguiente módulo:
- opencv-python-headless

## Despliegue de la función con OpenFaaS
1. Construcción y subida de la imagen.
```bash
faas-cli build -f stack.yaml
```
2. Invocación de la función.
```bash
echo "URL_IMAGEN" | faas-cli invoke facesdetection-python > output_base64.txt
```
3. Obtención de la imagen resultante
```bash
cat output_base64.txt | base64 -d > result.jpg
```

## Mejoras con redes neuronales

El enfoque anterior tiene limitaciones, especialmente en términos de precisión y capacidad para detectar rostros en diversas condiciones. En la nueva implementación, se reemplaza el modelo de Haar Cascade por una red neuronal convolucional (CNN), que ha sido entrenada previamente utilizando un modelo de la red neuronal ResNet, preentrenado con el framework Caffe.

### Beneficios conseguidos al usar CNN

Las redes neuronales convolucionales son especialmente eficaces en tareas de visión por computadora, como la detección de rostros, debido a sus propiedades de generalización y aprendizaje jerárquico de características espaciales en las imágenes. A diferencia de los enfoques tradicionales que requieren una manual selección de características (como en el caso de Haar Cascade), las CNN aprenden automáticamente las características relevantes del rostro durante el proceso de entrenamiento, lo que resulta en una mayor precisión y robustez.

### Despliegue de la función con CNN
1. Construcción y subida de la imagen.
```bash
faas-cli build -f stack.yaml
```
2. Invocación de la función.
```bash
echo "URL_IMAGEN" | faas-cli invoke facesdetection-cnn > output_base64.txt
```
3. Obtención de la imagen resultante
```bash
cat output_base64.txt | base64 -d > result.jpg
```

## Ejemplo

### Ejecución del modelo inicial

```bash
faas-cli up -f stack.yaml

echo "https://media.istockphoto.com/id/1368965646/es/foto/chicos-y-chicas-multi%C3%A9tnicos-que-se-toman-selfies-al-aire-libre-con-luz-de-fondo-concepto-de.jpg?s=612x612&w=0&k=20&c=QC9JqaBFDnZZtwutt6bvGFLXmmtbv9e355syXsG39KE=" | faas-cli invoke facesdetection-python > output_base64.txt

cat output_base64.txt | base64 -d > result.jpg
```

![result](https://github.com/user-attachments/assets/f32c5da8-63d1-4c3d-b68c-562594920a3f)


### Ejecución del modelo usando CNN

```bash
faas-cli up -f stack.yaml

echo "https://media.istockphoto.com/id/1368965646/es/foto/chicos-y-chicas-multi%C3%A9tnicos-que-se-toman-selfies-al-aire-libre-con-luz-de-fondo-concepto-de.jpg?s=612x612&w=0&k=20&c=QC9JqaBFDnZZtwutt6bvGFLXmmtbv9e355syXsG39KE=" | faas-cli invoke facesdetection-cnn > output_base64.txt

cat output_base64.txt | base64 -d > result.jpg
```

![result](https://github.com/user-attachments/assets/a26c0aca-9ac2-4706-92f0-776fa3c57580)

Como se puede observar en los resultados obtenidos, la implementación basada en redes neuronales convolucionales (CNN) muestra una mejora significativa en la detección facial en comparación con el modelo inicial basado en Haar Cascade. En la primera versión, el sistema logró identificar correctamente a 5 de los 6 individuos presentes en la imagen, presentando además una detección errónea en la que uno de los rostros fue segmentado en dos. Por el contrario, con el modelo basado en CNN, se logró detectar con precisión a los 6 integrantes sin errores de segmentación, lo que evidencia una mayor robustez y exactitud del nuevo enfoque.
