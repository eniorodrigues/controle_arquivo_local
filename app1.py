from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

# Conexão com SQL Server usando autenticação do Windows
def get_connection():
    return pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=ENIOBLUEMIND;'  # use ENIOBLUEMIND\SQLEXPRESS se for o caso
        r'DATABASE=PBI;'
        r'Trusted_Connection=yes;'
    )

# Página inicial com todos os registros
@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Controle_Arquivo_Local")
    registros = cursor.fetchall()
    conn.close()
    return render_template('index.html', registros=registros)

# Rota para adicionar novo registro
@app.route('/adicionar', methods=['POST'])
def adicionar():
    dados = (
        request.form['cliente'],
        request.form['responsavel'],
        request.form['al_2023'],
        request.form['status_rel_2024'],
        request.form['tipo_al'],
        request.form['anexos_al_rel'],
        request.form['status_trello'],
        request.form['observacoes'],
    )
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Controle_Arquivo_Local (
            Cliente, Responsavel, AL_2023, Status_Rel_2024,
            Tipo_AL, Anexos_AL_Rel, Status_Trello, Observações
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, dados)
    conn.commit()
    conn.close()
    return redirect('/')

# Rota para exibir tela de edição
@app.route('/editar/<int:id>')
def editar(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Controle_Arquivo_Local WHERE Id = ?", (id,))
    registro = cursor.fetchone()
    conn.close()
    return render_template('editar.html', registro=registro)

# Rota para atualizar registro
@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    dados = (
        request.form['cliente'],
        request.form['responsavel'],
        request.form['al_2023'],
        request.form['status_rel_2024'],
        request.form['tipo_al'],
        request.form['anexos_al_rel'],
        request.form['status_trello'],
        request.form['observacoes'],
        id
    )
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Controle_Arquivo_Local
        SET Cliente = ?, Responsavel = ?, AL_2023 = ?, Status_Rel_2024 = ?,
            Tipo_AL = ?, Anexos_AL_Rel = ?, Status_Trello = ?, Observações = ?
        WHERE Id = ?
    """, dados)
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
