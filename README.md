# **Governance and Universal Health Coverage in Southeast Asia**

An exploratory secondary-data analysis of the relationship between public-sector corruption control and essential health-service coverage in Indonesia and four Southeast Asian comparator countries.

## **Research Question**

**How is public-sector control of corruption associated with essential health-service coverage in Indonesia and selected Southeast Asian countries?**

## **Background**

Healthcare integrity depends on more than fraud detection alone. Public-sector governance, accountability, and resource management may influence how effectively health systems convert public resources into accessible services.

This project examines whether countries with stronger perceived control of corruption also demonstrate higher universal health coverage service levels. It examines an exploratory association between a broad governance indicator and a public-health performance indicator.


## **Study Design**

This project uses a cross-sectional secondary-data design.

### **Countries**

The analysis includes five Southeast Asian countries:

* Indonesia
* Malaysia  
* Philippines  
* Thailand
* Viet Nam

### **Study year**

The analysis uses 2023, the latest common year with complete observations for all five selected countries in the processed dataset.

### **Unit of analysis**

One country-year observation.


## **Variables**

### **Explanatory variable**

**Control of Corruption score**

* Indicator code: `GOV_WGI_CC_SC`.  
* Source: World Bank Worldwide Governance Indicators.  
* Scale: 0–100.  
* Interpretation: Higher scores indicate stronger perceived control of corruption.

The indicator reflects perceptions of the extent to which public power is exercised for private gain, including petty and grand corruption and state capture.

### **Outcome variable**

**UHC Service Coverage Index**

* Indicator code: `SH_UHC_SCI`.  
* Source: World Bank and World Health Organization Universal Health Coverage dataset.  
* Scale: 0–100.  
* Interpretation: Higher scores indicate greater coverage of essential health services.

The UHC Service Coverage Index is based on 14 tracer indicators across four broad domains:
* Reproductive, maternal, newborn, and child health.  
* Infectious diseases.  
* Noncommunicable diseases.  
* Service capacity and access.

## **Data Sources**

The original data are publicly available from:

### **World Bank Control of Corruption**
[https://api.worldbank.org/v2/en/indicator/GOV\_WGI\_CC\_SC?downloadformat=csv](https://api.worldbank.org/v2/en/indicator/GOV_WGI_CC_SC?downloadformat=csv) 

### **World Bank/WHO UHC Service Coverage Index**
[https://api.worldbank.org/v2/en/indicator/SH\_UHC\_SCI?downloadformat=csv](https://api.worldbank.org/v2/en/indicator/SH_UHC_SCI?downloadformat=csv) 

The raw ZIP archives are included in this repository. You can either download the data yourself (through the link provided) or access them in: ```data/raw/```

## **Repository Structure**
```
health-governance-uhc-research/
├── README.md
├── LICENSE
├── .gitignore
├── data
│   ├── processed
│   │   └── final_2023.csv
│   └── raw
│       ├── API_GOV_WGI_CC_SC_DS2_en_csv_v2_56931.zip
│       └── API_SH_UHC_SCI_DS2_en_csv_v2_35440.zip
├── etc
│   └── personal_documentation.png
├── outputs
│   ├── figures
│   │   ├── governance_vs_uhc_2023.png
│   │   └── uhc_by_country_2023.png
│   └── tables
│       ├── correlations_2023.csv
│       └── final_2023.csv
└── src
    ├── analysis.py
    └── requirements.txt
```

## **Results Dataset**

The processed dataset contains the following values:

| Country | Control of Corruption | UHC Service Coverage |
| ----- | ----- | ----- |
| Indonesia | 38.88 | 67 |
| Malaysia | 55.56 | 80 |
| Philippines | 36.34 | 69 |
| Thailand | 38.96 | 82 |
| Viet Nam | 41.61 | 71 |


## **Reproduction Instructions**

### **Requirements**

* Python 3.9 or later.  
* `pandas`.  
* `numpy`.  
* `matplotlib`.  
* `scipy`.

### **1. Clone the repository**

```git clone https://github.com/diviscinnova/health-governance-uhc-research.git```
```cd health-governance-uhc-research```


### **2. Create and activate a virtual environment**

```python -m venv .venv```

Activate the environment.

#### **Windows**

```.venv\Scripts\\activate```

#### **macOS/Linux**

```source .venv/bin/activate```


### **3. Install dependencies**

```pip install -r src/requirements.txt```

### **4. Download the raw data (optional)**

Download the two World Bank ZIP archives:

* `GOV_WGI_CC_SC`.  
* `SH_UHC_SCI`.

Place both ZIP files in:

``data/raw/``

Do not extract them manually. The analysis script reads the appropriate data CSV directly from each ZIP archive.


### **5. Run the analysis**

```python src/analysis.py```

The script will:
1. Read the World Bank ZIP archives.  
2. Identify the relevant non-metadata CSV files.  
3. Convert the data from wide to long format.  
4. Keep the five selected countries.  
5. Remove duplicate country-year records.  
6. Identify the latest common year.  
7. Calculate Pearson and Spearman correlations.  
8. Save the processed table.  
9. Generate the figures.

## **Generated Outputs**

After running the script, the following files are generated:

### **Tables**

``outputs/tables/final_2023.csv``

### **Figures**

* ``outputs/figures/uhc_by_country_2023.png`` 
* ``outputs/figures/governance_vs_uhc_2023.png``

## **Interpretation**

The analysis tests whether Control of Corruption is associated with UHC Service Coverage.

A positive association would indicate that countries with higher Control of Corruption scores also tend to have higher UHC Service Coverage scores in the selected sample.

However, this association should be interpreted cautiously because:

* The analysis contains only five countries.  
* The data are aggregated at the country level.  
* Control of Corruption is perception-based.  
* The governance indicator does not directly measure healthcare fraud.  
* UHC coverage is influenced by many factors beyond corruption control.  
* The cross-sectional design cannot establish causality.

Possible additional influences include:

* Health-system financing.  
* Healthcare infrastructure.  
* Workforce availability.  
* Economic development.  
* Education.  
* Social protection.  
* Government effectiveness.  
* Policy design.  
* Geographic access.

## **Ethical and Analytical Statement**

The study does not identify or accuse any specific government, institution, or individual of fraud or corruption.

Similarly, the UHC Service Coverage Index measures essential health-service coverage and does not represent overall healthcare quality or public trust.

## **Limitations**

This study has several limitations:

1. The sample includes only five countries.  
2. The analysis uses one common year.  
3. Country-level data may conceal differences among provinces, agencies, hospitals, and communities.  
4. Control of Corruption is based on perceptions and composite estimation.  
5. The UHC Service Coverage Index summarizes essential-service coverage but does not capture every aspect of health-system performance.  
6. The analysis cannot establish causality.  
7. Missing or inconsistent reporting across countries may affect comparability.

## **Suggested Citation**

If you use this repository, cite it as:

> Madhani, C. (2026). Governance and Universal Health Coverage in Southeast Asia:  An exploratory secondary-data analysis. GitHub repository.

## **License**

The source code of this computational framework is licensed under the MIT License. The curated datasets and analysis outputs are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).

The original datasets remain subject to the terms and attribution requirements of the World Bank and WHO. 
