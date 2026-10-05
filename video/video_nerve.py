"""
Módulo 'Nerve' (Inferencia, Efectos Cinematográficos y Renderizado de Video).
Arquitectura Dual-Runtime: Ejecuta el pipeline de renderizado utilizando FFmpeg,
aplicando efectos Ken Burns (zoom y paneo suaves), superposición tipográfica,
locución sincronizada y codificación H.264/AAC optimizada para YouTube.
"""

import os
import subprocess
import shutil
from typing import List, Dict, Any, Optional


class VideoNerve:
    """Motor de composición cinematográfica y renderizado de video mediante FFmpeg."""

    def __init__(self, work_dir: str = "temp/video_work"):
        self.work_dir = work_dir
        os.makedirs(self.work_dir, exist_ok=True)
        self.ffmpeg_bin = shutil.which("ffmpeg") or "/usr/local/bin/ffmpeg"
        self.say_bin = shutil.which("say") or "/usr/bin/say"

    def get_best_spanish_male_voice(self, preferred_voice: Optional[str] = None) -> str:
        """Resuelve con certeza una voz en ESPAÑOL y de HOMBRE MAYOR/adulto disponible en el sistema.
        
        Garantiza que nunca se use una voz en inglés o femenina por fallback.
        """
        if not os.path.exists(self.say_bin):
            return "Grandpa (Spanish (Spain))"

        try:
            res = subprocess.run([self.say_bin, "-v", "?"], capture_output=True, text=True, check=True)
            available = res.stdout.splitlines()

            # Si el usuario solicitó una voz explícita, comprobar si está disponible
            if preferred_voice:
                for line in available:
                    if preferred_voice.lower() in line.lower() and ("es_ES" in line or "es_MX" in line or "Spanish" in line):
                        # Extraer el nombre exacto de la voz antes del código de idioma
                        return preferred_voice

            # Candidatos priorizados: Hombre mayor en español (Grandpa) y hombres adultos
            male_candidates = [
                "Grandpa (Spanish (Spain))",
                "Grandpa (Spanish (Mexico))",
                "Grandpa",
                "Reed (Spanish (Spain))",
                "Reed (Spanish (Mexico))",
                "Eddy (Spanish (Spain))",
                "Eddy (Spanish (Mexico))",
                "Rocko (Spanish (Spain))",
                "Rocko (Spanish (Mexico))",
            ]

            for cand in male_candidates:
                for line in available:
                    if cand.lower() in line.lower():
                        return cand

            # Si por alguna razón ninguna coincidió, buscar cualquier voz en español
            for line in available:
                if "es_ES" in line or "es_MX" in line or "Spanish" in line:
                    parts = line.split()
                    if parts:
                        return parts[0]

        except Exception:
            pass

        return "Grandpa (Spanish (Spain))"

    def _format_narration_with_pauses(self, text: str) -> str:
        """Inserta pausas acústicas de asimilación reflexiva entre frases y conceptos."""
        import re
        # Pausa solemne de 750 ms tras puntos seguidos
        t = re.sub(r"\.\s+", ". [[slnc 750]] ", text)
        # Pausa de 500 ms tras dos puntos
        t = re.sub(r":\s+", ": [[slnc 500]] ", t)
        # Pausa de 450 ms tras punto y coma
        t = re.sub(r";\s+", "; [[slnc 450]] ", t)
        # Pausa sutil de 250 ms tras coma para no atropellar conceptos
        t = re.sub(r",\s+", ", [[slnc 250]] ", t)
        return t

    def _generate_edge_tts_audio(
        self,
        text: str,
        output_mp3_path: str,
        voice_id: str = "es-ES-AlvaroNeural",
        rate: str = "-12%",
        pitch: str = "-4Hz"
    ) -> bool:
        """Genera locución neuronal de estudio gratuita (masculina, cálida y profunda, equivalente a ElevenLabs)."""
        try:
            import asyncio
            import edge_tts

            async def _run():
                # Limpiar marcas de say para el motor neural
                import re
                clean = re.sub(r"\[\[slnc\s*\d+\]\]", "...", text)
                comm = edge_tts.Communicate(clean, voice_id, rate=rate, pitch=pitch)
                await comm.save(output_mp3_path)

            asyncio.run(_run())
            return os.path.exists(output_mp3_path) and os.path.getsize(output_mp3_mp3 := output_mp3_path) > 1000
        except Exception:
            return False

    def _get_audio_duration(self, audio_path: str) -> float:
        """Obtiene la duración exacta en segundos de un archivo de audio mediante ffprobe."""
        try:
            cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                audio_path
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            return float(res.stdout.strip())
        except Exception:
            return 8.0

    def render_scene_clip(
        self,
        image_paths: Any,
        scene: Dict[str, Any],
        output_clip_path: str,
        overlay_path: Optional[str] = None,
        voice: Optional[str] = None,
        enable_tts: bool = True
    ) -> str:
        """Renderiza un clip de video individual para una escena aplicando montaje multi-toma, Ken Burns y zócalo estático."""
        fps = 30

        # Normalizar image_paths a lista
        if isinstance(image_paths, str):
            images = [image_paths]
        else:
            images = list(image_paths)
        if not images:
            raise ValueError("Se requiere al menos una imagen para la escena.")

        # 1. Generar audio para la escena
        audio_clip_path = os.path.splitext(output_clip_path)[0] + "_audio.aac"
        has_audio = False
        raw_audio_dur = None

        if enable_tts:
            text_to_narrate = scene.get("narration", "")
            if text_to_narrate:
                temp_neural = os.path.splitext(output_clip_path)[0] + "_neural.mp3"
                # Intentar primero con la voz neuronal de estudio (AlvaroNeural: masculina, madura, profunda)
                voice_target = voice if (voice and "Neural" in voice) else "es-ES-AlvaroNeural"
                success_neural = self._generate_edge_tts_audio(
                    text=text_to_narrate,
                    output_mp3_path=temp_neural,
                    voice_id=voice_target,
                    rate="-10%",
                    pitch="-3Hz"
                )

                if success_neural:
                    try:
                        raw_audio_dur = self._get_audio_duration(temp_neural)
                        # Pausa sutil y fluida entre bloques: solo 0.8 segundos tras finalizar la locución
                        clip_dur = max(4.0, round(raw_audio_dur + 0.8, 1))

                        cmd_audio = [
                            self.ffmpeg_bin, "-y",
                            "-i", temp_neural,
                            "-af", f"apad=whole_dur={clip_dur},volume=1.0",
                            "-t", str(clip_dur),
                            "-c:a", "aac",
                            "-b:a", "192k",
                            "-ar", "48000",
                            "-ac", "2",
                            audio_clip_path
                        ]
                        subprocess.run(cmd_audio, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        has_audio = True
                        duration = clip_dur
                        scene["duration"] = clip_dur
                        if os.path.exists(temp_neural):
                            os.remove(temp_neural)
                    except Exception:
                        has_audio = False

                # Fallback al motor local say de macOS si falla el motor neural
                if not has_audio and os.path.exists(self.say_bin):
                    temp_aiff = os.path.splitext(output_clip_path)[0] + "_voice.aiff"
                    try:
                        selected_voice = self.get_best_spanish_male_voice(voice)
                        paced_text = self._format_narration_with_pauses(text_to_narrate)
                        cmd_say = [
                            self.say_bin,
                            "-v", selected_voice,
                            "-r", "115",
                            paced_text,
                            "-o", temp_aiff
                        ]
                        subprocess.run(cmd_say, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        raw_audio_dur = self._get_audio_duration(temp_aiff)
                        clip_dur = max(4.0, round(raw_audio_dur + 0.8, 1))

                        cmd_audio = [
                            self.ffmpeg_bin, "-y",
                            "-i", temp_aiff,
                            "-af", f"apad=whole_dur={clip_dur},volume=1.0",
                            "-t", str(clip_dur),
                            "-c:a", "aac",
                            "-b:a", "192k",
                            "-ar", "48000",
                            "-ac", "2",
                            audio_clip_path
                        ]
                        subprocess.run(cmd_audio, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        has_audio = True
                        duration = clip_dur
                        scene["duration"] = clip_dur
                        if os.path.exists(temp_aiff):
                            os.remove(temp_aiff)
                    except Exception:
                        has_audio = False

        # Si no hubo audio hablado, usar la duración base estimada
        if not has_audio:
            duration = float(scene.get("duration", 6.0))
            cmd_silent = [
                self.ffmpeg_bin, "-y",
                "-f", "lavfi",
                "-i", f"anullsrc=r=48000:cl=stereo",
                "-t", str(duration),
                "-c:a", "aac",
                "-b:a", "192k",
                audio_clip_path
            ]
            subprocess.run(cmd_silent, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 2. Montaje dinámico multi-toma: subdividir la duración entre las N fotos
        n_shots = len(images)
        shot_durations = [duration / n_shots] * n_shots
        shot_durations[-1] = duration - sum(shot_durations[:-1])

        effects_cycle = ["zoom_in", "pan_left", "zoom_out", "pan_right"]
        scene_idx = scene.get("scene_index", 0)

        shot_clips = []
        for k, img in enumerate(images):
            s_dur = shot_durations[k]
            s_frames = max(30, int(round(s_dur * fps)))
            s_effect = effects_cycle[(scene_idx + k) % len(effects_cycle)]
            s_out = os.path.splitext(output_clip_path)[0] + f"_shot_{k}.mp4"

            zoom_step = round(0.14 / max(1, s_frames), 6)
            pan_step = round(160.0 / max(1, s_frames), 4)

            if s_effect == "zoom_out":
                vf_filter = (
                    f"zoompan=z='if(lte(zoom,1.0),1.14,max(1.001,zoom-{zoom_step}))':"
                    f"d={s_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                    f"s=1920x1080:fps={fps}"
                )
            elif s_effect == "pan_left":
                vf_filter = (
                    f"zoompan=z=1.12:x='if(lte(on,1),(iw-iw/zoom),max(0,x-{pan_step}))':"
                    f"y='ih/2-(ih/zoom/2)':d={s_frames}:s=1920x1080:fps={fps}"
                )
            elif s_effect == "pan_right":
                vf_filter = (
                    f"zoompan=z=1.12:x='if(lte(on,1),0,min((iw-iw/zoom),x+{pan_step}))':"
                    f"y='ih/2-(ih/zoom/2)':d={s_frames}:s=1920x1080:fps={fps}"
                )
            else:  # zoom_in
                vf_filter = (
                    f"zoompan=z='min(zoom+{zoom_step},1.15)':"
                    f"d={s_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                    f"s=1920x1080:fps={fps}"
                )

            cmd_shot = [
                self.ffmpeg_bin, "-y",
                "-loop", "1",
                "-i", img,
                "-vf", vf_filter,
                "-t", f"{s_dur:.3f}",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "18",
                "-pix_fmt", "yuv420p",
                s_out
            ]
            res = subprocess.run(cmd_shot, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.returncode != 0:
                raise RuntimeError(f"Error renderizando toma {k} de escena {scene_idx}: {res.stderr.decode('utf-8', errors='ignore')}")
            shot_clips.append(s_out)

        # Concatenar tomas en un video de fondo
        if n_shots == 1:
            montage_video = shot_clips[0]
        else:
            montage_video = os.path.splitext(output_clip_path)[0] + "_montage.mp4"
            concat_file = os.path.splitext(output_clip_path)[0] + "_shots_list.txt"
            with open(concat_file, "w", encoding="utf-8") as f:
                for sc in shot_clips:
                    f.write(f"file '{os.path.abspath(sc)}'\n")

            cmd_concat_shots = [
                self.ffmpeg_bin, "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", concat_file,
                "-c", "copy",
                montage_video
            ]
            res = subprocess.run(cmd_concat_shots, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.returncode != 0:
                raise RuntimeError(f"Error concatenando tomas: {res.stderr.decode('utf-8', errors='ignore')}")
            if os.path.exists(concat_file):
                os.remove(concat_file)

        # 3. Superponer zócalo estático profesional y sincronizar audio
        if overlay_path and os.path.exists(overlay_path):
            cmd_final_clip = [
                self.ffmpeg_bin, "-y",
                "-i", montage_video,
                "-i", overlay_path,
                "-i", audio_clip_path,
                "-filter_complex", "[0:v][1:v]overlay=0:0[outv]",
                "-map", "[outv]",
                "-map", "2:a",
                "-t", str(duration),
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", "18",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-b:a", "192k",
                "-ar", "48000",
                "-shortest",
                output_clip_path
            ]
        else:
            cmd_final_clip = [
                self.ffmpeg_bin, "-y",
                "-i", montage_video,
                "-i", audio_clip_path,
                "-map", "0:v",
                "-map", "1:a",
                "-t", str(duration),
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", "18",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-b:a", "192k",
                "-ar", "48000",
                "-shortest",
                output_clip_path
            ]

        res = subprocess.run(cmd_final_clip, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            raise RuntimeError(f"Error finalizando clip FFmpeg: {res.stderr.decode('utf-8', errors='ignore')}")

        # Limpieza de subclips temporales de tomas
        for sc in shot_clips:
            if os.path.exists(sc):
                os.remove(sc)
        if n_shots > 1 and os.path.exists(montage_video):
            os.remove(montage_video)

        return output_clip_path

    def assemble_final_video(
        self,
        clip_paths: List[str],
        output_video_path: str
    ) -> str:
        """Concatena todos los clips individuales en el video final optimizado para YouTube."""
        concat_txt = os.path.join(self.work_dir, "concat_list.txt")
        with open(concat_txt, "w", encoding="utf-8") as f:
            for clip in clip_paths:
                abs_clip = os.path.abspath(clip)
                f.write(f"file '{abs_clip}'\n")

        # Concatenar con stream copy para máxima velocidad y fidelidad digital
        cmd_concat = [
            self.ffmpeg_bin, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_txt,
            "-c", "copy",
            "-movflags", "+faststart",
            output_video_path
        ]

        res = subprocess.run(cmd_concat, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            # Fallback con transcodificación si la concatenación directa fallara
            cmd_fallback = [
                self.ffmpeg_bin, "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", concat_txt,
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", "18",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-b:a", "192k",
                "-ar", "48000",
                "-movflags", "+faststart",
                output_video_path
            ]
            res_fb = subprocess.run(cmd_fallback, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res_fb.returncode != 0:
                raise RuntimeError(f"Error concatenando video final: {res_fb.stderr.decode('utf-8', errors='ignore')}")

        return output_video_path

    def cleanup(self):
        """Limpia los archivos temporales de trabajo."""
        if os.path.exists(self.work_dir):
            shutil.rmtree(self.work_dir, ignore_errors=True)
