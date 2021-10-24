import requests
import logging

HN_API = "https://hacker-news.firebaseio.com/v0/item/"
HN_TOP = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
articles_titles = []
articles_score = {}
game_on = True
logging.basicConfig(filename="test.log", level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def get_top():
    """
    Gets the top 40 articles from Hacker News using the website's dedicated api_endpoint
    (HN_TOP) for this kind of operation.
    """
    global articles_titles
    index_sys = 0
    try:
        top_response = requests.get(HN_TOP)
        top = top_response.json()
    except ConnectionError:
        raise ConnectionError("There seems to be a problem,\ncheck your internet connection")
    else:
        top = top[:40]
        nested_list = []
        for _ in top:
            nested_list.append(f"{HN_API}{top[index_sys]}.json?print=pretty")
            index_sys += 1
        articles_titles = nested_list
        logging.debug("program managed to attain top 40 articles from HN")


def rate():
    """
    Scores each article in accordance with the HN scoring algorithm,
    and then ordering each article in descending order by their respective score.
    """
    global articles_score
    nested_dict = {}
    for article in articles_titles:
        response = requests.get(article)
        article_info = response.json()
        article_points = article_info["score"]
        article_time = int(article_info["time"]) / 3600
        article_total_score = (article_points - 1) / pow((article_time + 2), 1.8)
        nested_dict[article] = article_total_score
    dict(sorted(nested_dict.items(), key=lambda item: item[1], reverse=True))
    articles_score = nested_dict
    logging.debug("program managed to sort top 40 articles from HN by descending order")


def get_list():
    """
    prints the top 40 articles' titles by their order, with a simple numbering system.
    """
    numbering_sys = 1
    print("please wait...")
    get_top()
    rate()
    for key in articles_score:
        response = requests.get(key)
        title = response.json()
        title_actual = title["title"]
        print(f"{numbering_sys}. {title_actual}")
        numbering_sys += 1
    logging.debug("program is printing top 40 articles titles and their respective numbers")


def start():
    """
    The main function. combines all neccessary functions to create the HN-shell,
    while also offering a refresh option for the articles list, and an option to
    escape the program.
    """
    global game_on
    input("welcome to ShellHN!\nenter any key to get the 40 most popular articles in Hacker News! ")
    get_list()
    while game_on:
        again_q = input("to refresh the list- enter r\nto exit the application- enter any key: ")
        if again_q == "r" or again_q == "R":
            print("\n" * 10)
            get_list()
        if again_q != "r" or again_q != "R":
            game_on = False
            print("\n" * 10)
            print("goodbye!")
    logging.debug("program finished operation successfully")


start()
