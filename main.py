from src.scraper import get_jam_submissions_html
from src.dataframe import create_submissions_data_csv, create_submission_scores_df
import asyncio


if __name__ == "__main__":
    base_url = input("Enter the base url of the GameJam you would like to scrape score data for. e.g. https://itch.io/jam/kenney-jam-2022/results : \n")
    max_pages = input("Enter the maximum number of results you would like to retrieve (default value = 2000): \n")
    if max_pages == "":
        max_pages = 100
    else:
        max_pages = int(int(max_pages) / 20)
    save_file_base_name = input("Enter what you want to save the file as. (Do not include .csv at the end): \n")
    print("Retrieving results from itch.io...")
    results = asyncio.run(get_jam_submissions_html(base_url=f"{base_url}", max_pages=max_pages))
    print("Creating dataframe...")
    data = create_submission_scores_df(results)
    print(f"Saving results...")
    create_submissions_data_csv(data, f"{save_file_base_name}")
    print("Execution Successful.")
