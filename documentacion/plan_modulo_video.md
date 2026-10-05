# Plan Estratégico y Técnico: Módulo de Generación de Video Audiovisual para ADES.CLOUD

> **Proyecto:** BrainPolitics  
> **Institución:** Centro de Estudios e Investigación Marxista ADES.CLOUD  
> **Módulo:** `video/` (Arquitectura Dual-Runtime: Brain / Nerve)  
> **Formato de Salida:** Video de Alta Calidad para YouTube (1080p Full HD / 16:9)  
> **Enlace Institucional de Cierre:** `https://ades.cloud`

---

## 1. Fundamentación y Objetivos del Módulo

El objetivo central de este módulo es transformar documentos y ensayos teóricos de economía política, materialismo histórico e investigaciones socioeconómicas en **video-ensayos documentales y piezas de divulgación audiovisual de calidad profesional**.

La divulgación contemporánea del pensamiento crítico exige una presencia activa en plataformas como YouTube, evitando tanto la banalización del contenido como la simple lectura estática de diapositivas. Para ello, el sistema automatiza la producción audiovisual mediante:

1. **Estructuración Dialéctica del Guión:** Conversión de la densidad abstracta del texto en una secuencia lógica de exposición (ascenso de lo abstracto a lo concreto).
2. **Modelado Numérico de Tiempos y Ritmo (Brain):** Uso de NumPy para calcular dinámicamente el tiempo de exposición por escena según palabras por minuto (WPM), densidad conceptual y pausas de asimilación.
3. **Curaduría Fotográfica Documental:** Localización e inserción exclusiva de fotografías reales, de archivo histórico, documental y periodístico, descartando taxativamente ilustraciones, dibujos y caricaturas.
4. **Cinemática y Ensamblado Profesional (Nerve):** Animación de imágenes mediante paneo y zoom suave (efecto Ken Burns), superposición tipográfica sobria de citas y conceptos, y codificación en formato estándar de YouTube (16:9, 1080p, H.264/AAC).
5. **Cierre Institucional Obligatorio:** Todo video concluye con un Outro formal que invita a la audiencia a consultar la totalidad de los escritos en **https://ades.cloud**.

---

## 2. Arquitectura 'Dual-Runtime' del Módulo

Siguiendo el principio arquitectónico del proyecto, el código se estructura en Python 3.11+ para la lógica y NumPy para el procesamiento numérico y temporal:

```
video/
├── __init__.py               # Interfaz pública: exporta convert_md_to_video
├── md_to_video.py            # CLI y orquestador del pipeline
├── video_brain.py            # 'Brain': Segmentación, guionización y cálculo de exposición con NumPy
├── image_curator.py          # Búsqueda, descarga, validación y normalización fotográfica
└── video_nerve.py            # 'Nerve': Ensamblado FFmpeg, animación Ken Burns, subtitulación y render
```

### 2.1. `video_brain.py` (Inteligencia Temporal y Estructuración)
- **Extracción Categorial:** Parsea encabezados (`#`, `##`, `###`), párrafos explicativos, callouts/alertas (`> [!NOTE]`, etc.) y tablas comparativas.
- **Cálculo de Tiempos y Pausas con NumPy:**
  - Define una matriz de pesos temporales basada en la longitud de palabras y el tipo de elemento (un encabezado o definición requiere mayor tiempo relativo que una oración de enlace).
  - Tasa de habla reflexiva y reposada: 105 palabras por minuto (~1.75 palabras por segundo).
  - Pausas acústicas de asimilación teórica: inserción de silencios solemnes de 750 ms tras puntos seguidos, 500 ms tras dos puntos y 250 ms tras comas.
  - Tiempo mínimo de escena: 10.0 segundos; margen ponderado para garantizar absorción conceptual.
- **Locución y Voz en Off:**
  - **Voz Neuronal Gratuita de Estudio (Primaria):** `es-ES-AlvaroNeural` (o `es-MX-JorgeNeural`), calibrada con tono grave y reflexivo (`pitch="-4Hz"`, `rate="-12%"`), equivalente acústico directo a *Mario (ElevenLabs)*, sin costes de suscripción ni límites por API Key.
  - **Motor de Respaldo Local (Offline):** `Grandpa (Spanish (Spain))` nativo de macOS para ejecución sin conexión a red.
- **Descriptores de Búsqueda Visual:** Genera términos de búsqueda específicos orientados a la fotografía documental (p. ej., *"strike workers factory 20th century photograph"*, *"cargo ship maritime trade docks"*).
- **Metadatos para YouTube:** Produce de forma automática:
  - Título optimizado.
  - Descripción con el enlace prioritario a `https://ades.cloud`.
  - Marcas de tiempo (*timestamps* / capítulos de YouTube) para navegación directa.

### 2.2. `image_curator.py` (Curaduría Fotográfica Estricta)
- **Filtro Fotográfico Exclusivo:**
  - Realiza peticiones a fuentes de imágenes abiertas y de archivo documental (Wikimedia Commons, Unsplash, Pexels o archivo local).
  - Aplica filtros estrictos de tipo de contenido: restringe a formato fotográfico y descarta etiquetas como `vector`, `illustration`, `drawing`, `clipart`, `cartoon`.
- **Encuadre y Normalización:**
  - Redimensionamiento y ajuste a resolución nativa 1920×1080 (16:9).
  - Manejo de fotografías verticales o de archivo histórico mediante desenfoque cinemático de fondo (*blurred letterbox background*) para preservar la relación de aspecto sin distorsión.

### 2.3. `video_nerve.py` (Ejecución Cinematográfica)
- **Efecto Ken Burns:**
  - Generación de filtros de paneo y zoom sutil (`zoompan`) en FFmpeg.
  - Alternancia dinámica de movimientos (zoom-in lento hacia el centro, paneo sutil de izquierda a derecha, zoom-out expansivo).
- **Maquetación Tipográfica en Pantalla:**
  - Frases centrales, citas textuales y categorías en tercios inferiores con fondos oscurecidos traslúcidos para garantizar legibilidad absoluta.
- **Outro Institucional:**
  - Pantalla final de cierre de 6 a 8 segundos con la identidad gráfica de **ADES.CLOUD** y la llamada a la acción:
    > *"Para profundizar en este y otros análisis, visita https://ades.cloud donde están todos nuestros escritos e investigaciones."*
- **Codificación y Renderizado:**
  - Códec H.264 (perfil High), contenedor MP4, tasa de 30 fps, píxeles en formato `yuv420p` y bandera `+faststart` para reproducción óptima en streaming.

---

## 3. Especificaciones Técnicas para YouTube

| Parámetro | Estándar Implementado | Justificación |
| :--- | :--- | :--- |
| **Relación de Aspecto** | 16:9 | Formato panorámico nativo de reproductores de escritorio y TV en YouTube. |
| **Resolución** | 1920 × 1080 px (Full HD) | Balance óptimo entre tiempo de procesamiento y nitidez profesional. |
| **Tasa de Cuadros** | 30 fps | Fluidez visual adecuada para movimiento de cámara fotográfica y lectura. |
| **Códec de Video** | H.264 / AVC | Compatibilidad universal sin recodificación destructiva por YouTube. |
| **Códec de Audio** | AAC (192-320 kbps / 48 kHz) | Fidelidad acústica para voz en off y ambientación. |
| **Optimización Web** | `movflags=+faststart` | Coloca el índice al inicio del archivo para carga inmediata. |

---

## 4. Estrategia de Cierre y Retención de Audiencia

El video finaliza con una pantalla de cierre estructurada:
1. **Identidad Institucional:** Logotipo y nombre del Centro de Estudios e Investigación Marxista **ADES.CLOUD**.
2. **Llamada a la Acción (CTA):** Enlace destacado visible `https://ades.cloud`.
3. **Invitación Expresa:** "Visita nuestro repositorio teórico para consultar el documento completo, notas al pie y referencias bibliográficas."

---

## 5. Instrucciones de Uso

### 5.1. Desde Línea de Comandos (CLI)
```bash
# Convertir un análisis a video con parámetros por defecto
python3 -m video.md_to_video analisis/ejemplo_analisis.md

# Especificar archivo de salida y preset visual
python3 -m video.md_to_video analisis/ejemplo_analisis.md -o salida/analisis_capital.mp4
```

### 5.2. Uso Programático desde Python
```python
from video import convert_md_to_video

video_path = convert_md_to_video(
    input_path="analisis/ejemplo_analisis.md",
    output_path="analisis/ejemplo_analisis.mp4",
    generate_metadata=True
)
print(f"Video generado exitosamente en: {video_path}")
```
