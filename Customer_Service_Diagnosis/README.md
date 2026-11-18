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

The dependencies are managed with [uv](https://docs.astral.sh/uv/): `pyproject.toml` lists the packages and `uv.lock` pins the exact versions the notebook was run with (Python 3.14). uv installs Python 3.14 if it is missing.

```bash
cd Customer_Service_Diagnosis
uv sync                            # create .venv with the locked versions
uv run jupyter lab
```

The data is not included in this repository. The notebook expects it in `portfolio-data/Customer_Service_Diagnosis/data/`, in a `portfolio-data` folder next to this repository. To use another location, change `DATA_DIR` in the notebook's setup cell.

<br>

[← Back to portfolio](../README.md)
