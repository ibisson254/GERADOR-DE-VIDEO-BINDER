"""Voz PROVISÓRIA local (Piper pt-BR edresson-low, tom subido) + Rhubarb por fala. NÃO PUBLICÁVEL.
uso: python3 -I voz_provisoria.py MODELO.onnx RHUBARB PASTA_SAIDA
Saída: <id>.wav (44,1 kHz mono) e <id>.json (bocas) por fala, e duracoes.json."""
import json, os, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
modelo, rhubarb, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
dur = {}
for f in json.load(open(os.path.join(AQUI, 'falas.json'))):
    raw, wav, txt = (os.path.join(out, f['id'] + s) for s in ('_raw.wav', '.wav', '.txt'))
    open(txt, 'w').write(f['texto'])
    subprocess.run([sys.executable, '-m', 'piper', '-m', modelo, '-f', raw, '--length_scale', '1.02'],
                   input=f['texto'].encode(), check=True, stderr=subprocess.DEVNULL)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-af',
                    'aresample=44100,rubberband=pitch=1.40:tempo=1.22:formant=preserved:pitchq=quality,silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,highpass=f=120,'
                    'equalizer=f=3000:t=q:w=1.2:g=2,loudnorm=I=-18:TP=-3', '-ar', '44100', wav], check=True)
    subprocess.run([rhubarb, '-q', '-r', 'phonetic', '-f', 'json', '--dialogFile', txt, '-o',
                    os.path.join(out, f['id'] + '.json'), wav], check=True)
    d = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', wav]))
    dur[f['id']] = round(d, 3)
    print(f['id'], f'{d:.2f}s', f['texto'])
json.dump(dur, open(os.path.join(out, 'duracoes.json'), 'w'), indent=1)
