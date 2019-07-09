import logging, pprint, sys, traceback

# import selenium
import settings
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)


opts = Options()
# opts.set_headless()
# assert opts.headless  # Operating in headless mode
browser = Firefox(options=opts)


def run_checks():
    """ Manages functional-checks. """
    try:
        check_A()
    except Exception:
        log.exception( 'exception; traceback...' )
        # raise


def check_A():
    """ Tests Hay `Archives/Manuscripts` requirement. """

    ## load page
    aim = """\n-------\nGoal: Ensure a format of `Archives/Manuscripts` with a location of `ANNEX HAY` shows the easyrequest_hay request url. """
    log.info( aim )
    log.info( f'hitting url, ```{settings.URL_A}```' )
    #
    browser.get( settings.URL_A )

    ## format
    format_element = browser.find_elements_by_class_name( 'blacklight-format' )[1]  # [0] is the word 'Format'
    assert format_element.text == 'Archives/Manuscripts', f'format_element.text, ```{format_element.text}```'

    ## main item info
    first_item = browser.find_elements_by_class_name( 'bib_item' )[0]
    # print( f'first_item.text, ```{first_item.text}```' )
    location = first_item.find_element_by_class_name( 'location' )
    assert location.text == 'ANNEX HAY', f'location.text, ```{location.text}```'
    #
    call_number = first_item.find_element_by_class_name( 'callnumber' )
    assert call_number.text == 'Ms.2010.010 Box 1', f'call_number.text, ```{call_number.text}```'
    #
    status = first_item.find_element_by_class_name( 'status' )
    assert status.text == 'AVAILABLE', f'status.text, ```{status.text}```'

    ## empties
    for class_type in [ 'scan', 'jcb_url', 'hay_aeon_url', 'ezb_volume_url' ]:
        empty_link_element = first_item.find_element_by_class_name( class_type )
        assert empty_link_element.text == '', f'empty_link_element.text, ```{empty_link_element.text}```'
        # print( f'good, no class_type, {class_type}' )

    ## real test
    easyrequest_hay_url = first_item.find_element_by_class_name( 'annexhay_easyrequest_url' )
    assert easyrequest_hay_url.text.strip() == 'request-access', f'easyrequest_hay_url.text, ```{easyrequest_hay_url.text}```'

    log.info( f'Result: All good.' )  # won't get here unless all asserts pass

    ## end def check_A()


run_checks()
browser.close()
log.info( '\n-------\nAll checks complete' )

