# Controlo de qualidade · ficheiro final ManaBurn_Especial_PreconEmJogo_916.mp4 (02/11/2026)

`qc_video.py --frente manaburn`: 1080×1920 · 30 fps · 79,33 s (75,47 s sem fecho) · −14,8 LUFS · pico −2,3 dBTP · fecho presente a partir de 75,47 s (dif. 0,07) · "Sem problemas mensuráveis".
`bordas.py`: OK (laterais entre 10 e 1068 px, topo a 300 px; medido na render final).
A olho, em quadros reais do ficheiro final: trecho do TUBO sincronizado com a legenda; cartões da comunidade legíveis; fichas com TV inteira e sem corte lateral; quadro do Conde presente nos planos de sala; expressões alternadas; fecho sem sobreposição.
Não conferido: audição humana da mistura.

## v2 (02/11/2026, TV sem corte e fora do ar)
qc_video.py: 1080×1920, 30 fps, 79,33 s, áudio: -14.8 LUFS · pico -2.3 dBTP, fecho a partir de 75,47 s, "Sem problemas mensuráveis".
bordas.py (regra nova): 2255 quadros, 1059 de TV, chassis entre 10 e 1070 px, quadros com TV cortada: 0.
testes_tv.py: 30 quadros consecutivos distintos; determinístico; ~19 ms por quadro.
A olho, 16 quadros do ficheiro final: TV inteira ou fora do quadro; carta/fichas e TV SAL sem interferência; fora do ar nos planos de sala; fecho preservado.
Placa BINDER: posição testada só em prévia, com logo_mark.png. Não está no vídeo.
