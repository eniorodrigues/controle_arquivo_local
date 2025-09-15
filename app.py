from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# ---------------- SUPABASE ----------------
url ="https://fwrrfmzdirgstbidpuad.supabase.co"
key ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3cnJmbXpkaXJnc3RiaWRwdWFkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwODU1OTAsImV4cCI6MjA3MjY2MTU5MH0.HIeEuRNpqIbwAN8yaDEUbm1TLlGX_E12ULvH5-wwKlI"
TABLE_NAME = "controle_arquivo_local"  # Nome da tabela no Supabase
 
supabase: Client = create_client(url, key)

# ---------------- ROTAS ----------------

@app.route("/") 
def index():
    data = supabase.table(TABLE_NAME).select("*").execute()
    registros = data.data
    return render_template("index.html", registros=registros)


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
    app.run(debug=True)