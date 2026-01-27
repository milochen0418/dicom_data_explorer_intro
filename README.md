# DICOM data explorer - intro

## App Overview

This app helps you explore public DICOM datasets, inspect series metadata, and download image files to your local machine.

### Landing Page
The welcome screen introduces the workflow and guides you to the search pages.

![Landing Page](docs/images/landing-page.png)

### IDC Search
Search IDC collections by filters, browse results, and add series to the download cart.

![IDC Search](docs/images/idc-search.png)

### Series Metadata
Inspect detailed series metadata before downloading.

![Series Metadata](docs/images/series-metadata.png)

### Download Flow
Review your cart and start downloads with progress feedback.

![Start Downloading](docs/images/start-downloading.png)

## Getting Started

This project is managed with [Poetry](https://python-poetry.org/).

### Prerequisites

- Python 3.11.x
- Poetry

### Installation

1. Ensure Poetry uses Python 3.11:

```bash
poetry env use python3.11
poetry env info
```

2. Install dependencies:

```bash
poetry install
```

### Running the App

Start the development server:

```bash
poetry run ./reflex_rerun.sh
```

The application will be available at `http://localhost:3000`.
