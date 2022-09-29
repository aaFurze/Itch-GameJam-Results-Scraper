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
    '''
    Parameters: A pandas (DataFrame) object and a filename (str).
    Creates a .csv containing the submission_data and with a filename "filename_TIME-DATE.csv"
    TIME format: Hour, Minute, Second. DATE format: Year Month Day
    Returns True if a .csv file created.
    '''
    timestamp = datetime.datetime.now().strftime("%H%M%S-%Y%m%d")
    submission_data.to_csv(f"data\\{filename}_{timestamp}.csv", index=False)
    return True


def _get_rating_categories(page: BeautifulSoup) -> List[str]:
    '''
    Parameter: A BeautifulSoup object containing a page's html
    Searches the first <table> it finds on the page, and retrieves the row names it finds.
    Returns: A list containing three common column names (game_title, author, number_of_ratings) and the row names found.
    If an "Overall" row name is found, that will be the 4th item in the list returned.
    '''
    table = page.find("table")
    table_rows = table.find_all("tr")

    basic_data_columns = ["game_title", "author", "number_of_ratings"]

    rating_columns = []

    for i, row in enumerate(table_rows):
        if i == 0: continue
        first_item = row.find("td")
        rating_columns.append(first_item.text)
    
    if "Overall" not in rating_columns:
        return basic_data_columns + rating_columns
    
    overall_index = rating_columns.index("Overall")
    if overall_index != 0 and overall_index != -1:
        new_output = [rating_columns[overall_index]]
        for value in rating_columns:
            if value == "Overall":
                continue
            new_output.append(value)
        
        new_output = basic_data_columns + new_output
        return new_output

    
    return basic_data_columns + rating_columns



def _create_df(category_groups: List[str]):
    '''
    Parameters: Input a list of category groups that act as the basis for column headers.
    Converts the column headers into lowercase strings with "_", "-" and "/" characters where appropriate.
    Creates three columns for each custom category_group (category_group that is not "game_title", "author" or "number_of_ratings")
    These are: "column_name_rank", "column_name_score", and "column_name_raw_score".
    '''
    column_names = category_groups[:3]
    for category in category_groups[3:]:
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
    '''
    Parameters: BeautifulSoup object containing page html and a list of the categories it expects to find in each table in page_html.
    For each submission, first retrieves basic data (game title, author and number of ratings).
    Then retrieves rank, score and raw score values for each category.
    Returns: A List of Lists containing data for each submission found on the page.

    '''
    summary_containers = page_html.find_all("div", class_="game_summary")
    game_titles = []
    authors = []
    rating_figures = []

    for container in summary_containers:
        game_titles.append(container.find("h2").text)

        h3_tags = container.find_all("h3")
        authors.append(h3_tags[0].text[3:])
        rating_text_block = h3_tags[1].text
        rating_figures.append(rating_text_block[rating_text_block.find("with") + 4 : rating_text_block.find("ratings") - 1])


    tables = page_html.find_all("table")
    output = []

    for i, table in enumerate(tables):
        data = [game_titles[i], authors[i], rating_figures[i]]
        data += _table_to_values(table, categories[3:])
        output.append(data)

    return output


def _table_to_values(table_html: BeautifulSoup, categories: List[str]) -> List[str]:
    '''
    Parameters: A BeautifulSoup object containing a submission table's html and the categories expected to be in the table.
    Finds the rows in the table, and cleans them. Then takes these cleaned results and puts them into a single list
    If a particular submission is not rated in a particular category, "n/a" will be inputted instead.#
    Returns: A list of strings representing the submission ranks/scores in particular categories.
    '''
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
    '''
    Parameter: A list of BeautifulSoup objects containing rows in a submission table.
    Removes all html tags and non-text values.
    Returns: A list(1) of list(2)s containing a category e.g. "GamePlay" and rank, score, and raw score values.
    Note: First list(2) in each list(1) will be a headings row (Usually "['Criteria', 'Rank', 'Score', 'Raw Score']")
    '''
    output = []
    for row in rows:
        row_values = row.find_all("td")
        output_row = []
        for column in row_values:
            output_row.append(column.text)
        output.append(output_row)
    print(output)
    return output

