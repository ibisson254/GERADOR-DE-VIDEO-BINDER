#!/usr/bin/env python3
"""Testes do QC automático (qc_video.py) e da regressão de imagem (comparar_videos.py) com vídeos sintéticos.

Vídeos gerados na hora com o ffmpeg (lavfi) + o fecho oficial; nada de episódios reais, nada de rede, zero créditos.
Uso: python3 -I comum/qc/test_qc.py     (salta com aviso se o ffmpeg ou o numpy/Pillow não existirem)
"""
import json, os, shutil, subprocess, sys, tempfile, unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
FECHO = os.path.join(RAIZ, 'comum', 'outro', 'outro_binder_916.mp4')
TEM = shutil.which('ffmpeg') and shutil.which('ffprobe')
try:
    import numpy, PIL  # noqa: F401
except ImportError:
    TEM = False


def ff(*a):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)


def corpo(saida, preto=False, som='sine', vol=0.25):
    """2 s de muro rosa (+1 s preto + 2 s rosa se preto=True) seguidos do fecho oficial, com áudio de teste"""
    pecas = ['color=c=0xE61E6E:s=1080x1920:r=30:d=2'] + (['color=c=black:s=1080x1920:r=30:d=1',
                                                        'color=c=0xE61E6E:s=1080x1920:r=30:d=2'] if preto else [])
    args = []
    for p in pecas:
        args += ['-f', 'lavfi', '-i', p]
    args += ['-i', FECHO]
    n = len(pecas) + 1
    dur = 2 + (3 if preto else 0) + 3.87
    src = f'sine=f=330:d={dur}' if som == 'sine' else f'anullsrc=r=48000:cl=stereo:d={dur}'
    args += ['-f', 'lavfi', '-i', src]
    fc = ''.join(f'[{i}:v]scale=1080:1920,setsar=1,fps=30[v{i}];' for i in range(n))
    fc += ''.join(f'[v{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=0[v];[{n}:a]volume={vol},aresample=48000,aformat=channel_layouts=stereo[a]'
    ff(*args, '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
       '-c:a', 'aac', '-shortest', saida)


def qc(video, frente, pasta):
    r = subprocess.run([sys.executable, '-I', os.path.join(AQUI, 'qc_video.py'), video, '--frente', frente, '--saida', pasta],
                       capture_output=True, text=True)
    with open(os.path.join(pasta, 'qc.json'), encoding='utf-8') as fh:
        return r.returncode, json.load(fh)


@unittest.skipUnless(TEM, 'ffmpeg/ffprobe, numpy ou Pillow em falta')
class TesteQC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp(prefix='qc_teste_')
        cls.ok = os.path.join(cls.d, 'ok.mp4'); corpo(cls.ok)
        cls.preto = os.path.join(cls.d, 'preto.mp4'); corpo(cls.preto, preto=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.d, ignore_errors=True)

    def test_fecho_e_formato(self):
        rc, j = qc(self.ok, 'lambe', os.path.join(self.d, 'q1'))
        self.assertEqual(rc, 0)
        self.assertTrue(j['fecho']['presente'])
        self.assertAlmostEqual(j['duracao_sem_fecho'], 2.0, delta=0.15)
        self.assertEqual((j['formato']['vcodec'], j['formato']['pix_fmt']), ('h264', 'yuv420p'))

    def test_lambe_nao_exige_14_lufs(self):
        # o seno de teste fica longe de −14 LUFS: no Lambe-lambe o loudness é só informativo (música no Instagram)
        _, j = qc(self.ok, 'lambe', os.path.join(self.d, 'q2'))
        self.assertFalse([t for g, t in j['problemas'] if 'loudness' in t])
        _, j = qc(self.ok, 'conde', os.path.join(self.d, 'q3'))
        self.assertTrue([t for g, t in j['problemas'] if 'loudness' in t])

    def test_quadros_pretos_no_corpo(self):
        _, j = qc(self.preto, 'conde', os.path.join(self.d, 'q4'))
        self.assertTrue([t for g, t in j['problemas'] if g == 'P1' and 'pretos' in t], j['problemas'])
        _, j = qc(self.ok, 'conde', os.path.join(self.d, 'q5'))
        self.assertFalse([t for g, t in j['problemas'] if 'pretos' in t], j['problemas'])

    def test_sem_fecho_e_p0(self):
        sem = os.path.join(self.d, 'sem.mp4')
        ff('-f', 'lavfi', '-i', 'color=c=0xE61E6E:s=1080x1920:r=30:d=5', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', sem)
        rc, j = qc(sem, 'lambe', os.path.join(self.d, 'q6'))
        self.assertEqual(rc, 1)
        self.assertTrue([t for g, t in j['problemas'] if g == 'P0' and 'fecho' in t])

    def test_comparar_videos(self):
        cmp = [sys.executable, '-I', os.path.join(AQUI, 'comparar_videos.py')]
        self.assertEqual(subprocess.run(cmp + [self.ok, self.ok], capture_output=True).returncode, 0)
        self.assertEqual(subprocess.run(cmp + [self.ok, self.preto], capture_output=True).returncode, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
