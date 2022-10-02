from src.scraper import get_jam_submissions_html
from src.dataframe import create_submissions_data_csv, create_submission_scores_df
from src.validate_input import check_webpage_exists, validate_file_name_input, validate_results_number_input
import asyncio


def run():
    base_url = input("Enter the base url of the GameJam you would like to scrape score data for. e.g. https://itch.io/jam/kenney-jam-2022/results  \n")
    if not check_webpage_exists: return

    max_pages = input("\nEnter the maximum number of results you would like to retrieve (default value = 2000): \n")
    max_pages = validate_results_number_input(max_pages)
    if not max_pages: return

    save_file_base_name = input("\nEnter what you want to save the file as. (Do not include .csv at the end): \n")
    save_file_base_name = validate_file_name_input(save_file_base_name)

    print("Retrieving results from itch.io...")
    results = asyncio.run(get_jam_submissions_html(base_url=f"{base_url}", max_pages=max_pages))
    print("Creating dataframe...")
    data = create_submission_scores_df(results)
    print(f"Saving results...")
    create_submissions_data_csv(data, f"{save_file_base_name}")
    print("Execution Successful.")


if __name__ == "__main__":
    run()

