# 🌐 Network Incident Prediction & Monitoring Dashboard

### Table of Contents
1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Objective](#objective)
4. [Background](#background)
5. [Architecture & Key Components](#architecture--key-components)
6. [Dashboard Tableau](#dashboard-tableau)
7. [Synthetic Dataset](#synthetic-dataset)
8. [Result](#result)
9. [Demo Video](#demo-video)
10. [Business Value](#business-value)
11. [How to Install & Run](#how-to-install--run)
    - [1. Set Up in Snowflake](#1-set-up-in-snowflake)
    - [2. Run the Machine Learning Notebooks](#2-run-the-machine-learning-notebooks)
    - [3. Launch the Streamlit App](#3-launch-the-streamlit-app)
    - [4. Connect Tableau](#4-connect-tableau)
12. [Google Slides Presentation](#google-slides-presentation)

---

### **Overview**
The **Network Incident Prediction & Monitoring Dashboard** is a Snowflake-based analytics and monitoring platform designed to **proactively identify and visualize network incidents** across regions and customers.  
It combines real-time network data, machine learning insights, and interactive dashboards — empowering the Network Operations Center (NOC) to respond faster and minimize customer impact.

---

### **Project Structure**
```
network-incident-monitoring/
├── assets/
│   └── img/
├── notebook/
│   ├── exploratory_data_analysis.ipynb
│   ├── generate_synthetic_dataset_1.ipynb
│   ├── generate_synthetic_dataset_2.ipynb
│   ├── generate_synthetic_dataset_3.ipynb
│   └── training_machine_learning_model.ipynb
├── semantic model/
│   └── network_outage.yaml
├── sql/
│   ├── processing.sql
│   └── setup.sql
├── streamlit/
│   ├── app/
│   │   └── network.py
│   ├── assets/
│   │   ├── scripts.js
│   │   └── styles.css
│   ├── custom_pages/
│   │   └── dash.py
│   ├── data/
│   │   ├── feature_importance.csv
│   │   └── outage_distribution.csv
│   ├── environment.yml
│   ├── requirements.txt
│   └── utils/
│       ├── data_prep.py
│       └── dash_sup.py
├── synthetic dataset/
│   ├── DIM_CITY.csv
│   ├── DIM_CLUSTER.csv
│   ├── DIM_OLT.csv
│   ├── FACT_CUSTOMER_FEEDBACK.parquet
│   ├── FACT_INCIDENT_TREND_SUMMARY.parquet
│   ├── FACT_NETWORK_CONTEXT_STATIC.parquet
│   └── FACT_TICKET_SUMMARY.parquet
└── README.md    
```

---

### **Objective**
To build an **integrated monitoring and prediction system** that enables the Network Provider’s NOC team to:
- Monitor network health and incidents in real time  
- Predict potential outages using machine learning  
- Instantly visualize which **regions or customers** are affected  

---

### **Background**
Currently, Network Provider receives network incident data from various devices through **SNMP traps**, which flow into the ticketing system.  
However, this data is often **fragmented and difficult to interpret**, making it hard to understand:
- The **overall scale** of disruptions  
- Which **customers or regions** are most affected  

This project addresses that gap by unifying data sources into Snowflake, enriching them with ML predictions, and presenting clear insights through visual dashboards.

---

### **Architecture & Key Components**

![Detail Architecture](https://raw.githubusercontent.com/nasutionijah07-arch/network-incident-monitoring/refs/heads/main/assets/img/architecture-2.png)

![Architecture](https://raw.githubusercontent.com/nasutionijah07-arch/Network-Incident-Monitoring/refs/heads/main/assets/img/architecture.png)

| Component | Description |
|------------|--------------|
| **Snowpark Python** (notebook) | Used for machine learning model training and data enrichment (e.g., mapping device IDs → location → customer). |
| **Snowflake Database** | Central data repository for storing, managing, and accessing all network and incident data. |
| **Streamlit** | Interactive web app for running predictions and visualizing real-time insights. |
| **Tableau Dashboard** | Displays heatmaps of impacted regions, severity levels, and incident trends over time. |
| **Cortex Analyst** | Enables data exploration and insight generation directly within Snowflake. |
| **Cortex Search** | Allows users to search through NOC operator transcripts and understand ongoing network conditions. |
| **Agents** | Handle process orchestration and workflow automation. |
| **Custom Tools** | Automate notifications (e.g., send summary emails about incidents or Snowflake Intelligence chats). |
| **Snowflake Intelligence (Chatbot)** | A natural language assistant that lets users query network insights in plain English, powered by Cortex Analyst and Search. |

---

### **Dashboard Tableau** 
[📦 Google Drive Link](https://drive.google.com/drive/folders/1QWD-cRVoxHhzX5J3y2JZZEj6w1s14Q5P?usp=sharing)

---

### **Synthetic Dataset**

Due to large file sizes, the **full synthetic dataset** is hosted externally.
You can access and download all sample datasets from the following link:

[📦 Full Synthetic Dataset (Google Drive)](https://drive.google.com/drive/folders/1SlA7YD3CI4N7q5coH8RrzcuVuc2CXAxF?usp=sharing)

---

### **Result**

![Streamlit Output](https://raw.githubusercontent.com/nasutionijah07-arch/network-incident-monitoring/refs/heads/main/assets/img/streamlit-screenshot-1.png)

![Streamlit Output 2](https://raw.githubusercontent.com/nasutionijah07-arch/network-incident-monitoring/refs/heads/main/assets/img/streamlit-screenshot-2.png)

![Confusion Matrix](https://raw.githubusercontent.com/nasutionijah07-arch/network-incident-monitoring/refs/heads/main/assets/img/confusion-matrix.png)

![Snowflake Intelligence](https://raw.githubusercontent.com/nasutionijah07-arch/network-incident-monitoring/refs/heads/main/assets/img/snowflake_intelligence_screenshot.png)

![Snowflake Intelligence Root Cause](https://raw.githubusercontent.com/nasutionijah07-arch/network-incident-monitoring/refs/heads/main/assets/img/root-cause.png)

![Dashboard Tableau 1](https://raw.githubusercontent.com/nasutionijah07-arch/network-incident-monitoring/refs/heads/main/assets/img/tableau-ont-summary.png)

![Dashboard Tableau 2](https://raw.githubusercontent.com/nasutionijah07-arch/network-incident-monitoring/refs/heads/main/assets/img/tableau-ont%20-detail.png)

![Dashboard Tableau 3](https://raw.githubusercontent.com/nasutionijah07-arch/network-incident-monitoring/refs/heads/main/assets/img/tableau-trouble-ticket-summary.png)

![Dashboard Tableau 4](https://raw.githubusercontent.com/nasutionijah07-arch/network-incident-monitoring/refs/heads/main/assets/img/tableau-trouble-ticket-detail.png)

---

### **Demo Video**

📺 You can watch a demonstration of the network monitoring system in action here:  
[Google Drive Link](https://drive.google.com/drive/folders/1rZ56El_KqoH1JA9JlH7wK3MneIgAgmNi?usp=sharing)

Also, the chatbot (Snowflake Intelligence) outputs chat transcripts as PDFs, which can be found here:  
[📦 Google Drive Link](https://drive.google.com/drive/folders/1rZ56El_KqoH1JA9JlH7wK3MneIgAgmNi?usp=sharing)


---

### **Business Value**
✅ **Real-Time Situational Awareness** — The NOC team can instantly view affected areas without waiting for manual updates.  
✅ **Faster Incident Response** — Early detection and prediction reduce downtime and customer impact.  
✅ **Data-Driven Operations** — Unified insights for operational decisions and performance tracking.  
✅ **Scalable Architecture** — Built on Snowflake for seamless integration and performance across large datasets.

---

### **How to Install & Run**

#### **1. Set Up in Snowflake**
1. Create or use an existing **Snowflake account**.  
2. Load the provided synthetic datasets (`.csv` and `.parquet` files) into Snowflake tables.  
3. Deploy the **semantic model (`network_outage.yaml`)** to define relationships between datasets.  
4. Enable **Snowflake Notebook**, **Cortex features (Cortex Analyst, Cortex Search)**, **Custom Tools**, **Agent**, and **Snowflake Intelligence** in your Snowflake account.

#### **2. Run the Machine Learning Notebooks**
- Open the `notebook/` folder.  
- Run `exploratory_data_analysis.ipynb` to explore the data.  
- Run `training_machine_learning_model.ipynb` to train and test the incident prediction model.

#### **3. Launch the Streamlit App**
```bash
cd streamlit
conda env create -f environment.yml
conda activate network-monitoring
streamlit run streamlit_app.py
```

The app will open in your browser, allowing you to:
- Input or simulate new data
- Run predictions
- View the latest network performance insights

#### **4. Connect Tableau**
- Use Tableau to connect to your Snowflake data source.

---

### **Google Slides Presentation**

[🌟 Google Slides Link](https://docs.google.com/presentation/d/1PwGnDE_B6p2iuZH9-QKsOZ4Ncfq5A1rl/edit?usp=sharing&ouid=111178249732581842636&rtpof=true&sd=true)

