"""Gera as faixas de áudio do Burn e do Mana com pausas de 1.0s entre falas,
prontas para o process.py fatiar e sincronizar.
"""
import asyncio, json, pathlib, subprocess, wave
import numpy as np
import edge_tts

ROOT = pathlib.Path(__file__).parent.resolve()
EPI = json.loads((ROOT / 'episode.json').read_text(encoding='utf-8'))
SR = 44100

async def gen_voice(texts, voice, rate, pitch, out_mp3):
    tmp_dir = ROOT / '_audio_tmp'
    tmp_dir.mkdir(exist_ok=True)
    wav_parts = []
    silence = np.zeros(int(1.0 * SR), dtype=np.float32)

    for i, t in enumerate(texts):
        # Remove asteriscos (marcação de legenda amarela)
        clean_text = t.replace('*', '')
        part_mp3 = tmp_dir / f'part_{i:02d}.mp3'
        part_wav = tmp_dir / f'part_{i:02d}.wav'
        
        communicate = edge_tts.Communicate(clean_text, voice, rate=rate, pitch=pitch)
        await communicate.save(str(part_mp3))
        
        # Converte para WAV mono 44100Hz
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(part_mp3),
                        '-ac', '1', '-ar', str(SR), str(part_wav)], check=True)
        
        with wave.open(str(part_wav), 'rb') as w:
            data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
            wav_parts.append(data)
            if i < len(texts) - 1:
                wav_parts.append(silence)

    full_audio = np.concatenate(wav_parts)
    full_audio = np.clip(full_audio, -1.0, 1.0)
    full_wav = ROOT / (out_mp3.stem + '.wav')
    with wave.open(str(full_wav), 'wb') as o:
        o.setnchannels(1)
        o.setsampwidth(2)
        o.setframerate(SR)
        o.writeframes((full_audio * 32767).astype('<i2').tobytes())

    # Converte para MP3 para o process.py
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(full_wav),
                    '-c:a', 'libmp3lame', '-b:a', '192k', str(out_mp3)], check=True)
    full_wav.unlink()
    print(f'Pronto: {out_mp3} ({len(full_audio)/SR:.2f}s)')

async def main():
    print('Gerando voz do Burn (AntonioNeural, ritmo rápido, rouco)...')
    await gen_voice(EPI['B'], 'pt-BR-AntonioNeural', '+14%', '+2Hz', ROOT / 'burn.mp3')
    
    print('Gerando voz do Mana (AntonioNeural com pitch mais grave e ritmo calmo/lento)...')
    await gen_voice(EPI['M'], 'pt-BR-AntonioNeural', '-8%', '-6Hz', ROOT / 'mana.mp3')

if __name__ == '__main__':
    asyncio.run(main())
