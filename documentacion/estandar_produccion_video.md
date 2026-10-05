# Guía y Estándar de Producción Audiovisual Documental (ADES.CLOUD)

> **Proyecto:** BrainPolitics  
> **Institución:** Centro de Estudios e Investigación Marxista ADES.CLOUD  
> **Módulo:** `video/` (Arquitectura Dual-Runtime: Brain / Nerve)  
> **Objetivo:** Registro normativo de especificaciones técnicas, lecciones aprendidas y directrices obligatorias para la generación automatizada de video-ensayos y documentales para YouTube.

---

## 1. Principios Rectores y Estándar de Calidad

Los videos producidos por **ADES.CLOUD** no son presentaciones estáticas de diapositivas ni animaciones superficiales; son **piezas documentales de investigación y combate ideológico** con estándar de emisión profesional (*broadcast grade*). Toda producción audiovisual del sistema debe respetar rigurosamente los siguientes cinco pilares:

1. **Locución Solemne y Humana:** Voz masculina madura en español, de tono reflexivo y pausado, sin lectura de caracteres de sintaxis ni marcas de formato.
2. **Dinamismo Visual y Montaje Multi-Toma:** Ritmo cinematográfico continuo mediante cortes periódicos entre múltiples fotografías por bloque temático. Prohibido congelar una sola imagen durante todo un párrafo o escena.
3. **Autenticidad Fotográfica Documental:** Empleo exclusivo de fotografía real de archivo histórico, documental y periodístico. Queda estrictamente vetado el uso de dibujos, caricaturas, ilustraciones artísticas o grabados.
4. **Zócalos Tipográficos Inmutables (Lower-Thirds):** Textos, categorías y citas íntegras, con contraste absoluto garantizado mediante fondos oscuros dedicados, montados como capas estáticas independientes después del movimiento de cámara. Prohibido el recorte de bordes o truncamiento de palabras.
5. **Cierre Institucional Obligatorio:** Todo video culmina con la pantalla de cierre institucional con invitación formal y enlace explícito a **https://ades.cloud**.

---

## 2. Locución y Procesamiento Acústico (Voice & Audio)

### 2.1. Selección y Perfil de Voz
- **Idioma y Género:** Español neutro o peninsular solemne (`es-ES` o `es-MX`), registro masculino maduro, emulando la serenidad y peso conceptual de un narrador documental histórico.
- **Motor Primario de Estudio:** `edge-tts` con la voz `es-ES-AlvaroNeural` (o en su defecto `es-MX-JorgeNeural`).
  - **Calibración tonal:** `pitch="-4Hz"` (tono más grave y solemne) y `rate="-8%"` a `"-10%"` (velocidad pausada para asimilación teórica).
  - **Alternativa / Respaldo Offline:** Motor `say` nativo de macOS (`Grandpa (Spanish (Spain))`).

### 2.2. Sanitización Absoluta del Guión de Lectura (Anti-Spelling de Markdown)
El texto enviado al motor TTS debe ser **prosa limpia y continua**. Queda terminantemente prohibido que el locutor vocalice elementos de sintaxis:
- **Tokens Markdown eliminados:** Símbolos `#`, `##`, `###`, asteriscos `**`, guiones `-`, viñetas, corchetes `[]`, paréntesis de hipervínculos `()`, enlaces URL y llamadas de alerta `> [!NOTE]`.
- **Palabras parásitas proscritas:** Se prohíbe verbalizar términos metalingüísticos como *"guion"*, *"hashtag"*, *"asterisco"*, *"barra"* o *"link"*.
- **Puntuación y Pausas de Respiración:**
  - Los silencios entre bloques o párrafos deben ser de **500 ms a 750 ms**. Se prohíben pausas excesivas mayores a 1.2 segundos que generen silencios incómodos o desconexión en el espectador.
  - Comas y dos puntos introducen micro-pausas naturales de 200 ms a 350 ms.

---

## 3. Curaduría y Montaje Fotográfico (Visual & Cinematic)

### 3.1. Prohibición de Ilustraciones y Grabados
Para preservar el rigor científico e histórico de las investigaciones de **ADES.CLOUD**, las imágenes deben ser documentos de la realidad material:
- **Permitido:** Fotografías reales de época, retratos de archivo fotográfico, tomas periodísticas, registros documentales de huelgas, minería, fábricas, puertos, asambleas y sedes políticas.
- **Terminantemente Prohibido:** Ilustraciones vectoriales, dibujos animados, caricaturas, infografías planas, grabados en madera (*woodcuts*), aguafuertes (*etchings*) y litografías artísticas decimonónicas.
- **Filtro Técnico en APIs de Búsqueda (Wikimedia Commons):**
  - Añadir siempre descriptores excluyentes: `-engraving -woodcut -etching -diagram -map -drawing -cartoon -clipart`.

### 3.2. Montaje Multi-Toma por Escena (Pacing Cinematográfico)
- **Frecuencia de Corte:** Se prohíbe sostener una misma imagen fija durante más de 10 segundos.
- **Regla Multi-Shot:** Cada escena de 20–30 segundos debe ensamblar un mínimo de **3 fotografías documentales distintas** asociadas a los conceptos expuestos.
- **Duración por Toma:** Cada sub-fotografía se proyecta durante **6 a 8 segundos** ($D_{escena} / N_{fotos}$), permitiendo que la locución continúe fluida y sin saltos mientras el fondo visual dinamiza la atención.
- **Normalización 16:9 (1920×1080):** Toda fotografía histórica (vertical o panorámica) debe enmarcarse con técnica de **letterbox desenfocado** (*blurred background*): la imagen original se expande al 100% de alto en el centro nítido, mientras el fondo se rellena con la misma imagen desenfocada a pantalla completa para evitar bandas negras vacías.

### 3.3. Movimiento de Cámara Ken Burns
- Aplicar variaciones sutiles y continuas de movimiento en cada cambio de fotografía:
  1. `zoom_in`: Acercamiento lento al 115% hacia el centro de interés.
  2. `pan_left`: Desplazamiento horizontal suave de derecha a izquierda.
  3. `zoom_out`: Alejamiento progresivo de 115% a 100%.
  4. `pan_right`: Desplazamiento horizontal suave de izquierda a derecha.

---

## 4. Arquitectura de Zócalos y Tipografía Inferior (Lower-Thirds)

### 4.1. Causa Raíz del Error de Texto Cortado
Cuando el texto o cintillo informativo se renderiza directamente sobre el archivo de imagen antes del filtro `zoompan` de FFmpeg:
- Al aplicar el zoom dinámico de cámara (1.15x), los bordes exteriores y los 70–100 píxeles inferiores de la imagen quedan recortados fuera del área visible de la pantalla.
- Esto provoca que el texto se estire, se mueva con la cámara y se corte en los laterales e inferior.

### 4.2. Regla Técnica Obligatoria: Superposición Estática (`Overlay Post-Motion`)
- La capa gráfica inferior debe generarse **exclusivamente como un lienzo PNG transparente independiente de 1920×1080 píxeles**.
- En el pipeline de FFmpeg, la composición debe realizarse **después** del movimiento de cámara:
  ```bash
  [0:v]zoompan=z='...':x='...':y='...':d=...:s=1920x1080[bg]; [bg][1:v]overlay=0:0[outv]
  ```
- **Resultado:** El zócalo permanece 100% estático, nítido, estable e inafectado por el zoom o paneo de la imagen de fondo.

### 4.3. Contraste y Respaldo Visual Seguro
- El texto del tercio inferior no puede depender únicamente de sombras de letras.
- Debe incluir una base opaca oscura color pizarra (`rgba(8, 12, 16, 235)`) que cubra la franja inferior (desde `y=745` hasta `y=1080`), precedida por un degradado suave de transición (`y=670` a `y=745`).
- Línea de acento institucional carmesí (`#9E1B1B`, altura 4px) en la frontera superior del zócalo para separar el contenido audiovisual de la síntesis textual.

### 4.4. Integridad de Citas y Ajuste de Líneas
- **Prohibición de Slicing Ciego:** Queda prohibido recortar cadenas mediante índices fijos como `texto[:120]` o expresiones regulares voraces que unan comillas distantes en Markdown.
- **Frases Teóricas Completas:** El zócalo debe mostrar tesis conceptuales cerradas y gramaticalmente completas, envueltas entre comillas angulares latinas (*«...»*).
- **Ajuste Automático (*Word Wrap*):** Máximo de 2 líneas por zócalo, divididas por palabras enteras mediante `textwrap` con un límite estricto de 78–82 caracteres por renglón.

---

## 5. Pantalla de Cierre Institucional (Outro) y Metadatos de YouTube

### 5.1. Outro Oficial ADES.CLOUD
Todo video producido debe finalizar de forma ineludible con la escena de cierre institucional (duración: 7 segundos):
- Fondo oscuro sobrio con gradiente radial y micro-ruido cinematográfico.
- Título principal: **ADES.CLOUD**
- Subtítulo: *Centro de Estudios e Investigación Marxista*
- Llamada a la acción destacada:
  > *"Documento completo, citas y referencias bibliográficas en:"*  
  > **https://ades.cloud**

### 5.2. Archivo de Metadatos y Capítulos para YouTube
Junto al archivo `.mp4`, el sistema genera automáticamente un archivo `.youtube_metadata.txt` que contiene:
1. **Título:** Conciso, riguroso y optimizado con nomenclatura institucional:  
   `[Título del Documento] | ADES.CLOUD`
2. **Capítulos (*Timestamps*):** Marcas de tiempo calculadas milimétricamente desde el inicio (ej. `00:00 Introducción`, `00:23 I. Purga Judicial...`) que YouTube convierte automáticamente en barra de navegación de capítulos.
3. **Descripción:** Resumen teórico del contenido y enlace prioritario en primera línea a `https://ades.cloud`.
4. **Etiquetas Clave (*Tags*):** Descriptores conceptuales para posicionamiento algorítmico en ciencias sociales.

---

## 6. Checklist de Validación Prevuelo para Nuevos Videos

Antes de dar por concluida la generación de cualquier video, verificar:

- [ ] **Locución:** ¿Es voz masculina, en español, pausada y sin mención de caracteres de formato Markdown?
- [ ] **Pausas:** ¿Los silencios entre párrafos son naturales (500–750 ms) y sin baches vacíos?
- [ ] **Fotografía:** ¿Todas las imágenes son fotografías reales de archivo? ¿Se han filtrado grabados, caricaturas o dibujos?
- [ ] **Multi-Toma:** ¿Cada escena contiene al menos 3 tomas con cortes cada 6–8 segundos?
- [ ] **Zócalo Inferior:** ¿El texto es visible al 100%, sin recortes en la parte inferior o lateral, y montado con `overlay` post-zoompan?
- [ ] **Citas:** ¿Las frases del zócalo son sentencias teóricas completas sin palabras a medio cortar?
- [ ] **Outro:** ¿Aparece la pantalla final invitando a `https://ades.cloud`?
- [ ] **Limpieza:** ¿Se han eliminado los archivos temporales de audio y video intermedios?
