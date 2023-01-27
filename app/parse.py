import re
import sys
import snscrape.modules.twitter as snstwitter
import datetime
import pytz
import time
from config import Config
from app import create_app
from rq import get_current_job
from app import db
from app.models import Task
import logging

app = create_app()
app.app_context().push()


def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        if progress >= 100:
            task.complete = True
        db.session.commit()


def scrap(sources: list, regs):
    try:
        now = datetime.datetime.now(tz=pytz.utc)
        start = time.time()
        tweets = []
        since = now - datetime.timedelta(days=Config.TIME_INTERVAL)
        _set_task_progress(0)
        for acc in sources:
            print(acc)
            print('HUUUI')
            query = f'(from:{acc} since:{since.strftime("%Y-%m-%d")} until:{now.strftime("%Y-%m-%d")})'
            print(query)
            app.logger.info(f'{query}')
            for tweet in snstwitter.TwitterSearchScraper(query).get_items():
                tweets.append({'url': tweet.url, 'content': tweet.rawContent, 'date': tweet.date})
        print(tweets)
        app.logger.info(f'{tweets}')
        print("--- %s seconds ---" % (time.time() - start))
        print(len(tweets))
        _set_task_progress(100)
        return parser(tweets, regs)
    except:
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())


def parser(tweets, regs):
    print(regs)
    app.logger.info(f'{regs}')
    r = '|'.join(regs)
    print(r)
    app.logger.info(f'{r}')
    regex = fr'^(?=.*({r})).*$'
    print(regex)
    app.logger.info(f'{regex}')
    matched = []
    for i in tweets:
        raw_text = i['content'].split()
        raw_text = ' '.join(raw_text).lower()
        parse_result = re.match(regex, raw_text)
        if parse_result:
            matched.append(i)
    print(matched)
    app.logger.info(f'{matched}')
    return matched

