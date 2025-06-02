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
├── app.py                  
├── README.md               
└── dados/
    └── dados_pessoais_com_imc.xlsx
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