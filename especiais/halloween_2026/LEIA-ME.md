# Especial de Halloween 2026 · Innistrad × Duskmourn: O Julgamento do Horror

Crossover BINDER Originals (Mana & Burn + Conde de Manaforte + TUBO). Dossier completo (pesquisa, guião, storyboard, prompts, voz, música, montagem, legenda): documento "Especial de Halloween · Innistrad × Duskmourn — dossier de produção" no claude.ai.

Estado (31/10/2026): PRÉVIA montada (94,9 s). Faltam a voz do Conde e do TUBO (créditos ElevenLabs esgotados: 89) e o tema musical original.

## Como finalizar
Pasta de trabalho com: estes scripts, `vozes/burn_raw.mp3`, `vozes/mana_raw.mp3` (flow ElevenLabs "BINDER Especial Halloween · Innistrad x Duskmourn"),
`vozes/conde_raw.mp3`, `vozes/tubo_raw.mp3` (prompts em roteiro.json → tts_pendente), `musica/tema_especial.mp3` (opcional; sem ele usa os temas das séries),
cartas do Scryfall em /root/work/cards (`<chave>.png` e `<chave>_art.jpg`; chaves e sets em cartas_meta.json) e a pasta `mb/` com links para manaburn/node_modules, tv_asset.png, logo e cards/main.png (Emrakul EMN 6).

    python3 vozes.py && python3 tl.py && python3 render_mb.py && python3 render.py && python3 mix.py
    python3 ../../manaburn/episodios/ep09_dack/fecho_scanner.py ../.. fecho.mp4 && python3 build.py && python3 capa.py

QC: ffprobe (1080x1920, 30 fps), cropdetect sem corte lateral, ebur128 (-14 LUFS, pico < -1), quadros de cada cena.
