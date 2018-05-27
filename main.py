import praw
import redis
import os

search_term = os.environ['SEARCH_TERM']

client_id = os.environ['CLIENT']
client_secret = os.environ['SECRET']
user_agent = os.environ['USER']

redis_host = os.environ['REDIS_HOST']
redis_port = 6379
set_name = "dashboard"


def main():
    redis_db = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

    for e in reddit.subreddit('all').stream.submissions():
        if search_term in str.lower(e.title):
            print("%s: %s - %s, %s" % (e.created_utc, e.title, e.author, e.selftext))
            key = 'red_%s' % e.id
            redis_db.hsetnx(key,
                            {"title": e.title, "author": e.author.name, "text": e.selftext, "timestamp": e.created_utc})


if __name__ == "__main__":
    main()
