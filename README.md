# GERADOR-DE-VIDEO-BINDER

Kit de produção automatizada de Reels 9:16 (1080×1920, 30 fps) para o Instagram [@binderthetrade](https://instagram.com/binderthetrade).

## Estrutura do Repositório

```
/
├── CLAUDE.md         # Entrada obrigatória dos agentes (AGENTS.md aponta para ele)
├── README.md
├── manaburn/         # Mana & Burn · PERFIL.md + gerador (HTML/Playwright + ffmpeg)
├── conde/            # Conde de Manaforte · O Tribunal Estético · PERFIL.md + CONTEXTO.md
├── oraculo/          # Meta em Curto (TUBO, ex-Oráculo de Tubo) · PERFIL.md + CONTEXTO.md
└── comum/
    ├── originals/    # Constituição BINDER Originals, checklist, modelos, registo de decisões
    ├── outro/        # Fecho obrigatório com o scanner real
    ├── historico.md  # Desempenho e previsões
    └── easter_eggs.md
```

## Como Usar (Claude / Agentes)

Ler primeiro o [`CLAUDE.md`](CLAUDE.md). Depois, clonar com profundidade 1 e usar a pasta da série:

```bash
git clone --depth 1 https://github.com/ibisson254/GERADOR-DE-VIDEO-BINDER.git
cd GERADOR-DE-VIDEO-BINDER/conde     # Conde de Manaforte
cd GERADOR-DE-VIDEO-BINDER/manaburn  # Mana & Burn
cd GERADOR-DE-VIDEO-BINDER/oraculo   # Meta em Curto (TUBO)
```

## Dependências

- **Sistema:** Python 3, `ffmpeg`, fontes Lora (Google Fonts).
- **Python:** `numpy`, `scipy`, `Pillow`, `playwright` (+ Chromium: `playwright install chromium`), `num2words` (`librosa` opcional).

## Direitos Autorais e Créditos

- Imagens e propriedades de Magic: The Gathering são © Wizards of the Coast LLC. Conteúdo de fã não oficial, sem aprovação ou endosso da Wizards.
- Trilhas musicais e vozes sintetizadas criadas via ElevenLabs pelo autor do projeto para o canal @binderthetrade.
