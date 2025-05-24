# 🏛️ Acropolis Museum Review Analysis

This repository provides a complete pipeline for collecting, processing, and analyzing visitor reviews of the Acropolis Museum from TripAdvisor. It consists of three main components:

1. **Scraper** (`main.py`) – Collects raw review data from TripAdvisor.
2. **Combiner** (`combine_acropolis_reviews.py`) – Merges and preprocesses multiple review datasets.
3. **Analyzer** (`Final_Acropolis_Sentiment_Analysis.ipynb`) – Performs sentiment analysis and visualizations.

---

## 📂 Project Structure

```
.
├── main.py                         # Web scraper for TripAdvisor reviews
├── combine_acropolis_reviews.py   # Merges and analyzes review CSVs
├── Final_Acropolis_Sentiment_Analysis.ipynb  # Sentiment analysis and visualization
```

---

## ⚙️ Setup

1. **Install required Python packages:**

```bash
pip install curl-cffi beautifulsoup4 pandas matplotlib seaborn scikit-learn nltk
```

2. **(Optional)** Setup NLTK data if required by the notebook:

```python
import nltk
nltk.download('vader_lexicon')
```

---

## 🕸️ Web Scraping

To scrape TripAdvisor reviews of the Acropolis Museum, run:

```bash
python main.py
```

- Output: `tripadvisor_acropilis_museum.csv`
- Automatically paginates through all review pages (~2300+)

---

## 🧩 Combine and Analyze Reviews

To merge review datasets and get basic stats:

```bash
python combine_acropolis_reviews.py
```

- Output: `all_acropolis_reviews.csv`
- Includes source tracking and summary statistics (average rating, review length, etc.)

---

## 📊 Sentiment Analysis

Open and run the notebook:

```bash
Final_Acropolis_Sentiment_Analysis.ipynb
```

- Performs sentiment scoring
- Visualizes rating distributions and sentiment trends
- Uses NLP techniques for text preprocessing

---


## 📄 License

MIT License
