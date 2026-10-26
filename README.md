# MiguelCPU

Simulador educativo de um computador e de uma CPU, com motor em Python (Flask) e interfaces em HTML, CSS e JavaScript.

> **Aviso:** este projeto é uma simulação visual. Não mede nem controla o hardware real do computador.

## Requisitos
- Python 3.10 ou superior
- pip

## Executar no Windows
1. Abra o terminal dentro da pasta do projeto.
2. Crie e ative um ambiente virtual (opcional, recomendado):
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Instale as dependências:
   ```powershell
   py -m pip install -r requirements.txt
   ```
4. Inicie o servidor:
   ```powershell
   py main.py
   ```
5. Acesse http://127.0.0.1:5000

## Interfaces
- **PC:** programas simulados, utilização de CPU/memória, frequência, temperatura e controles para abrir/fechar processos.
- **CPU View:** visão interna dos quatro núcleos e oito threads simulados, cache e carga por núcleo.

## Especificações simuladas
- 4 núcleos / 8 threads
- Clock base: 3,2 GHz
- Clock máximo: 4,0 GHz
- Cache L1: 32 KB de dados + 32 KB de instruções por núcleo
- Cache L2: 256 KB por núcleo
- Cache L3: 8 MB compartilhados

Esses valores são fictícios e servem apenas como demonstração.

## Estrutura
```
MiguelCPU/
├── main.py
├── cpu.py
├── requirements.txt
├── README.md
├── pc/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── cpu_view/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── static/
    ├── images/
    └── icons/
```

## Próximas ideias
- Escalonador de processos mais detalhado
- Simulação de cache e instruções
- Turbo boost e thermal throttling
- Modo de stress test visual


## Publicação online

O projeto usa duas partes:

- **Frontend estático:** pasta `docs/`, publicada pelo GitHub Pages.
- **API Flask:** publicada no Render com a configuração `render.yaml`.

### Render
1. Importe este repositório no Render como um Web Service ou use o Blueprint a partir do `render.yaml`.
2. Confirme o serviço `miguelcpu-api` e aguarde o deploy.
3. Se o Render atribuir uma URL diferente de `https://miguelcpu-api.onrender.com`, atualize `docs/config.js` para a URL real.

### GitHub Pages
1. Abra **Settings → Pages** no repositório.
2. Em **Build and deployment**, escolha **Deploy from a branch**.
3. Selecione a branch `main` e a pasta `/docs`, depois salve.
4. O frontend usa `docs/config.js` para acessar a API publicada no Render.

A API permite chamadas do site em `https://migdaPipoca.github.io`. Os dados continuam sendo simulados e não vêm dos sensores reais do computador.
