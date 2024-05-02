# EVA

![logo](./docs/logo.jpg)

EVA - Emergency Virtual Assistant is an AI-driven application designed to assist in the triage process at healthcare facilities by utilizing Google Gemini and the Manchester Triage System. This application leverages cutting-edge AI technology to help medical professionals classify patients quickly and accurately based on urgency.

## Introduction video

[Introduction video](https://www.youtube.com/watch?v=kICv8-PmgeI)

## Demo video

[Demo video](https://www.youtube.com/watch?v=5c1Xed7ql_k)

## Features

- **AI-Powered Triage**: Leverages Google Gemini for robust natural language processing.
- **Manchester Triage System**: Implements this standardized system to assess patient urgency.
- **Intuitive User Interface**: Easy-to-use interface designed for healthcare professionals.
- **Real-Time Data Processing**: Provides immediate triage classifications with ongoing data input.
- **Secure Data Handling**: Adheres to stringent data security and healthcare compliance standards.

## Live preview

- https://triage-agent-server.107.173.7.184.sslip.io/

## Installation

**Prerequisites**

- Docker
- Docker Compose

**Setup with Docker**

Configure the environment:
Create a .env file in the ./server directory and populate it with necessary environment variables following .env.example file

```bash
docker compose up
```

## Usage

Once the Docker containers are running, EVA is accessible through a web browser. Navigate to http://localhost:8501 to start using the application.

## Operating the Application

Enter the patient information into the provided form on the web interface.
The AI analyzes the input using the Manchester Triage System and returns the urgency level.
Healthcare staff can then prioritize patient care based on the AI recommendations.
Contributing
Contributions are what make the open-source community such a powerful place to learn, inspire, and create. Any contributions you make are greatly appreciated.

## To contribute:

Fork the project.
Create your feature branch (git checkout -b feature/AmazingFeature).
Commit your changes (git commit -m 'Add some AmazingFeature').
Push to the branch (git push origin feature/AmazingFeature).
Open a pull request.

## TO START DEVELOPMENT

requirements:

- poetry v 1.7.1

```bash
cp .env.example .env
```

fill in all env, then

```bash
poetry install
poetry run prisma generate
poetry run start
```

head to localhost:8501

## PROJECT STRUCTURE

```bash
.
├── compose.yml
├── Dataset
│   ├── data.csv
│   ├── triage.csv
│   ├── triage_feature_preprocessed_engineered.csv
│   └── triagena.csv
├── docs
│   └── logo.jpg
├── ML
│   ├── models
│   │   ├── knn_model.pkl
│   │   ├── lgbm_model.pkl
│   │   └── rf_model.pkl
│   ├── triageMLClassifier_Inference.ipynb
│   └── triageMLClassifier.ipynb
├── README.md
└── server
    ├── concept.excalidraw
    ├── Dockerfile
    ├── poetry.lock
    ├── prisma
    │   ├── migrations
    │   │   ├── 20240428153732_
    │   │   │   └── migration.sql
    │   │   ├── 20240428160529_reworked_db_schema
    │   │   │   └── migration.sql
    │   │   ├── 20240428161236_added_index
    │   │   │   └── migration.sql
    │   │   ├── 20240428175200_changed_message_table
    │   │   │   └── migration.sql
    │   │   ├── 20240428175449_changed_chat_message_table
    │   │   │   └── migration.sql
    │   │   ├── 20240428181701_dev
    │   │   │   └── migration.sql
    │   │   ├── 20240428182324_dev
    │   │   │   └── migration.sql
    │   │   ├── 20240429160358_update_chief_complaint_field
    │   │   │   └── migration.sql
    │   │   ├── 20240501160003_dev
    │   │   │   └── migration.sql
    │   │   ├── 20240501185751_delete_cascade
    │   │   │   └── migration.sql
    │   │   └── migration_lock.toml
    │   ├── partial_types.py
    │   ├── __pycache__
    │   │   └── partial_types.cpython-311.pyc
    │   └── schema.prisma
    ├── pyproject.toml
    ├── rag_documents
    │   └── Emergency_Triage.md
    ├── scripts
    │   ├── inspect_db.py
    │   ├── __pycache__
    │   │   ├── seed_vectordb.cpython-311.pyc
    │   │   ├── start.cpython-311.pyc
    │   │   └── testing.cpython-311.pyc
    │   ├── seed_vectordb.py
    │   ├── start.py
    │   └── testing.py
    └── src
        ├── apis
        │   ├── index.py
        │   ├── __pycache__
        │   │   └── index.cpython-311.pyc
        │   └── routes
        │       ├── base.py
        │       ├── messages.py
        │       ├── patients_records.py
        │       ├── __pycache__
        │       │   ├── messages.cpython-311.pyc
        │       │   ├── patients_records.cpython-311.pyc
        │       │   ├── threads.cpython-311.pyc
        │       │   └── users.cpython-311.pyc
        │       ├── threads.py
        │       └── users.py
        ├── app.py
        ├── configs
        │   ├── index.py
        │   └── __pycache__
        │       └── index.cpython-311.pyc
        ├── datasources
        │   ├── prisma.py
        │   └── __pycache__
        │       └── prisma.cpython-311.pyc
        ├── main.py
        ├── middlewares
        │   └── authentication.py
        ├── __pycache__
        │   └── main.cpython-311.pyc
        ├── saved_models
        │   ├── knn_model.pkl
        │   ├── lgbm_model.pkl
        │   └── rf_model.pkl
        ├── services
        │   ├── agents
        │   │   ├── gemini_chat_agent
        │   │   │   ├── index.py
        │   │   │   ├── nodes
        │   │   │   │   ├── extraction_agent.py
        │   │   │   │   ├── extract_missing_informations.py
        │   │   │   │   ├── gemini_model.py
        │   │   │   │   ├── post_extraction_agent.py
        │   │   │   │   ├── __pycache__
        │   │   │   │   │   ├── after_extraction_agent.cpython-311.pyc
        │   │   │   │   │   ├── extraction_agent.cpython-311.pyc
        │   │   │   │   │   ├── extract_missing_informations.cpython-311.pyc
        │   │   │   │   │   ├── gemini_chat_agent.cpython-311.pyc
        │   │   │   │   │   ├── gemini_model.cpython-311.pyc
        │   │   │   │   │   └── post_extraction_agent.cpython-311.pyc
        │   │   │   │   └── review_agent.py
        │   │   │   ├── __pycache__
        │   │   │   │   └── index.cpython-311.pyc
        │   │   │   └── states
        │   │   │       ├── index.py
        │   │   │       └── __pycache__
        │   │   │           └── index.cpython-311.pyc
        │   │   ├── mts_agent
        │   │   │   ├── conditional_entry.py
        │   │   │   ├── discriminators_agent.py
        │   │   │   ├── index.py
        │   │   │   ├── presentation_identification_agent.py
        │   │   │   ├── __pycache__
        │   │   │   │   ├── conditional_entry.cpython-311.pyc
        │   │   │   │   ├── discriminators_agent.cpython-311.pyc
        │   │   │   │   ├── index.cpython-311.pyc
        │   │   │   │   ├── presentation_identification_agent.cpython-311.pyc
        │   │   │   │   ├── queue_agent.cpython-311.pyc
        │   │   │   │   └── state.cpython-311.pyc
        │   │   │   ├── queue_agent.py
        │   │   │   └── state.py
        │   │   └── tools
        │   │       ├── __pycache__
        │   │       │   ├── save_patient_info.cpython-311.pyc
        │   │       │   ├── save_patient_info_kg.cpython-311.pyc
        │   │       │   ├── save_patient_presenting_complaint.cpython-311.pyc
        │   │       │   └── save_patient_triage_colour.cpython-311.pyc
        │   │       ├── save_patient_info_kg.py
        │   │       ├── save_patient_info.py
        │   │       ├── save_patient_presenting_complaint.py
        │   │       └── save_patient_triage_colour.py
        │   ├── concept.excalidraw
        │   ├── er_visit.py
        │   ├── extraction
        │   │   ├── index.py
        │   │   └── __pycache__
        │   │       └── index.cpython-311.pyc
        │   ├── prediction
        │   │   └── index.py
        │   ├── __pycache__
        │   │   ├── er_visit.cpython-311.pyc
        │   │   ├── rag.cpython-311.pyc
        │   │   └── testing.cpython-311.pyc
        │   ├── README.md
        │   └── testing.py
        └── utils
            ├── discriminators_knowledge_retrieval.py
            ├── extracted_data_preprocessing.py
            ├── knowledge_graph.py
            ├── presentational_knowledge_retrieval.py
            ├── __pycache__
            │   ├── discriminators_knowledge_retrieval.cpython-311.pyc
            │   ├── knowledge_graph.cpython-311.pyc
            │   ├── mts_knowledge_retrieval.cpython-311.pyc
            │   └── presentational_knowledge_retrieval.cpython-311.pyc
            └── triage_ml_inference.py
```

## License

Distributed under the MIT License. See LICENSE for more information.
