# :raising_hand: Customer Service Diagnosis

Data science challenge: find out why customers are dissatisfied with a ticket-based support service, and what to change.

**Solution:** [notebook](Customer_Service_Diagnosis.ipynb)

<br>

## :question: Context

A company that develops software for other businesses provides customer support through a ticket system.

The goal of the system is to meet the customer's need: customers expect their request to be solved in the first ticket, within the time they need.

Tickets have one of three priorities: Critical, Urgent and Normal. Customers expect a ticket to be completed within **3 days if critical, 7 days if urgent and 21 days if normal**.

## :exclamation: Problem

The company has identified widespread dissatisfaction among its customers with this service.

**Your task is to analyze the ticket system's data and find relevant insights about customer satisfaction, so that the company can act to improve it.**

## :computer: Resources

The company's relational database (SQL Server) has the tables below. The data is not included in this repository.

- **Chamado:** tickets
- **Chamado_Interacao:** messages and events on each ticket
- **Tarefa:** tasks created to solve each ticket
- **Prioridade:** ticket priorities
- **Chamado_Tipo:** ticket types
- **Sistema:** systems (software products)

## :rocket: Deliverables

A Jupyter notebook showing the full development of the solution.

## :gear: Running the notebook

```bash
cd Customer_Service_Diagnosis
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

The data is not included in this repository. To run the notebook, point `DATA_DIR` in its setup cell to your copy of the data.

<br>

[← Back to portfolio](../README.md)
