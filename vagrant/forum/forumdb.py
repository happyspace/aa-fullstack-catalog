#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach


## Database connection


## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''

    con = psycopg2.connect("dbname=forum")
    cursor = con.cursor()

    cursor.execute("select * from posts order by time desc limit 10")
    results = cursor.fetchall()
    posts = [{'content': bleach.clean(str(row[1])), 'time': str(row[0])} for row in results]


     # posts.sort(key=lambda row: row['time'], reverse=True)
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    t = time.strftime('%c', time.localtime())

    clean = bleach.clean(content)

    con = psycopg2.connect("dbname=forum")
    cursor = con.cursor()
    cursor.execute("insert into posts (content) values (%s)", (clean,))
    con.commit()
    # DB.append((t, content))
