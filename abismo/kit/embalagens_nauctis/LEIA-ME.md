# Embalagens oficiais · decks de Commander de Nauctis

Imagens de produto da Wizards of the Coast (página «Collecting Nauctis: The Sunken Realm», 13/11/2026), recortadas do fundo branco para as peças do ABISMO (AB-04 v2, AB-05 a AB-10). **Não são versionadas** (© Wizards, como as cartas): o PNG fica em `saida/` (ignorada pelo Git).

Recriar (raiz do repositório), a partir das imagens 1920×1080 de fundo branco:

```
python3 -I abismo/kit/embalagens_nauctis/preparar.py merfolk=<img> terrors=<img> blood=<img> seal=<img>
```

| Ficheiro | Produto | Origem usada a 20/11/2026 |
|---|---|---|
| `saida/merfolk.png` | Merfolk Regiment (padrão) | enviada pelo fundador (1000154096.jpg) |
| `saida/terrors.png` | Terrors of the Abyss (padrão) | enviada pelo fundador (1000154094.jpg) |
| `saida/blood.png` | Blood in the Water (padrão) | enviada pelo fundador (1000154095.jpg) |
| `saida/seal.png` | Seal the Deal (**Premium Edition**) | enviada pelo fundador (1000154097.jpg) |

URLs oficiais (padrão): `https://media.wizards.com/2026/images/daily/jQEVaVecs4/en_CU1EyxtKT6Xc.webp` (Merfolk), `en_tFfZG6evMEgC.webp` (Terrors), `en_KJnHC6PlT8Db.webp` (Blood), `en_4nlrWcqKiFRj.webp` (Seal). O domínio está bloqueado no ambiente cloud do Claude; por isso as imagens chegam pelo fundador.

Regras: identificar sempre como «Embalagem oficial» no crédito; nunca recortar a caixa para parecer uma carta; não alterar a arte.
