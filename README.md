# 🌐 Network Incident Prediction & Monitoring Dashboard

### **Overview**
The **Network Incident Prediction & Monitoring Dashboard** is a Snowflake-based analytics and monitoring platform designed to **proactively identify and visualize network incidents** across regions and customers.  
It combines real-time network data, machine learning insights, and interactive dashboards — empowering the Network Operations Center (NOC) to respond faster and minimize customer impact.

---

### **Objective**
To build an **integrated monitoring and prediction system** that enables iForte’s NOC team to:
- Monitor network health and incidents in real time  
- Predict potential outages using machine learning  
- Instantly visualize which **regions or customers** are affected  

---

### **Background**
Currently, iForte receives network incident data from various devices through **SNMP traps**, which flow into the ticketing system.  
However, this data is often **fragmented and difficult to interpret**, making it hard to understand:
- The **overall scale** of disruptions  
- Which **customers or regions** are most affected  

This project addresses that gap by unifying data sources into Snowflake, enriching them with ML predictions, and presenting clear insights through visual dashboards.

---

### **Architecture & Key Components**

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

### **Demo Video**

📺 You can watch a demonstration of the network monitoring system in action here:  
[Google Drive Link](https://drive.google.com/drive/folders/1rZ56El_KqoH1JA9JlH7wK3MneIgAgmNi?usp=sharing)


---

### **Business Value**
✅ **Real-Time Situational Awareness** — The NOC team can instantly view affected areas without waiting for manual updates.  
✅ **Faster Incident Response** — Early detection and prediction reduce downtime and customer impact.  
✅ **Data-Driven Operations** — Unified insights for operational decisions and performance tracking.  
✅ **Scalable Architecture** — Built on Snowflake for seamless integration and performance across large datasets.

---

### **Project Structure**
```
network-incident-monitoring/
├── README.md
├── notebook/
│   ├── exploratory_data_analysis.ipynb
│   └── training_machine_learning_model.ipynb
├── semantic model/
│   └── network_outage.yaml
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
└── synthetic dataset/
    ├── DIM_CITY.csv
    ├── DIM_CLUSTER.csv
    ├── DIM_OLT.csv
    ├── FACT_CUSTOMER_FEEDBACK.parquet
    ├── FACT_INCIDENT_TREND_SUMMARY.parquet
    ├── FACT_NETWORK_CONTEXT_STATIC.parquet
    └── FACT_TICKET_SUMMARY.parquet
```

---

### **Synthetic Dataset**

Due to large file sizes, the **full synthetic dataset** is hosted externally.
You can access and download all sample datasets from the following link:

[📦 Full Synthetic Dataset (Google Drive)](https://drive.google.com/drive/folders/1SlA7YD3CI4N7q5coH8RrzcuVuc2CXAxF?usp=sharing)

---

### **How to Install & Run**

#### **1. Set Up in Snowflake**
1. Create or use an existing **Snowflake account**.  
2. Load the provided synthetic datasets (`.csv` and `.parquet` files) into Snowflake tables.  
3. Deploy the **semantic model (`network_outage.yaml`)** to define relationships between datasets.  
4. Enable **Snowpark Python** and **Cortex features** in your Snowflake account.

#### **2. Run the Machine Learning Notebooks**
- Open the `notebook/` folder.
- Run `exploratory_data_analysis.ipynb` to explore data.
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
- Import the provided **semantic model** to build or extend dashboards.

---

### **Example Insights**
- Heatmap of impacted regions by severity level  
- Top 5 devices causing recurring outages  
- Predicted outage probability by region  
- Real-time ticket volume and resolution trend  

---

### **Next Steps**
- Integrate live SNMP trap streams directly into Snowflake.  
- Deploy the model as a real-time inference service.  
