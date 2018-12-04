import os
import csv
from nose.tools import assert_equal
from draftfast import rules
from draftfast import optimize
from draftfast.csv_parse import uploaders, salary_download


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def test_dk_nba_upload():
    players = salary_download.generate_players_from_csvs(
        game=rules.DRAFT_KINGS,
        salary_file_location='{}/data/dk_nba_salaries.csv'.format(CURRENT_DIR),
    )
    roster = optimize.run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=players,
        verbose=True,
    )
    upload_file = '{}/data/current-upload.csv'.format(CURRENT_DIR)
    uploader = uploaders.DraftKingsNBAUploader(
        pid_file='{}/data/dk_nba_pids.csv'.format(CURRENT_DIR),
        upload_file=upload_file,
    )
    uploader.write_rosters([roster])

    row = None
    with open(upload_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for idx, row in enumerate(reader):
            if idx == 0:
                continue
    assert_equal(
        row,
        [
            '11743190',
            '11743146',
            '11743013',
            '11743142',
            '11743007',
            '11743176',
            '11743369',
            '11743024',
        ]
    )