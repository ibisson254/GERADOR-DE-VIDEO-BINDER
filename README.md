# GERADOR-DE-VIDEO-BINDER

Kit de produção automatizada de Reels 9:16 (1080×1920, 30 fps) para o Instagram [@binderthetrade](https://instagram.com/binderthetrade).

## Estrutura do Repositório

```
/
├── README.md
├── .gitignore
├── manaburn/         # Gerador Mana & Burn (HTML/Playwright + ffmpeg)
│   └── musica/       # Trilhas sonoras originais
├── conde/            # Montador O Tribunal Estético (Pillow + ffmpeg)
│   ├── CONTEXTO.md   # Diretrizes, tom e regras de produção
│   ├── assets/       # Retrato oficial e expressões do Conde
│   ├── legendas/     # Legendas dos episódios
│   └── musica/       # Tema oficial (tema.mp3)
├── oraculo/          # Oráculo de Tubo — personagem TUBO (análise competitiva)
│   ├── CONTEXTO.md   # Personagem, ambientação, tipos de episódio e regras
│   ├── assets/       # Imagem-mestra do TUBO
│   └── legendas/     # Legendas dos episódios
└── comum/
    └── historico.md  # Histórico de desempenho e métricas
```

## Como Usar (Claude / Agentes)

Clone o repositório com profundidade 1 e acesse a pasta da série desejada:

```bash
git clone --depth 1 https://github.com/ibisson254/GERADOR-DE-VIDEO-BINDER.git
cd GERADOR-DE-VIDEO-BINDER/conde     # Para O Tribunal Estético
# ou
cd GERADOR-DE-VIDEO-BINDER/manaburn  # Para Mana & Burn
# ou
cd GERADOR-DE-VIDEO-BINDER/oraculo   # Para Oráculo de Tubo (TUBO)
```

## Dependências

- **Sistema:** Python 3, `ffmpeg`, fontes Lora (Google Fonts).
- **Python:** `numpy`, `scipy`, `Pillow`, `playwright` (+ Chromium: `playwright install chromium`), `num2words` (`librosa` opcional).

## Direitos Autorais e Créditos

- Imagens e propriedades de Magic: The Gathering são © Wizards of the Coast LLC. Conteúdo de fã não oficial, sem aprovação ou endosso da Wizards.
- Trilhas musicais e vozes sintetizadas criadas via ElevenLabs pelo autor do projeto para o canal @binderthetrade.
