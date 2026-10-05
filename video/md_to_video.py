"""
Interfaz principal de conversión Markdown a Video para el proyecto BrainPolitics (ADES.CLOUD).
Proporciona la función `convert_md_to_video` y ejecutable por CLI.
"""

import sys
import os
import argparse
from typing import Optional
from .video_brain import VideoBrain
from .image_curator import ImageCurator
from .video_nerve import VideoNerve


def convert_md_to_video(
    input_path: str,
    output_path: Optional[str] = None,
    voice: str = "es-ES-AlvaroNeural",
    enable_tts: bool = True,
    generate_metadata: bool = True
) -> str:
    """Convierte un documento Markdown en un video profesional para YouTube (1080p / 16:9).

    Args:
        input_path: Ruta al archivo Markdown fuente (.md).
        output_path: Ruta del video MP4 de salida. Si es None, se genera con el mismo nombre y extensión .mp4.
        voice: Voz neuronal en español de hombre maduro/profundo (por defecto "es-ES-AlvaroNeural").
        enable_tts: Si es True, genera locución de voz para cada escena.
        generate_metadata: Si es True, genera un archivo .youtube_metadata.txt con capítulos y enlaces.

    Returns:
        str: Ruta absoluta al archivo de video MP4 generado.
    """
    input_abs = os.path.abspath(input_path)
    if not os.path.exists(input_abs):
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {input_path}")

    if not output_path:
        base, _ = os.path.splitext(input_abs)
        output_path = f"{base}.mp4"
    else:
        output_path = os.path.abspath(output_path)

    # Directorio de trabajo temporal
    work_dir = os.path.join(os.path.dirname(output_path), ".video_work_tmp")
    os.makedirs(work_dir, exist_ok=True)

    print(f"[*] Iniciando procesamiento de video para: {os.path.basename(input_abs)}")
    with open(input_abs, "r", encoding="utf-8") as f:
        md_content = f.read()

    # 1. BRAIN: Estructuración dialéctica, tiempos con NumPy y guionización pausada de hombre mayor
    brain = VideoBrain(target_wpm=105.0)
    doc_title = brain.extract_document_title(md_content)
    print(f"[*] Analizando estructura categorial del documento: «{doc_title}»")
    scenes = brain.parse_scenes(md_content)
    print(f"[*] {len(scenes)} escenas cinematográficas estructuradas con cálculo temporal NumPy.")

    # 2. IMAGE CURATOR: Búsqueda fotográfica documental y generación de zócalos
    curator = ImageCurator(cache_dir=os.path.join(work_dir, "images"))
    print("[*] Localizando y curando múltiples fotografías documentales por escena (sin dibujos)...")
    
    scene_shots = []
    scene_overlays = []
    for i, sc in enumerate(scenes):
        # Determinar cantidad de fotos según duración de la escena (2 para escenas breves, 3 para estándar)
        shot_count = 2 if sc.get("duration", 20.0) < 14.0 else 3
        imgs = curator.fetch_scene_images(sc, count=shot_count)
        scene_shots.append(imgs)

        # Generar capa gráfica estática (zócalo y título profesional sin cortes)
        overlay_out = os.path.join(work_dir, f"overlay_{i:02d}.png")
        curator.create_lower_third_overlay(sc, overlay_out)
        scene_overlays.append(overlay_out)
        print(f"    - Escena {i+1}/{len(scenes)}: {len(imgs)} fotografías documentales preparadas.")

    # 3. NERVE: Renderizado con montaje multi-toma, locución y ensamblado FFmpeg
    nerve = VideoNerve(work_dir=work_dir)
    print("[*] Renderizando clips cinematográficos con montaje multi-toma y zócalos estáticos...")
    
    clip_paths = []
    for i, sc in enumerate(scenes):
        clip_out = os.path.join(work_dir, f"clip_{i:02d}.mp4")
        nerve.render_scene_clip(
            image_paths=scene_shots[i],
            scene=sc,
            output_clip_path=clip_out,
            overlay_path=scene_overlays[i],
            voice=voice,
            enable_tts=enable_tts
        )
        clip_paths.append(clip_out)

    # Ensamblado final
    print(f"[*] Ensamblando video final con optimización para YouTube (+faststart)...")
    final_video = nerve.assemble_final_video(clip_paths, output_path)

    # 4. Generación de Metadatos para YouTube (descripción con https://ades.cloud y marcas de tiempo)
    if generate_metadata:
        meta = brain.generate_youtube_metadata(doc_title, scenes)
        meta_file = os.path.splitext(output_path)[0] + ".youtube_metadata.txt"
        with open(meta_file, "w", encoding="utf-8") as f:
            f.write(f"TÍTULO SUGERIDO PARA YOUTUBE:\n{meta['title']}\n\n")
            f.write(f"DURACIÓN TOTAL ESTIMADA: {meta['total_duration_sec']} segundos\n\n")
            f.write(f"DESCRIPCIÓN OPTIMIZADA PARA COPIAR EN YOUTUBE:\n")
            f.write("=" * 60 + "\n")
            f.write(meta["description"] + "\n")
            f.write("=" * 60 + "\n")
        print(f"[+] Metadatos y capítulos para YouTube guardados en: {meta_file}")

    # Limpieza de archivos temporales
    nerve.cleanup()
    print(f"[✓] ¡Video documental completado exitosamente!: {final_video}")
    return final_video


def main():
    parser = argparse.ArgumentParser(
        description="Conversor de Documentos Markdown a Video Documental para YouTube (ADES.CLOUD)"
    )
    parser.add_argument("input_file", help="Ruta al archivo Markdown (.md)")
    parser.add_argument("-o", "--output", help="Ruta del video MP4 de salida", default=None)
    parser.add_argument("--voice", help="Voz para locución (ej: es-ES-AlvaroNeural, es-MX-JorgeNeural)", default="es-ES-AlvaroNeural")
    parser.add_argument("--no-tts", help="Desactivar locución de voz y usar audio ambiental", action="store_true")
    parser.add_argument("--no-meta", help="No generar archivo de metadatos de YouTube", action="store_true")

    args = parser.parse_args()

    try:
        convert_md_to_video(
            input_path=args.input_file,
            output_path=args.output,
            voice=args.voice,
            enable_tts=not args.no_tts,
            generate_metadata=not args.no_meta
        )
    except Exception as e:
        print(f"\n[!] ERROR en la generación del video: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
