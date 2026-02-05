# RTFTI Protocol Terminal

**Real-Time Financial Trust Infrastructure — Full-Stack Execution Console**

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.0+-red)

## Overview

RTFTI is a protocol that transforms raw financial data from MSMEs into a standardized, verifiable **Financial Trust Score (FTS)**. It bridges the information asymmetry between small businesses, financial institutions, and regulators.

### The Problem

MSMEs struggle to access formal credit because banks cannot efficiently verify their financial health. Traditional audits are expensive, slow, and periodic.

### The Solution

RTFTI creates a continuous, automated trust pipeline that processes real-time financial data through **5 layers** to produce an objective trust score.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the terminal
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## Features

- **Full-Stack Terminal**: All 5 protocol layers visible on a single page
- **Editable Data**: Modify GL, Bank, GST, and Payroll data directly
- **Real-Time Execution**: Process data through the entire pipeline with one click
- **Dark/Light Theme**: Toggle between modes in the sidebar
- **Stakeholder Views**: See outputs tailored for MSME, Bank, and Regulator perspectives
- **Comprehensive Documentation**: Built-in docs explaining every component

## Requirements

- Python 3.8+
- Streamlit
- Pandas
- NumPy
- Plotly

See [requirements.txt](requirements.txt) for full dependencies.

## Project Structure

```
RTFTI/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── DOCUMENTATION.md   # Detailed protocol documentation
```

## License

MIT License

## Author

RTFTI Protocol v1.0
