from typing import List
import pandas as pd
from bs4 import BeautifulSoup
import datetime


def create_submission_scores_df(pages: List[BeautifulSoup]) -> pd.DataFrame:
    df = _create_df()
    for page in pages:
        page_data = _jam_results_page_to_data(page)
        for submission in page_data:
            df.loc[len(df)] = submission
    return df

def create_submissions_data_csv(submission_data: pd.DataFrame, filename: str) -> bool:
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    submission_data.to_csv(f"data\\{filename}_{timestamp}")
    return True


def _create_df():
    output = pd.DataFrame(columns=["overall_rank", "overall_score", "overall_raw_score",
     "theme_rank", "theme_score", "theme_raw_score",
     "visuals_rank", "visuals_score", "visuals_raw_score",
     "concept_rank", "concept_score", "concept_raw_score"])

    return output


def _jam_results_page_to_data(page_html: BeautifulSoup) -> List[List[str]]:
    tables = page_html.find_all("table")
    output = []
    for table in tables:
        data = _table_to_values(table)
        output.append(data)
    return output


def _table_to_values(table_html: BeautifulSoup) -> List[str]:
    table_rows = table_html.find_all("tr")
    cleaned_rows = _get_cleaned_table_rows(table_rows)

    temp_dict = {"overall": None, "theme": None, "visuals": None, "concept": None}

    for row in cleaned_rows:
        if row[0].find("Overall") != -1:
            temp_dict["overall"] = row[1:]
        elif row[0].find("visuals") != -1:
            temp_dict["visuals"] = row[1:]
        elif row[0].find("Theme") != -1:
            temp_dict["theme"] = row[1:]   
        elif row[0].find("Concept") != -1:
            temp_dict["concept"] = row[1:]       
    
    return temp_dict["overall"] + temp_dict["theme"] + temp_dict["visuals"] + temp_dict["concept"]


def _get_cleaned_table_rows(rows: List[BeautifulSoup]) -> List[List[str]]:
    output = []
    for row in rows:
        row_values = row.find_all("td")
        output_row = []
        for column in row_values:
            output_row.append(column.text)
        output.append(output_row)
    return output

