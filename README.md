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

Ejemplo:
```bash
faas-cli up -f stack.yaml

echo "https://media.istockphoto.com/id/1368965646/es/foto/chicos-y-chicas-multi%C3%A9tnicos-que-se-toman-selfies-al-aire-libre-con-luz-de-fondo-concepto-de.jpg?s=612x612&w=0&k=20&c=QC9JqaBFDnZZtwutt6bvGFLXmmtbv9e355syXsG39KE=" | faas-cli invoke facesdetection-python > output_base64.txt

cat output_base64.txt | base64 -d > result.jpg
```
