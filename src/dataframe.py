from typing import List
import pandas as pd
from bs4 import BeautifulSoup
import datetime


def create_submission_scores_df(pages: List[BeautifulSoup]) -> pd.DataFrame:
    '''
    Parameter: List of HTML Pages (BeautifulSoup objects). 
    Returns: Pandas Dataframe containing scoring data from each page.
    '''
    rating_categories = _get_rating_categories(pages[0])
    df = _create_df(rating_categories)
    print("Populating Dataframe")
    counter = 0
    for page in pages:
        page_data = _jam_results_page_to_data(page, rating_categories)
        for submission in page_data:
            counter += 1
            print(f"Inserting submission {counter} data.")
            df.loc[len(df)] = submission
    return df

def create_submissions_data_csv(submission_data: pd.DataFrame, filename: str) -> bool:
    timestamp = datetime.datetime.now().strftime("%H%M%S-%Y%m%d")
    submission_data.to_csv(f"data\\{filename}_{timestamp}.csv", index=False)
    return True


def _get_rating_categories(page: BeautifulSoup) -> List[str]:
    table = page.find("table")
    table_rows = table.find_all("tr")

    # Add number_of_ratings column as default.
    output = []

    for i, row in enumerate(table_rows):
        if i == 0: continue
        first_item = row.find("td")
        output.append(first_item.text)
    
    if "Overall" not in output:
        return output
    
    overall_index = output.index("Overall")
    if overall_index != 0 and overall_index != -1:
        new_output = [output[overall_index]]
        for value in output:
            if value == "Overall":
                continue
            new_output.append(value)
        
        return new_output

    
    return output



def _create_df(category_groups: List[str]):
    column_names = []
    for category in category_groups:
        base_name = ""
        for char in category.lower():
            if char in [" "]:
                base_name += "_"
            if char in ["-", "/"]:
                base_name += "-"
            elif char.isalnum():
                base_name += char
            
        column_names += [f"{base_name}_rank", f"{base_name}_score", f"{base_name}_raw_score"]

    output = pd.DataFrame(columns=column_names)

    return output


def _jam_results_page_to_data(page_html: BeautifulSoup, categories: List[str]) -> List[List[str]]:
    # ratings_container = page_html.find_all("some_criteria")
    # for rating in ratings_container:
    #   Do some re/parsing to get the rating value
    #   Add the value to a list of ratings.

    tables = page_html.find_all("table")
    output = []
    # Convert this to an enumerable.
    for table in tables:
        # data = [ratings_list[i]]
        # data += table_values
        data = _table_to_values(table, categories)
        output.append(data)
    return output


def _table_to_values(table_html: BeautifulSoup, categories: List[str]) -> List[str]:
    table_rows = table_html.find_all("tr")
    cleaned_rows = _get_cleaned_table_rows(table_rows)

    temp_dict = {category: None for category in categories}
    keys = temp_dict.keys()

    for row in cleaned_rows:
        for key in keys:
            if row[0].find(key) != -1:
                temp_dict[key] = row[1:] 
    output = []
    for key in keys:
        if temp_dict[key] is None:
            output += ["n/a", "n/a", "n/a"]
            continue
        output += temp_dict[key]
    
    return output


def _get_cleaned_table_rows(rows: List[BeautifulSoup]) -> List[List[str]]:
    output = []
    for row in rows:
        row_values = row.find_all("td")
        output_row = []
        for column in row_values:
            output_row.append(column.text)
        output.append(output_row)
    return output

