from __future__ import annotations

import os

from flask import Flask, flash, redirect, render_template, request, url_for

from api_client import ApiClient, BackendUnavailableError


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "livraria-frontend-secret")
    api = ApiClient()

    @app.context_processor
    def inject_config():
        return {"api_base_url": api.base_url}

    @app.get("/teste-backend")
    def teste_backend():
        """Tela do cliente que importa/consome o servidor usando API_BASE_URL."""
        try:
            health = api.health()
            debug = api._request("GET", "/api/debug/teste")
            return render_template("teste_backend.html", health=health, debug=debug)
        except BackendUnavailableError as exc:
            flash(str(exc), "error")
            return redirect(url_for("index"))

    @app.get("/")
    def index():
        term = request.args.get("q", "").strip()
        try:
            dashboard = api.dashboard()
            books = api.list_books(term)["items"][:4]
        except BackendUnavailableError as exc:
            flash(str(exc), "error")
            dashboard = {"total_livros": 0, "disponiveis": 0, "indisponiveis": 0, "categorias": 0, "emprestimos_ativos": 0}
            books = []
        return render_template("index.html", books=books, dashboard=dashboard, term=term)

    @app.get("/catalogo")
    def catalogo():
        term = request.args.get("q", "").strip()
        try:
            data = api.list_books(term)
            books = data["items"]
        except BackendUnavailableError as exc:
            flash(str(exc), "error")
            books = []
        return render_template("catalogo.html", books=books, term=term)

    @app.get("/livros/<int:book_id>")
    def detalhes_livro(book_id: int):
        try:
            book = api.get_book(book_id)
        except BackendUnavailableError as exc:
            flash(str(exc), "error")
            return redirect(url_for("catalogo"))
        return render_template("livro.html", book=book)

    @app.route("/livros/novo", methods=["GET", "POST"])
    def novo_livro():
        if request.method == "POST":
            payload = {
                "titulo": request.form.get("titulo", ""),
                "autor": request.form.get("autor", ""),
                "categoria": request.form.get("categoria", ""),
                "ano": request.form.get("ano", ""),
                "resumo": request.form.get("resumo", ""),
                "disponivel": request.form.get("disponivel") == "on",
            }
            try:
                api.create_book(payload)
            except BackendUnavailableError as exc:
                flash(str(exc), "error")
                return render_template("novo_livro.html", form_data=payload), 400

            flash("Livro cadastrado com sucesso.", "success")
            return redirect(url_for("catalogo"))

        return render_template("novo_livro.html", form_data={})

    @app.post("/livros/<int:book_id>/excluir")
    def excluir_livro(book_id: int):
        try:
            api.delete_book(book_id)
            flash("Livro removido com sucesso.", "success")
        except BackendUnavailableError as exc:
            flash(str(exc), "error")
        return redirect(url_for("catalogo"))

    @app.post("/livros/<int:book_id>/emprestar")
    def emprestar_livro(book_id: int):
        borrower_name = request.form.get("borrower_name", "")
        try:
            api.borrow_book(book_id, borrower_name)
            flash("Livro emprestado com sucesso.", "success")
        except BackendUnavailableError as exc:
            flash(str(exc), "error")
        return redirect(url_for("detalhes_livro", book_id=book_id))

    @app.post("/livros/<int:book_id>/devolver")
    def devolver_livro(book_id: int):
        try:
            api.return_book(book_id)
            flash("Livro devolvido com sucesso.", "success")
        except BackendUnavailableError as exc:
            flash(str(exc), "error")
        return redirect(url_for("detalhes_livro", book_id=book_id))

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    app.run(host="0.0.0.0", port=port, debug=True)
