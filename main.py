from api import get_campaigns
from db import fetchall, insert


if __name__ == "__main__":
    campaigns = get_campaigns()
    if campaigns:
        for campaign in campaigns:
            insert("campaigns", campaign)
        written_data = fetchall("campaigns")
        print(written_data)
    else:
        print("Не удалось получить список кампаний")
