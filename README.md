# Sansad Parliament Q&A Scraper

A Python tool to automatically scrape questions & answers from both houses of the Indian Parliament — **Lok Sabha** and **Rajya Sabha** — for any keyword, save the metadata to Excel, and download all linked PDFs.

---

## Problem Statement

Since the 1950s, both houses of Indian Parliament have been discussing and debating policy issues relevant to socio-economic and human development. This tool automates downloading the list of questions and answers (with their PDFs and links) for any provided keyword.

**Sources:**
- Lok Sabha: https://sansad.in/ls/questions/questions-and-answers
- Rajya Sabha: https://sansad.in/rs/questions/questions-and-answers

---

## How It Works

### Lok Sabha (LS)
- Fetches all sessions for Lok Sabhas 13-18 via `sansad.in/api_ls/question/qetFilteredQuestionsAns`
- Scans all questions per session and filters by keyword in the `subjects` field
- Excludes questions where the member's name also contains the keyword

### Rajya Sabha (RS)
- Fetches all session numbers from `rsdoc.nic.in/Question/Get_sessionforQuestionSearch`
- Downloads the full question list per session from `rsdoc.nic.in/Question/Search_Questions`
- Filters by keyword in `qtitle` or `qn_text`, excludes member-name matches

### Output
- **Excel file** with two sheets: `Lok Sabha` and `Rajya Sabha`
- **PDFs** downloaded into `sansad_output/pdfs/ls/` and `sansad_output/pdfs/rs/`
- **Log file** `sansad_scraper.log` for full run history

---

## Project Structure

```
sansad-scraper/
|-- sansad_scraper.py     # Main scraper (LS + RS + PDF download + Excel export)
|-- requirements.txt      # Python dependencies
|-- .gitignore
|-- README.md
```

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/S-Chakraborty163/sansad-scraper.git
cd sansad-scraper
```

### 2. Create a virtual environment 
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Usage

### Scrape both houses for a keyword
```bash
python sansad_scraper.py --keyword damodar
```

### Lok Sabha only
```bash
python sansad_scraper.py --keyword damodar --source ls
```

### Rajya Sabha only
```bash
python sansad_scraper.py --keyword damodar --source rs
```

### All Lok Sabhas 13-18 (full historical data)
```bash
python sansad_scraper.py --keyword damodar --source ls --all-loksabhas
```

### Download PDFs from an existing Excel file
```bash
python pdf_downloader.py --excel sansad_output/sansad_damodar_20260320.xlsx --source ls
```

---

## All Arguments

| Argument | Default | Description |
|---|---|---|
| `--keyword` | `damodar` | Search keyword |
| `--source` | `both` | `ls`, `rs`, or `both` |
| `--loksabha` | `18` | Specific Lok Sabha number |
| `--all-loksabhas` | False | Scrape all Lok Sabhas (13-18) |
| `--no-pdf` | False | Skip PDF downloads |
| `--out-dir` | `sansad_output` | Output directory |

---

## Output Structure

```
sansad_output/
|-- sansad_damodar_20260320_151714.xlsx
|-- pdfs/
    |-- ls/
    |   |-- LS_19122024_Q1234_Damodar_Valley_Corporation.pdf
    |   |-- ...
    |-- rs/
        |-- RS_23032020_Q3288_Desiltation_of_Damodar_river.pdf
        |-- ...
```

### Excel - Lok Sabha Sheet

| Column | Description |
|---|---|
| lok_sabha_no | Lok Sabha number (e.g. 18) |
| session_no | Session number |
| question_no | Question number |
| title | Subject of the question |
| type | STARRED / UNSTARRED |
| date | Date of question |
| ministry | Ministry concerned |
| members | Member(s) who asked |
| pdf_url | Direct PDF link |
| local_pdf_path | Local path after download |

### Excel - Rajya Sabha Sheet

| Column | Description |
|---|---|
| session_no | Session number |
| question_no | Question number |
| title | Title of the question |
| type | STARRED / UNSTARRED |
| date | Date of answer |
| ministry | Ministry concerned |
| member_name | Member who asked |
| question_text | Full question text |
| answer_text | Full answer text |
| pdf_url | Direct PDF link |
| local_pdf_path | Local path after download |

---

## API Endpoints Discovered

Found by inspecting Chrome DevTools Network tab:

| House | Purpose | Endpoint |
|---|---|---|
| LS | Questions per session | `https://sansad.in/api_ls/question/qetFilteredQuestionsAns` |
| LS | Browse Lok Sabhas | `http://eparlib.sansad.in/restv3/field/browse` |
| RS | Questions per session | `https://rsdoc.nic.in/Question/Search_Questions` |
| RS | Session list | `https://rsdoc.nic.in/Question/Get_sessionforQuestionSearch` |

---

