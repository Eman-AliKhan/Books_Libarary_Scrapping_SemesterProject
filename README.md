# 📚 Book Library Web Scraping & Recommendation System

A Python-based semester project focused on collecting, cleaning, analyzing, and organizing book data across multiple genres. The project includes web scraping scripts, structured CSV datasets, exploratory data analysis, and a Streamlit-based book recommendation application.

## 📌 Project Overview

Books contain useful information about genres, authors, ratings, and prices. Collecting this information from online sources can help organize book catalogs and explore patterns in reading preferences.

This project gathers book information across four categories—autobiography, children's books, fiction, and history—and stores the collected data in CSV files for further analysis and potential use in recommendation applications.

## 🎯 Project Objectives

- Collect book information from online sources using Python web scraping.
- Organize book data into structured CSV datasets.
- Clean and prepare collected data for analysis.
- Explore book-related patterns through exploratory data analysis (EDA).
- Develop a Streamlit-based interface for book recommendations.
- Build practical experience in data collection, preprocessing, and data-driven applications.

## ✨ Key Features

### 🕸️ Web Scraping
Separate Python scripts are provided for collecting book data across different genres.

### 🗂️ Multi-Genre Datasets
The repository includes datasets for:
- Autobiography books
- Children's books
- Fiction books
- History books

### 🧹 Data Preparation
Collected information is stored in CSV format to support data inspection, organization, cleaning, and further analysis.

### 📊 Exploratory Data Analysis
The `eda.py` script supports the project's data analysis workflow. Its specific analyses and visualizations can be documented after reviewing the implementation.

### 📖 Book Recommendation Application
The repository includes a Streamlit Python script for a book recommendation interface. The recommendation logic and available user interactions depend on the implementation in the script.

## 🛠️ Technologies Used

- **Python** — Data collection and processing
- **Web Scraping** — Extracting information from online book catalogs
- **Pandas** — Tabular data processing, if used in the scripts
- **CSV** — Structured dataset storage
- **Streamlit** — Interactive application interface
- **Exploratory Data Analysis (EDA)** — Investigating the collected data

## 📁 Repository Structure

| File | Purpose |
|---|---|
| `scraping_autobio_books.py` | Scraping script for autobiography books |
| `scraping children books.py` | Scraping script for children's books |
| `scraping fiction books.py` | Scraping script for fiction books |
| `scraping history books.py` | Scraping script for history books |
| `1000_autobio_books.csv` | Autobiography book dataset |
| `1000_children_books.csv` | Children's book dataset |
| `1000_fiction_books.csv` | Fiction book dataset |
| `1000_history_books.csv` | History book dataset |
| `eda.py` | Exploratory data analysis script |
| `book_rec_streamlit_notepad.py` | Streamlit-based book recommendation application |
| `fiction_books_wrong_date.csv` | Additional fiction dataset containing date-related data that may require validation |

## 🚀 Getting Started

### Prerequisites

Install Python 3.9 or later and ensure that the libraries required by your scripts are installed.

### 1. Clone the Repository

```bash
git clone https://github.com/Eman-AliKhan/Books_Libarary_Scrapping_SemesterProject.git
cd Books_Libarary_Scrapping_SemesterProject
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

Install the packages imported by the project scripts. For example, if your code uses these libraries:

```bash
pip install pandas requests beautifulsoup4 streamlit matplotlib seaborn
```

The exact dependencies may differ depending on the implementation.

### 4. Run the Analysis

```bash
python eda.py
```

### 5. Launch the Streamlit Application

```bash
streamlit run book_rec_streamlit_notepad.py
```

Run the commands from the project directory. If a script expects a specific CSV filename or folder, ensure the required file is available at that location.

## 📈 Potential Applications

- Exploring book catalogs across multiple genres
- Comparing book ratings and prices, where available
- Preparing datasets for visualization and analytics
- Supporting the development of book discovery and recommendation tools

## 🎓 Learning Outcomes

This project provided an opportunity to work with:

- Web scraping and structured data collection
- CSV-based dataset organization
- Data preprocessing and quality checks
- Exploratory data analysis
- Python application development
- Building a foundation for recommendation systems

## 👩‍💻 Author

**Eman Ali Khan**

GitHub: [@Eman-AliKhan](https://github.com/Eman-AliKhan)

## 📌 Project Type

Academic Semester Project

---

*This repository documents a practical project in web scraping, data analysis, and book recommendation application development.*
