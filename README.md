# DivisorRoteiro

Aplicação Python e Streamlit para dividir um roteiro, de forma totalmente determinística, em prompts de aproximadamente oito segundos. Nenhuma IA é usada na divisão.

## Como funciona

1. O tempo é convertido de `MM:SS` ou `HH:MM:SS` para segundos.
2. A quantidade de prompts é `ceil(segundos / 8)`.
3. O roteiro é tokenizado exclusivamente com `texto.split()`.
4. Cada token recebe um peso determinístico de fala baseado em grupos vocálicos, extensão da palavra e pausas de pontuação.
5. A otimização global minimiza primeiro a variância do número de palavras. Sempre que matematicamente possível, os segmentos diferem por no máximo uma palavra.
6. Entre todas as distribuições de variância mínima, uma programação dinâmica escolhe conjuntamente a ordem dos tamanhos que melhor preserva pontuação, transições, construções contínuas e ritmo de fala.
7. Uma etapa final de rebalanceamento transfere fronteiras adjacentes sempre que isso reduz a variância, eliminando segmentos extremamente curtos ou longos.
8. A saída é validada token a token e por continuidade de índices e tempos.

O algoritmo nunca corrige, reescreve, remove, duplica ou move tokens. Espaços em branco do texto de entrada são normalizados ao exibir os prompts, consequência direta da tokenização exigida por `split()`; o conteúdo e a ordem de cada token permanecem idênticos.

## Requisitos

- Python 3.10 ou superior

## Instalação

No terminal do VS Code, dentro da pasta do projeto:

```bash
python -m venv .venv
```

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

macOS ou Linux:

```bash
source .venv/bin/activate
```

Instale a dependência:

```bash
python -m pip install -r requirements.txt
```

## Execução

```bash
streamlit run app.py
```

A interface mostra tempo, total de palavras, quantidade de prompts, média, menor e maior prompt e desvio padrão. Os resultados podem ser baixados em TXT, Markdown e CSV.

## Uso em Python

```python
from segmentador import Segmentador

segmentador = Segmentador("Primeira frase. Segunda frase!", "00:16")
prompts = segmentador.dividir()
estatisticas = segmentador.estatisticas()
```

## Estrutura

```text
DivisorRoteiro/
├── app.py
├── segmentador.py
├── formatter.py
├── validator.py
├── exportador.py
├── requirements.txt
├── README.md
└── outputs/
```
