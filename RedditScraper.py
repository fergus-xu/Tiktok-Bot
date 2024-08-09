# generate txt files of reddit posts
import praw
import os
import helper
from unidecode import unidecode

def make_reddit():
    settings = helper.read_settings("settings.txt")
    client_id = settings.get("client_id")
    client_secret = settings.get("client_secret")
    user_agent = settings.get("user_agent")
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    subreddit = input("What subreddit do you want to access? ")
    subreddit = reddit.subreddit(subreddit)
    filter_by = input("What do you want to filter by? ")
    if filter_by == "":
        filter_by = "top"
    num = input("How many posts? ")
    if num == "":
        num = 10
    num = int(num)
    if filter_by.lower() == "top":
        criteria = input("What time period? ")
        if criteria == "":
            criteria = "all"
        posts = subreddit.top(time_filter=criteria, limit=num)
    elif filter_by.lower() == "hot":
        posts = subreddit.hot(limit=num)
    elif filter_by.lower() == "new":
        posts = subreddit.new(limit=num)
    elif filter_by.lower() == "controversial":
        posts = subreddit.controversial(limit=num)
    else:
        return 0
    subreddit_name = subreddit.display_name
    folder_name = settings.get('folder') # change file naming
    current_directory = os.getcwd()
    new_directory_path = os.path.join(current_directory, folder_name)
    helper.clean(new_directory_path)
    if not os.path.exists(new_directory_path):
        os.mkdir(new_directory_path)
    if not os.path.exists(f"{new_directory_path}/{subreddit_name}"):
        os.mkdir(f"{new_directory_path}/{subreddit_name}")
    for idx, post in enumerate(posts, start=1):
        post_id = post.id
        file_name = f"{new_directory_path}/{subreddit_name}/{post_id}.txt"  # Define file name for each post
        with open(file_name, 'w', encoding='utf-8') as file:
            file_text = post.title + '\n' + post.selftext
            file_text = format_text(file_text)
            file.write(file_text)
            print(f"Post written to {file_name}")
    return f"{new_directory_path}/{subreddit_name}"


def format_text(text: str): # formats text into useable format
    # determine which format is most useful
    # remove title, check to make sure everything is str valid
    # need to handle curly apostrophe
    table = {
        ord('‘'): "'",
        ord('’'): "'",
        ord('“'): '"',
        ord('”'): '"'
    }
    text = text.translate(table)
    text = unidecode(text)
    return text
