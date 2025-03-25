Claro, Fabio! Aqui está um **modelo de README.md** pronto para usar no seu repositório GitHub, explicando tudo direitinho: objetivos do projeto, estrutura, instruções de uso dos scripts Python, observações sobre caminhos de arquivos e dicas para adaptar ao Power BI.

---

### ✅ README.md — PESTEL Visual Analysis (Canada – Manufacturing Sector)

```markdown
# 📊 PESTEL Visual Analysis – Canadian Manufacturing Sector

This repository contains all code, datasets, and visualizations used in a PESTEL-driven economic analysis focused on the Canadian manufacturing sector and its supply chain. The visualizations are based on public data from Statistics Canada and the Bank of Canada.

---

## 🔎 Project Context

The goal of this project is to analyze how external macro-environmental factors (Political, Economic, Social, Technological, Environmental, Legal) influence the Canadian manufacturing sector. Using real datasets, we generate visual insights that support a PESTEL-based strategic analysis.

---

## 📁 Repository Structure

```
├── Grafico1.py             # RMPI – Price trends of key raw materials
├── Grafico2.py             # RMPI – Most volatile materials
├── Grafico3.py             # Inflation vs GDP
├── Grafico4.py             # IPPI – Industrial product volatility
├── Grafico5.py             # GDP – Top 5 industry sectors
├── Grafico6.py             # Fossil vs Non-Fossil material prices
├── Grafico7.py             # GDP – Macro sectors (goods/services)
├── Grafico8.py             # Inflation metrics over time (CPI measures)
├── Grafico10.py            # Inflation during 2008 and 2020 crises
├── datasets/               # Folder with all CSV datasets used
└── README.md               # Project documentation
```

---

## 📂 Datasets

All datasets are from **official government sources**:

- 🟦 Statistics Canada
- 🟥 Bank of Canada

They are already included in the `/datasets` folder for reproducibility.

---

## ⚠️ Important Notes

### 1. 🛠️ Update File Paths

If you're running the scripts locally, you **must update the paths** to the datasets at the top of each Python script.

Example:
```python
# Change this:
df = pd.read_csv(r"C:\Users\YourName\Desktop\meusdatasets\CPI_MONTHLY.csv")

# To something like this:
df = pd.read_csv(r"./datasets/CPI_MONTHLY.csv")
```

Alternatively, keep the dataset files in the same directory as the scripts.

---

### 2. 💡 Using Power BI?

These Python scripts use **Pandas**, **Seaborn**, and **Matplotlib**. If you plan to reproduce these visualizations in Power BI:

- You can import the datasets into Power BI and use **DAX** or **Python visuals**
- Some chart formatting and grouping logic (like `groupby`, `mean`, and filtering by date) will need to be **rewritten using Power BI's tools**
- Time series visuals will work best if you ensure the date columns are properly parsed as `date/time` or `quarter`

---

## 🧠 Suggested Use

- Strategic presentations (e.g., consulting, case studies)
- Academic work involving supply chain, macroeconomics, or PESTEL analysis
- Data visualization training with real government data

---

## 👨‍💻 Authors

- Bruno Mascarenhas  
- Fabio Prumucena  
- Renato Oshiro

Special thanks to Professor Omid Isfahanialamdari – University of Niagara Falls.

---

## 📜 License

This project is for academic and educational purposes only. Feel free to fork and adapt with attribution.
```

---

Se quiser, posso te gerar esse README como `.md`, `.txt`, `.docx`, ou até já com os gráficos embutidos no Word. Me avisa como prefere!
