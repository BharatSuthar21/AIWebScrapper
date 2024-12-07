import json
import os
import csv
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_ollama
# Query
query = ("Generate a list of job or internship opportunities. Provide the details in a structured JSON format with the following keys: "
         "job_title, company_name, job_description, job_requirements, salary, job_type, duration, skills_required, last_date_to_apply, "
         "and other_information. Ensure the data is clear and complete for each field.")

# Load URLs from JSON File
urls_file = "./urls.json"
if not os.path.exists(urls_file):
    raise FileNotFoundError(f"{urls_file} not found. Please provide a valid JSON file.")

with open(urls_file, "r") as file:
    urls_data = json.load(file)

# Ensure URLs are properly structured as a dictionary
if not isinstance(urls_data, dict):
    raise ValueError("The URLs file must be a JSON object with integer keys and URL values.")

# CSV File to Save Results
csv_file = "relevant_information.csv"

# Initialize CSV file with headers if it doesn't exist
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Query", "Extracted Information"])

# Process Each URL
all_results = []
for key, url in urls_data.items():
    print(f"Processing URL: {url}")

    try:
        # Step 1: Scrape Website
        result = scrape_website(url)
        body_content = extract_body_content(result)
        cleaned_content = clean_body_content(body_content)

        # Step 2: Parse Content Using Query
        dom_chunks = split_dom_content(cleaned_content)
        parsed_result = parse_with_ollama(dom_chunks, query)

        # Skip if no relevant information found
        if not parsed_result.strip():
            print(f"No relevant information found for {url}")
            continue

        # Check if the entry is already in the CSV
        entry_exists = False
        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == url and row[1] == query:
                    entry_exists = True
                    break

        # Step 3: Save to CSV if Not Present
        if not entry_exists:
            with open(csv_file, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([url, query, parsed_result])

        # Store the result for in-memory use
        all_results.append({"url": url, "query": query, "result": parsed_result})
        print(f"Data extracted and saved for URL: {url}")

    except Exception as e:
        print(f"Error processing {url}: {e}")
        continue

# Summary
print(f"Processed {len(all_results)} URLs. Data saved to {csv_file}.")
