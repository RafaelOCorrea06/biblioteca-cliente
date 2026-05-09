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

## Deploy no Render

1. Faça deploy do repositório `livraria-servidor` primeiro.
2. Copie a URL do servidor.
3. Crie outro repositório no GitHub chamado `livraria-cliente`.
4. Envie este código para ele.
5. No Render, escolha **New > Web Service**.
6. Conecte o repositório `livraria-cliente`.
7. Use:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
8. Configure a variável:

```env
API_BASE_URL=https://URL-DO-SERVIDOR
```

## Entrega do laboratório

Entregue:

```text
Link do front-end:
https://URL-DO-CLIENTE

Link do back-end:
https://URL-DO-SERVIDOR

Função de teste do back-end:
https://URL-DO-SERVIDOR/api/debug/teste
```
