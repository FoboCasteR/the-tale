import os
import argparse

from tt_web import utils

from .. import service
from .. import operations


parser = argparse.ArgumentParser(description='Run service')

parser.add_argument('-c',
                    '--config',
                    metavar='config',
                    default=os.environ.get('TT_CONFIG'),
                    type=str,
                    help='path to config file')


def main():
    args = parser.parse_args()

    config = utils.load_config(args.config)

    async def utility():
        await operations.rollback_hanged_transactions()

    service.run_utility(config, utility)
