import datetime
import itertools

import click

from nori.facebook import Facebook
from nori.feedly import Feedly
from nori.utils import grouper


def stats(facebook_token, feedly_token, count, days):
    feedly = Feedly(feedly_token)
    fb = Facebook(facebook_token)

    # retrieve the categories from feedly, each category has label and an id
    # that will be used to fetch the entries streams
    categories = feedly.get_categories()

    results = []
    for category in categories:
        click.echo("Processing category '%s'" % category['label'])

        # get the latest entries for the feeds in the category
        date_from = datetime.datetime.utcnow() - datetime.timedelta(days=days)
        entries = feedly.get_streams_contents(
            stream_id=category['id'],
            count=count,
            newer_than=date_from.timestamp())

        # extract links from the items
        links = map(lambda item: item['alternate'][0]['href'], entries['items'])

        # here we split the link list in groups of 4 elements.
        # this is needed in order to avoid problems with lenght of
        # the request's url
        for group in grouper(links, 4):
            stats = fb.get_urls(*group)

            # filter out stats with no share to avoid errors
            stats = [item for item in stats.values() if 'og_object' in item]
            results.extend(stats)

    return results


@click.command()
@click.option('--facebook-token', envvar='NORI_FACEBOOK_TOKEN',
              help='Facebook API token')
@click.option('--feedly-token', envvar='NORI_FEEDLY_TOKEN',
              help='Feedly API token')
@click.option('-c', '--count', default=20,
              help='Fetch at least `count` entries from each feedly stream')
@click.option('-d', '--days', default=1,
              help='Fetch only entries newer than `days` ago.')
@click.option('-C', '--output-count', default=10,
              help='Print only `output-count` results')
def cli(facebook_token, feedly_token, count, days, output_count):
    click.echo("Getting streams from feedly...")

    results = stats(facebook_token, feedly_token, count, days)

    # sort the results by share count
    results = sorted(results, key=lambda e: e['share']['share_count'], reverse=True)

    click.echo('###### RESULTS #######')
    for item in itertools.islice(results, output_count):
        click.echo('share count: %s - comments: %s - updated: %s' % (
            item['share']['share_count'], item['share']['comment_count'], item['og_object']['updated_time']))
        click.echo('url: %s' % item['id'])
        click.echo('---')
