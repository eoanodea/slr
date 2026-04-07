# Systematic Literature Review: Energy Efficiency in Microservice Architectures

**Last Updated**: October 2025

A systematic literature review investigating how energy efficiency is addressed in microservice-based systems, including measurement approaches, architectural solutions, and trade-offs.

## 📁 Repository Structure

```
├── 0-pilot/                      # Pilot study and preliminary exploration
├── 1-paper-extraction/           # Search queries and paper collection
│   ├── search-string.md         # Database-specific search strings
│   ├── combine.ipynb            # Script to combine extraction results
│   ├── iteration-5/             # Earlier extraction iteration
│   └── iteration-6/             # Latest extraction iteration
├── 2-screenings/                 # Multi-stage screening process
│   ├── 1-pilot-screening/       # Initial pilot screening
│   ├── 2-preliminary-screening/ # Preliminary relevance screening
│   ├── 3-primary-screening/     # Primary screening with inclusion criteria
│   ├── 4-seconday-screening/    # Secondary screening and validation
│   └── automate-ic.py          # Automation script for inclusion criteria
├── 3-snowball/                   # Snowballing for additional papers
├── helpers/                      # Utility scripts and tools
├── research-questions.md         # Detailed research questions and parameters
└── digest.txt                    # Compressed repository context (for AI assistance)
```

## 📌 Spreadsheet

A Google Sheet was used to track papers through the screening process, with columns for metadata, screening decisions, and notes. You can accesss it under the file `SLR Tracker.xlsx` in the repository.

## 📋 Research Questions

This review addresses three main research questions with multiple sub-questions covering the software lifecycle, measurement approaches, architectural solutions, and trade-offs.

→ See [`research-questions.md`](research-questions.md) for complete details.

## 🔍 Search Strategy

Database searches conducted on Scopus, IEEE Xplore, and ACM Digital Library (2015-2025).

→ See [`1-paper-extraction/search-string.md`](1-paper-extraction/search-string.md) for search queries.

## 📊 Key Notebooks

- [`1-paper-extraction/combine.ipynb`](1-paper-extraction/combine.ipynb) - Combine papers from different databases
- [`2-screenings/2-preliminary-screening/combine-datasets.ipynb`](2-screenings/2-preliminary-screening/combine-datasets.ipynb) - Merge screening rounds
- Screening automation scripts in `2-screenings/` directories

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Jupyter Notebook/Lab
- ASReview (for screening)
- OpenAI API key (for automated screening, optional)

### Setup

```bash
# Clone the repository
git clone git@github.com:eoanodea/slr.git
cd slr

# Create .env file with your API keys (if using automation)
cp .env.example .env
# Edit .env with your credentials

# Install dependencies (if requirements.txt exists)
pip install -r requirements.txt
```
