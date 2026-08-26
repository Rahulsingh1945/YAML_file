# Book Scraper & Dataset Automation

## Project Overview
my only goal is to learn github action to automate scraping so that i can scrap more data without turning on my pc
## Objectives
Automate the scraping process using GitHub Actions.
## Data Source
Website: https://books.toscrape.com/
## Technologies Used
Python, Requests, BeautifulSoup, CSV, Pandas,Git & GitHub,GitHub Actions

## Dataset Description
## Dataset Description

The final dataset contains **1,000 unique books** collected from the Books to Scrape website.

Each row represents one book, and each column contains a specific attribute collected during the scraping process.

The dataset includes:

* Book name
* Category
* Price excluding tax
* Price including tax
* Tax
* Availability
* Stock count
* Rating
* UPC
* Product URL
* Image URL
* Description
* Page number
* Scraped timestamp

The dataset is stored as a CSV file:

```text
data/raw/books.csv
```

The UPC is used as the unique identifier to prevent the same book from being added multiple times during repeated scraping runs.


## Data Cleaning & Quality Checks

## Duplicate Handling
## Duplicate Handling

During development, repeated scraper runs were initially adding the same books to the CSV file. This happened because new records were appended without checking whether the book already existed.

To prevent this, the scraper now uses the **UPC (Universal Product Code)** as a unique identifier.

Before saving a book:

1. The scraper reads the existing UPC values from the dataset.
2. It checks whether the scraped book's UPC already exists.
3. If the UPC already exists, the record is skipped.
4. If the UPC is new, the book is added to the dataset.

The existing dataset was also cleaned using the UPC field as the deduplication key.

### Result

* Records before cleaning: **8,034**
* Records after cleaning: **1,000**
* Duplicate UPCs after cleaning: **0**

This ensures that repeated scraping runs do not continuously create duplicate records.


## GitHub Actions Automation

GitHub Actions is used to automate the book scraping workflow.

The workflow runs the scraper in a GitHub-hosted environment and performs the required steps without needing to run the script manually on a local computer.

### Workflow

1. Check out the repository.
2. Set up the Python environment.
3. Install the required Python packages.
4. Run the book scraper.
5. Validate the collected dataset.
6. Clean and update the dataset.
7. Commit and push updated data to the repository.

The workflow can be scheduled using a cron expression, allowing the dataset to be updated automatically at a defined interval.

During development, the workflow was temporarily disabled while the duplicate-handling logic was tested and the existing dataset was cleaned.

## Project Structure
scrap book YAML file/
│
├── .github/
│       └── scrape.yml
│
├── data/
│   └── raw/
│       └── books.csv
│
├── scripts/
│   ├── scraper.py
│   └── remove_duplicates.py
│
├── README.md
└── requirements.txt

## How to Run Locally
## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Rahulsingh1945/YAML_file.git
cd YAML_file
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the scraper

```bash
python scripts/scraper.py
```

The scraped data will be stored in:

```text
data/raw/books.csv
```

### 5. Check the dataset

You can use Python and Pandas to verify the collected records:

```python
import pandas as pd

df = pd.read_csv("data/raw/books.csv")

print("Total rows:", len(df))
print("Unique UPCs:", df["upc"].nunique())
print("Duplicate UPCs:", df["upc"].duplicated().sum())
```

A correctly maintained dataset should contain unique UPC values without duplicate records.

## Dataset Columns

| Column           | Description                                 |
| ---------------- | ------------------------------------------- |
| `book_name`      | Name of the book                            |
| `category`       | Category assigned to the book               |
| `price_excl_tax` | Book price excluding tax                    |
| `price_incl_tax` | Book price including tax                    |
| `tax`            | Tax amount                                  |
| `availability`   | Availability status of the book             |
| `stock_count`    | Number of copies available                  |
| `rating`         | Book rating                                 |
| `upc`            | Unique product identifier                   |
| `product_url`    | URL of the book's product page              |
| `image_url`      | URL of the book's cover image               |
| `description`    | Description of the book                     |
| `page_number`    | Website page where the book was found       |
| `scraped_at`     | Date and time when the record was collected |

## Example Output

Example record from the dataset:

```text
Book Name: A Light in the Attic
Category: Poetry
Price: £51.77
Availability: In stock
Stock Count: 22
Rating: 3
```

The complete dataset is available in:

```text
data/raw/books.csv
```

## Challenges & Solutions

### 1. Duplicate Records

Repeated scraper runs initially appended existing books to the CSV, creating thousands of duplicate records.

**Solution:** The scraper was updated to use the book's UPC as a unique identifier and skip books that already exist in the dataset.

### 2. Existing Duplicate Dataset

The initial dataset contained **8,034 records**, including repeated books.

**Solution:** The existing dataset was cleaned using the UPC field, resulting in **1,000 unique records** with zero duplicate UPCs.

### 3. Automated Execution

Running the scraper manually every time is inefficient.

**Solution:** GitHub Actions was configured to automate the scraping workflow.

### 4. Data Validation

Scraped data can contain missing or unexpected values.

**Solution:** Dataset checks were added to inspect record counts, unique identifiers, and duplicate records.

## Limitations

* The dataset depends on the structure and availability of the source website.
* Changes to the website's HTML structure may require changes to the scraper.
* The project currently stores the collected data in CSV format rather than a database.
* The scraper collects data available on the source website and does not verify the information independently.
* The project is designed primarily for learning and portfolio purposes rather than large-scale production scraping.

## Future Improvements

* Store the dataset in a SQL database.
* Add more comprehensive data validation.
* Add logging for scraping errors and failed requests.
* Implement retry handling for temporary network failures.
* Track changes in book prices and stock over time.
* Create a dashboard using Power BI to analyze book prices, ratings, categories, and availability.
* Add automated tests for the scraper and data-quality checks.
* Improve the GitHub Actions workflow with clearer failure notifications.

## Key Takeaways

This project provided practical experience with:

* Web scraping using Python, Requests, and BeautifulSoup.
* Extracting and structuring data from HTML pages.
* Handling duplicate records using a unique identifier.
* Performing basic dataset validation and cleaning.
* Automating a data-collection workflow with GitHub Actions.
* Using Git and GitHub for version control and project management.

The project also demonstrated the importance of testing automated data pipelines. A scraper can successfully collect data while still producing a poor-quality dataset if duplicate handling and validation are not considered.

## Author

**Rahul Singh**

Data Analyst aspirant with a background in Chemistry, currently building practical projects in Python, SQL, data analysis, web scraping, and data automation.

* GitHub: [Rahul Singh](https://github.com/Rahulsingh1945)
* LinkedIn: [Rahul Singh](https://www.linkedin.com/in/rahul-singh1945/)
