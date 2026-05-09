# Contrato da API - Livraria Cliente-Servidor

O repositório `livraria-cliente` não importa classes Python do servidor.
Ele importa/consome o servidor por HTTP, usando a variável de ambiente `API_BASE_URL`.

## Base URL

Local:

```text
http://localhost:5000
```

Produção:

```text
https://URL-DO-SERVIDOR
```

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/health` | Teste simples de saúde do servidor |
| GET | `/api/debug/teste` | Função de teste para entrega/deploy |
| GET | `/api/dashboard` | Dados resumidos para a tela inicial |
| GET | `/api/books` | Lista todos os livros |
| GET | `/api/books?q=termo` | Pesquisa por título, autor ou categoria |
| GET | `/api/books/<id>` | Detalhes de um livro |
| POST | `/api/books` | Cria livro |
| DELETE | `/api/books/<id>` | Remove livro |
| POST | `/api/books/<id>/borrow` | Empresta livro |
| POST | `/api/books/<id>/return` | Devolve livro |

## Exemplo de criação de livro

```bash
curl -X POST http://localhost:5000/api/books \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Arquitetura Limpa","autor":"Robert C. Martin","categoria":"Tecnologia","ano":2017,"resumo":"Exemplo","disponivel":true}'
```
