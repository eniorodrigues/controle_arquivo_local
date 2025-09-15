import os
from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

app = Flask(__name__)

# Supabase
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
TABLE_NAME = "controle_arquivo_local"

supabase: Client = create_client(url, key)

@app.route("/") 
def index():
    data = supabase.table(TABLE_NAME).select("*").execute()
    registros = data.data
    return render_template("index.html", registros=registros)

# @app.route("/api/dados", methods=["GET"])
# def api_dados():
#     data = supabase.table(TABLE_NAME).select("*").execute()
#     return jsonify(data.data)

@app.route("/api/dados", methods=["GET"])
def api_dados():
    token = request.args.get("token")
    expected_token = os.getenv("SUPABASE_KEY")  # Define no .env ou no ambiente da Render

    if token != expected_token:
        return jsonify({"error": "Acesso não autorizado"}), 401

    data = supabase.table(TABLE_NAME).select("*").execute()
    return jsonify(data.data)


@app.route("/edit/<int:record_id>", methods=["POST"])
def edit_record(record_id):
    payload = {
        "cliente": request.form.get("cliente"),
        "responsavel": request.form.get("responsavel"),
        "al_2023": request.form.get("al_2023"),
        "status_rel_2024": request.form.get("status_rel_2024"),
        "tipo_al": request.form.get("tipo_al"),
        "anexos_al_rel": request.form.get("anexos_al_rel"),
        "status_trello": request.form.get("status_trello"),
        "observacoes": request.form.get("observacoes")
    }
    supabase.table(TABLE_NAME).update(payload).eq("id", record_id).execute()
    return jsonify({"success": True})

@app.route("/get/<int:record_id>")
def get_record(record_id):
    data = supabase.table(TABLE_NAME).select("*").eq("id", record_id).execute()
    if data.data:
        return jsonify(data.data[0])
    return jsonify({"error": "Registro não encontrado"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
