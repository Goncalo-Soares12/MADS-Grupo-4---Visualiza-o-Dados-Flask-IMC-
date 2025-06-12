from flask import Flask, request, redirect, render_template
import pandas as pd
import datetime
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)

# Configuração do Google Sheets
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
SHEET_ID = '1QPioUWqLQ0v5HZ4An0exK52sNCOSIyiDsxpMgM0cKxA'

# Caminhos possíveis para o arquivo de credenciais
SECRET_PATHS = [
    '/etc/secrets/tasty-2-0-e6fb412ba5ff.json',  # Para produção (Secret Files)
    'secrets/tasty-2-0-e6fb412ba5ff.json'  # Para desenvolvimento local
]

def get_credentials():
    # Procura o arquivo de credenciais nos caminhos possíveis
    for creds_path in SECRET_PATHS:
        if os.path.exists(creds_path):
            try:
                return ServiceAccountCredentials.from_json_keyfile_name(creds_path, SCOPE)
            except Exception as e:
                print(f"Erro ao carregar credenciais de {creds_path}: {str(e)}")
    
    raise Exception("Nenhum arquivo de credenciais válido encontrado nos caminhos: " + ", ".join(SECRET_PATHS))

# Inicializa o cliente do Google Sheets
try:
    creds = get_credentials()
    client = gspread.authorize(creds)
except Exception as e:
    print(f"Falha na autenticação: {str(e)}")
    client = None

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

def calcular_idade(data_nascimento):
    hoje = datetime.datetime.today()
    return hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

def load_data():
    try:
        sheet = client.open_by_key(SHEET_ID).sheet1
        records = sheet.get_all_records()
        df = pd.DataFrame(records)
        
        # Conversão de tipos
        df['Data de Nascimento'] = pd.to_datetime(df['Data de Nascimento'])
        df['Idade'] = df['Data de Nascimento'].apply(calcular_idade)
        
        # Garante que latitude e longitude são numéricas
        df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
        df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
        
        # Remove linhas com valores inválidos
        df = df.dropna(subset=['Latitude', 'Longitude'])
        
        return df
    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro

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
            <li><b>&lt; 18.5:</b> Abaixo do peso 💀🦴</li>
            <li><b>18.5 - 24.9:</b> Peso normal ✅🧍‍♂️🧍‍♀️</li>
            <li><b>25 - 29.9:</b> Sobrepeso ⚠️</li>
            <li><b>&ge; 30:</b> Obesidade <img src="static/obesidade.ico" alt="Obesidade" style="width:20px; vertical-align:middle;"></li>
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
    cols = ['Nome', 'Idade', 'Altura (m)', 'Peso (kg)', 'IMC', 'Telefone', 'NIF', 'Email', 'Género']
    tabela = df[cols].to_html(index=False, classes='display', justify='center')

    fig = px.scatter(df, x='Altura (m)', y='Peso (kg)', color='Género', title='Peso vs Altura')
    graph_html = fig.to_html(full_html=False)

    return render_page("🔐 Dados Privados - Nível 1", tabela + graph_html, link_home=True)

@app.route("/privado2")
def privado2():
    if keyword != "acesso2":
        return redirect("/")
    
    df = load_data()
    
    # Verifica se há dados válidos
    if df.empty or 'Latitude' not in df.columns or 'Longitude' not in df.columns:
        return render_page("🔐 Dados Privados - Nível 2", 
                         "<p style='color:red'>Dados de localização inválidos ou não encontrados</p>", 
                         link_home=True)
    
    # Cria o mapa
    try:
        center_lat = df['Latitude'].mean()
        center_lon = df['Longitude'].mean()
    except:
        center_lat = df['Latitude'].iloc[0]
        center_lon = df['Longitude'].iloc[0]
    
    mapa = folium.Map(location=[center_lat, center_lon], zoom_start=6)
    marker_cluster = MarkerCluster().add_to(mapa)

    for _, row in df.iterrows():
        imc = row['IMC']
        if imc < 18.5:
            icon_color = 'blue'
        elif imc < 25:
            icon_color = 'green'
        elif imc < 30:
            icon_color = 'orange'
        else:
            icon_color = 'red'

        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Nome']} - IMC: {imc:.1f}",
            icon=folium.Icon(color=icon_color)
        ).add_to(marker_cluster)

    # Retorna incorporando o mapa diretamente
    return render_page("🔐 Dados Privados - Nível 2", 
                      mapa._repr_html_(), 
                      link_home=True)

@app.route("/privado3")
def privado3():
    global nif_digitado
    df = load_data()
    pessoa = df[df["NIF"] == nif_digitado]
    if pessoa.empty:
        return redirect("/")

    tabela = pessoa.to_html(index=False, classes='display', justify='center')

    fig1 = px.scatter(pessoa, x='Altura (m)', y='Peso (kg)', title='Peso vs Altura')
    graph1_html = fig1.to_html(full_html=False)

    datas = pd.date_range(end=datetime.datetime.today(), periods=5).to_pydatetime().tolist()
    imcs = [pessoa['IMC'].values[0] - i for i in range(5)]
    fig2 = px.line(x=datas, y=imcs, labels={'x': 'Data', 'y': 'IMC'}, title='Evolução do IMC')
    graph2_html = fig2.to_html(full_html=False)

    return render_page("🔐 Acesso Individual por NIF", tabela + graph1_html + graph2_html, link_home=True)

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
    app.run()
