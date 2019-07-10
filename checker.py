"""
Usage: from 'blacklight_hay_FTcode' directory...

  $ source ../env_bh_selenium/bin/activate
  (env_bh_selenium) $ python3 ./checker.py
"""

import logging, pprint, sys, traceback

import settings
from lib import page_checks
from lib.page_checks import YokenCheck, JohnHayCheck, GregorianCheck, BrownCheck, MiscMicrofilmCheck
from lib.results_checks import BeckwithResultsCheck, YokenResultsCheck, JohnHayResultsCheck, GregorianResultsCheck, BrownResultsCheck


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)


def run_page_checks():
    """ Manages functional-checks for bib-pages. """
    try:
        page_checks.check_A()         # `David Beckwith papers`
        yoken = YokenCheck()          # `Mel B. Yoken collection`
        yoken.run_check()
        john_hay = JohnHayCheck()     # `John Hay papers`
        john_hay.run_check()
        gregorian = GregorianCheck()  # `Vartan Gregorian papers`
        gregorian.run_check()
        brown = BrownCheck()          # `John Nicholas Brown II papers`
        brown.run_check()
        microfilm = MiscMicrofilmCheck()
        microfilm.run_check()
    except Exception:
        log.exception( 'exception; traceback...' )
        # raise

def run_results_checks():
    """ Manages functional-checks for bib-pages. """
    try:
        beckwith = BeckwithResultsCheck()    # `David Beckwith papers`
        beckwith.run_check()
        yoken = YokenResultsCheck()          # `Mel B. Yoken collection`
        yoken.run_check()
        john_hay = JohnHayResultsCheck()     # `John Hay papers`
        john_hay.run_check()
        gregorian = GregorianResultsCheck()  # `Vartan Gregorian papers`
        gregorian.run_check()
        brown = BrownResultsCheck()          # `John Nicholas Brown II papers`
        brown.run_check()
    except Exception:
        log.exception( 'exception; traceback...' )
        # raise


run_page_checks()
run_results_checks()
try:
    browser.close()
except:
    pass
log.info( '\n-------\nAll checks complete' )
