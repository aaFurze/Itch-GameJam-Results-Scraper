from src.scraper import get_jam_submissions_html
from src.dataframe import create_submissions_data_csv, create_submission_scores_df
import asyncio


if __name__ == "__main__":
    results = asyncio.run(get_jam_submissions_html("https://itch.io/jam/kenney-jam-2022/results"))
    data = create_submission_scores_df(results)
    create_submissions_data_csv(data, "Kenney-Jam-2022")
