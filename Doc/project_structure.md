nbs-price-tracker/
│
├── README.md                  # Overview, usage, setup
├── requirements.txt           # Python dependencies
├── .env.example               # Template for env variables (API keys, DB URI, etc.)
├── .gitignore
│
├── data/
│   ├── raw/                   # Original NBS Excel/PDF files
│   ├── interim/               # Intermediate cleaned files (pre-validated)
│   └── processed/             # Final clean CSVs ready for loading/analysis
│
├── scripts/
│   ├── __init__.py
│   ├── download_nbs_data.py   # Downloads or scrapes from NBS site
│   ├── extract_tables.py      # Extracts structured tables from Excel/PDF
│   ├── transform_data.py      # Cleans and normalizes data
│   ├── validate_data.py       # Validates schema, data types, units
│   └── upload_to_storage.py   # Pushes final data to cloud/github/etc
│
├── pipeline/
│   ├── run_pipeline.py        # Main orchestrator for ETL
│   └── config.py              # Paths, settings, constants
│
├── notebooks/                 # Jupyter notebooks for EDA, debugging
│   └── initial_analysis.ipynb
│
├── utils/
│   ├── file_utils.py          # File I/O helpers, download handlers
│   ├── schema_utils.py        # Schema definitions, validators
│   └── logging_config.py      # Logging setup
│
├── logs/
│   └── etl_2024-04-13.log     # Run logs
│
└── tests/
    └── test_transform.py      # Pytest-based unit tests for scripts
