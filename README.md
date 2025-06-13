# 🌐 Sistema de Visualização de Dados com Render - IMC

Este é um projeto web em Python/Flask que apresenta uma página pública e áreas privadas com diferentes níveis de acesso a dados fictícios de pessoas e saúde, com foco no **IMC (Índice de Massa Corporal)**.

---

## 📌 Funcionalidades

- ✅ Página pública com explicação do IMC e tabela interativa
- 🔐 Área privada Nível 1: acesso com palavra-passe `acesso1`, com dados adicionais (email, telefone) e gráfico interativo
- 🔐 Área privada Nível 2: acesso com palavra-passe `acesso2`, com mapa interativo baseado em localização e IMC
- 🔑 Acesso individual por NIF, com visualização gráfica personalizada
- 📊 Tabelas interativas com ordenação, busca e paginação (via DataTables)
- 🌍 Mapa com **Folium** e clusters baseados em classificação do IMC
- 📈 Gráficos dinâmicos com **Plotly**
- 📁 Dados carregados automaticamente a partir de um Google Sheet:  
  [🔗 Ver GoogleSheet](https://docs.google.com/spreadsheets/d/1QPioUWqLQ0v5HZ4An0exK52sNCOSIyiDsxpMgM0cKxA/edit#gid=940413956)

---

## ⚙️ Tecnologias Utilizadas

- Python 3
- Flask
- pandas
- Plotly
- Folium
- gspread + OAuth2 (Google Sheets API)
- DataTables (JS)
- HTML + CSS
- Deploy: [Render.com](https://mads-grupo-4-visualiza-o-dados-render-imc.onrender.com)

---

## 🧮 O que é o IMC?

> **IMC = Peso (kg) / Altura² (m²)**

| IMC           | Classificação       |
|---------------|---------------------|
| Menor que 18.5| Abaixo do peso 💀     |
| 18.5 - 24.9   | Peso normal ✅        |
| 25 - 29.9     | Sobrepeso ⚠️         |
| 30 ou mais    | Obesidade 🚨         |

---

## 📁 Estrutura do Projeto

```
flask-dados-imc/
│
├── app.py                  # Aplicação principal Flask
├── static/
│   └── obesidade.ico       # Ícone para IMC alto
└── README.md               # Este documento
```

---

## 🔐 Palavras-passe de Acesso (teste)

- Nível 1: `acesso1`
- Nível 2: `acesso2`
- NIF individual: digite um NIF presente no Google Sheet

---

## 📦 requirements.txt (Corrigido)

```txt
Flask
pandas
gspread
oauth2client
plotly
folium
os
datetime
```

---


---

## 🛡️ Aviso Legal

> Este projeto utiliza **dados fictícios** apenas para fins educacionais. Nenhuma informação real de pessoas foi usada.
