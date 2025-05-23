# camunda-querytool

The Camunda Process Instance Query Tool is a very simple Streamlit - based application that enables users to connect to the Camunda engine, query and manage process instances and their historical data.

Why use this tool?

Camunda provides a powerful **cockpit** for managing and monitoring business processes. However, the Community Edition **cockpit** does not provide a history query feature. This tool allows users to query and manage process instances and their historical data using the Camunda engine's REST API.

References: <https://docs.camunda.org/manual/7.14/webapps/cockpit/bpmn/process-history-views/>

## Prerequisites

- Streamlit
- Python 3.9+
- Camunda engine 7.x

## Installation

Install by source code:

```bash
pip install .
```

## Usage

### Run

```bash
streamlit run camunda_querytool.py
```

### Connect to Camunda

The application will prompt you to enter the URL of your Camunda engine. The URL should be in the format `http://localhost:8080/engine-rest`.

Support basic authentication and bearer token authentication.

### Query Process Instances

Click on the "Query Process Instances" button to retrieve a list of all process instances.

### Query History Process Instances

Click on the "Query History Process Instances" button to retrieve a list of all historical process instances.
