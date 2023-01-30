def test_get_page_link():
    import sys
    # tell interpreter where to look
    sys.path.insert(0,"..")
    from DataScraping.crawler import Crawler
    food_crawler = Crawler('https://nigerianstat.gov.ng/elibrary', 'food price', 'august 2022')
    page_link = food_crawler.get_page_link()
    assert page_link == 'https://nigerianstat.gov.ng/elibrary/read/1241235'
def test_get_page_link():
    import sys
    # tell interpreter where to look
    sys.path.insert(0,"..")
    from DataScraping.crawler import Crawler
    food_crawler = Crawler('https://nigerianstat.gov.ng/elibrary', 'food price', 'august 2022')
    data_link = food_crawler.get_data_link('https://nigerianstat.gov.ng/elibrary/read/1241235')
    assert data_link == 'https://nigerianstat.gov.ng/resource/SELECTED%20FOOD%20AUGUST%202022.xlsx'
def test_process_data():
    import sys
    # tell interpreter where to look
    sys.path.insert(0,"..")
    from DataScraping.crawler import Crawler
    from DataPreprocessing.Preprocess import Data
    url = 'https://nigerianstat.gov.ng/elibrary'
    commodity = 'food price'
    month_year = 'august 2022'
    path = "DataPreprocessing/SELECTED FOOD AUGUST 2022.xlsx"
    # food_crawler = Crawler(url, commodity, month_year)
    # data_link = food_crawler.get_data_link(food_crawler.get_page_link())
    preprocess_food = Data(url, commodity, month_year, path)
    df = preprocess_food.create_final_df()
    assert df.shape[0] > 68 
    assert len(df.State.unique()) >= 36