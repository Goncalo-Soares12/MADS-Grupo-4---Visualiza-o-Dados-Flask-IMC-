from flask import Flask, request, redirect
import pandas as pd
import datetime

app = Flask(__name__)

EXCEL_PATH = './dados/dados_pessoais_com_imc.xlsx'
SHEET_NAME = 'Sheet1'

titleico = "<title>Dados Públicos e Privados</title><link rel='icon' type='image/png' href='https://cdn-icons-png.flaticon.com/512/3105/3105825.png'>"
datatables_css_js = """
<!-- DataTables -->
<link rel="stylesheet" href="https://cdn.datatables.net/1.13.4/css/jquery.dataTables.min.css">
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
<script>
    $(document).ready(function () {
        $('table').DataTable({
            language: {
                url: "//cdn.datatables.net/plug-ins/1.13.4/i18n/pt-PT.json"
            }
        });
    });
</script>
"""

bodyfont = '<body style="font-family: Roboto, sans-serif; margin: 40px;">'
disclaimer = "<div style='background-color:#FFD580; padding:10px; border:1px solid orange;'><b>Estes dados são fictícios e utilizados apenas para fins educativos.</b></div><br>"
agora = str(datetime.datetime.now())[0:19]
bottomline = f"<hr color=green><small><i>{agora} | exemplo educativo</i></small>"

keyword = ""
nif_digitado = ""

def load_data():
    return pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)

@app.route("/", methods=["GET", "POST"])
def home():
    global keyword, nif_digitado
    df = load_data()

    public_cols = ['Idade', 'Altura (m)', 'Peso (kg)', 'IMC']
    tabela = df[public_cols].to_html(index=False, classes='display', justify='center')

    explicacao_imc = """
    <div style='text-align: justify; max-width: 850px; margin: auto;'>
        <h2>🔍 O que é o IMC?</h2>
        <p>O <strong>Índice de Massa Corporal (IMC)</strong> é uma ferramenta simples usada para avaliar se uma pessoa está com o peso adequado em relação à sua altura.</p>
        <p><strong>Como calcular:</strong> divida o peso (em kg) pela altura (em metros) elevada ao quadrado:</p>
        <p style='text-align: center; font-size: 1.2em;'><b>IMC = Peso (kg) / Altura² (m²)</b></p>
        <h4>📊 Classificações de IMC:</h4>
        <ul>
            <li><b>&lt; 18.5:</b> Abaixo do peso</li>
            <li><b>18.5 - 24.9:</b> Peso normal ✅</li>
            <li><b>25 - 29.9:</b> Sobrepeso ⚠️</li>
            <li><b>&ge; 30:</b> Obesidade 🚨</li>
        </ul>
        <p>Essas categorias ajudam a identificar possíveis riscos à saúde e motivar hábitos mais saudáveis.</p>
    </div><br>
    """

    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip().lower()
        if keyword == "acesso1":
            return redirect("/privado1")
        elif keyword == "acesso2":
            return redirect("/privado2")
        elif keyword.isdigit() and int(keyword) in df['NIF'].values:
            nif_digitado = int(keyword)
            return redirect("/privado3")
        else:
            return render_page("Página Pública", explicacao_imc + tabela, erro="Palavra-passe incorreta", mostrar_form=True)

    return render_page("Página Pública", explicacao_imc + tabela, mostrar_form=True)

@app.route("/privado1")
def privado1():
    if keyword != "acesso1":
        return redirect("/")
    df = load_data()
    cols = ['Nome', 'Idade', 'Altura (m)', 'Peso (kg)', 'IMC', 'Telefone', 'NIF', 'Email']
    tabela = df[cols].to_html(index=False, classes='display', justify='center')
    return render_page("🔐 Dados Privados - Nível 1", tabela, link_home=True)

@app.route("/privado2")
def privado2():
    if keyword != "acesso2":
        return redirect("/")
    df = load_data()
    if 'Morada' in df.columns:
        df = df.drop(columns=['Morada'])
    tabela = df.to_html(index=False, classes='display', justify='center')
    return render_page("🔐 Dados Privados - Nível 2", tabela, link_home=True)

@app.route("/privado3")
def privado3():
    global nif_digitado
    df = load_data()
    pessoa = df[df["NIF"] == nif_digitado]
    if pessoa.empty:
        return redirect("/")
    tabela = pessoa.to_html(index=False, classes='display', justify='center')
    return render_page("🔐 Acesso Individual por NIF", tabela, link_home=True)

def render_page(titulo, tabela_html, erro=None, link_home=False, mostrar_form=False):
    erro_html = f"<p style='color:red; font-weight:bold'>{erro}</p>" if erro else ""
    link_back = "<a href='/' style='text-decoration:none;'>⬅️ Voltar à Página Principal</a><br><br>" if link_home else ""

    form_html = """
        <form method="post" style="margin-top:20px;">
            <input name="keyword" type="password" placeholder="Digite a palavra-passe" style="padding:8px; width:250px;">
            <input type="submit" value="Aceder" style="padding:8px;">
        </form>
    """ if mostrar_form else ""

    return f"""
        <!doctype html>
        {titleico}
        {datatables_css_js}
        {bodyfont}
        <h1 style='text-align:center'>{titulo}</h1>
        {disclaimer}
        {link_back}
        <div>{tabela_html}</div>
        {erro_html}
        {form_html}
        {bottomline}</body></html>
    """

if __name__ == "__main__":
    app.run(debug=True)
