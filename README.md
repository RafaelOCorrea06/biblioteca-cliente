# Livraria Cliente

Front-end da livraria em arquitetura Cliente-Servidor.

Este repositório é o **cliente**. Ele renderiza as telas em Flask/Jinja e consome o servidor por HTTP/JSON.

## Relação com o repositório servidor

Este cliente depende de um servidor rodando. A ligação entre os dois repositórios é feita pela variável:

```env
API_BASE_URL=http://localhost:5000
```

Em produção, troque pelo link do deploy do servidor:

```env
API_BASE_URL=https://URL-DO-SERVIDOR
```

O arquivo `api_client.py` é o ponto que "importa" o servidor no cliente: ele não acessa arquivos internos do back-end, só chama os endpoints REST.

## Estrutura

```text
templates/       # Telas HTML
static/          # CSS
api_client.py    # Cliente HTTP que consome o servidor
app.py           # Rotas do front-end
```

## Rodando localmente

Primeiro rode o servidor em outro terminal.

Depois, neste repositório:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
set API_BASE_URL=http://localhost:5000
```

Linux/macOS:

```bash
source .venv/bin/activate
export API_BASE_URL=http://localhost:5000
```

Depois:

```bash
pip install -r requirements.txt
python app.py
```

Cliente local:

```text
http://localhost:5001
```

Tela de teste da integração:

```text
http://localhost:5001/teste-backend
```

