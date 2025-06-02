# 🌐 Sistema de Visualização de Dados com Flask - IMC

Este é um projeto web em Python/Flask que apresenta uma página pública e áreas privadas com diferentes níveis de acesso a dados pessoais e de saúde fictícios, com foco no **IMC (Índice de Massa Corporal)**.

## 📌 Funcionalidades

- ✅ Página pública com dados básicos e explicação do IMC
- 🔐 Área privada Nível 1: acesso com palavra-passe (`acesso1`) com mais detalhes, incluindo email e telefone
- 🔐 Área privada Nível 2: acesso com palavra-passe (`acesso2`) e dados completos, exceto morada
- 🔑 Acesso individual por NIF
- 📊 Tabelas dinâmicas com ordenação, busca e paginação via DataTables
- 📁 Dados carregados de um ficheiro Excel (`dados_pessoais_com_imc.xlsx`)

---

## ⚙️ Tecnologias

- Python 3
- Flask
- pandas
- HTML + CSS + JS (DataTables)
- Deploy: [Render.com](https://render.com)

---

## 🧮 Explicação sobre o IMC

O **Índice de Massa Corporal (IMC)** é uma fórmula usada para verificar se uma pessoa está com o peso ideal:

```
IMC = Peso (kg) / Altura² (m²)
```

| IMC           | Classificação       |
|---------------|---------------------|
| Menor que 18.5| Abaixo do peso      |
| 18.5 - 24.9   | Peso normal ✅       |
| 25 - 29.9     | Sobrepeso ⚠️        |
| 30 ou mais    | Obesidade 🚨        |

---

## 📁 Estrutura do Projeto

```
flask-dados-imc/
│
├── app.py                  # Código principal da aplicação Flask
├── README.md               # Este arquivo
├── requirements.txt        # Dependências do projeto
├── .render.yaml            # Configuração do deploy na Render
├── .gitignore              # Arquivos/pastas ignoradas pelo Git
└── dados/
    └── dados_pessoais_com_imc.xlsx  # Base de dados em Excel
```

---

## 🚀 Como publicar na Render

### 1. Faça push para o GitHub

Crie um repositório e envie os arquivos para ele:

```bash
git init
git add .
git commit -m "Projeto Flask IMC"
git remote add origin https://github.com/seu-usuario/flask-dados-imc.git
git push -u origin main
```

### 2. Crie o serviço na Render

1. Acesse [render.com](https://render.com)
2. Clique em **New > Web Service**
3. Conecte ao seu repositório GitHub
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Environment:** Python 3
   - **Public URL:** Será fornecida pela Render

### 3. Adicione a pasta `dados/` com o arquivo `dados_pessoais_com_imc.xlsx` via GitHub ou use armazenamento externo (S3, etc.)

---

## 🌐 Acessar aplicação online

Após o deploy, sua aplicação estará disponível em algo como:

```
https://flask-imc-nome-do-servico.onrender.com
```

---

## 🔐 Palavras-passe de acesso (teste)

- Nível 1: `acesso1`
- Nível 2: `acesso2`
- NIF individual: Digite um NIF existente na base de dados

---

## 📦 requirements.txt

```txt
Flask
pandas
openpyxl
```

---

## 🛡️ Aviso

> **Este projeto utiliza dados fictícios para fins educativos. Nenhum dado real é utilizado.**

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações (adicione se quiser).
