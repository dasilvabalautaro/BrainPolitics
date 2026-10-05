# BrainPolitics

> **Centro de Estudios e Investigación Marxista ADES.CLOUD**  
> Plataforma de investigación, crítica de la economía política y producción automatizada de análisis, documentos y video-ensayos documentales.

---

## 1. Arquitectura 'Dual-Runtime'

El sistema implementa una arquitectura rigurosa de dos niveles en **Python 3.11+**:
- **Lógica e Inferencia (Nerve):** Orquestación de flujos, procesamiento textual, pipelines y composición audiovisual con FFmpeg y WeasyPrint.
- **Inteligencia y Modelado Numérico (Brain):** Procesamiento cuantitativo y temporal con **TensorFlow / NumPy** para calcular métricas de densidad, proporciones y ritmos de exposición.

```
BrainPolitics/
├── converter/          # Módulo Dual-Runtime: Conversión de Markdown a PDF editorial
├── video/              # Módulo Dual-Runtime: Producción de Video Documental para YouTube
├── documentacion/      # Estándares técnicos y guías de producción
├── analisis/           # Informes de coyuntura y diagnósticos socioeconómicos
├── articulo/           # Artículos teóricos y ensayos
├── folleto/            # Materiales pedagógicos y formativos
├── critica/            # Polémica teórica y refutación ideológica
└── investigacion/      # Monografías extensas y estudios empíricos
```

---

## 2. Suites del Sistema

### 2.1. Conversor Editorial a PDF (`converter/`)
Genera publicaciones maquetadas con tipografía académica, portadas institucionales, callouts y paginación formal mediante WeasyPrint y CSS Paged Media.

```bash
python3 -m converter.md_to_pdf analisis/mi_documento.md
```

### 2.2. Suite de Video Documental para YouTube (`video/`)
Transforma investigaciones en documentales cinematográficos a 1080p con locución solemne, curaduría de fotografía histórica real de archivo (multi-toma), efectos de cámara Ken Burns y zócalos inferiores (*lower thirds*) de alta legibilidad.

```bash
python3 -m video.md_to_video articulo/mi_articulo.md
```

Para especificaciones detalladas, consultar [`documentacion/estandar_produccion_video.md`](documentacion/estandar_produccion_video.md).

---

## 3. Autoría Institucional

Todos los trabajos producidos bajo esta plataforma corresponden a:  
**Centro de Estudios e Investigación Marxista ADES.CLOUD**  
Web oficial: [https://ades.cloud](https://ades.cloud)