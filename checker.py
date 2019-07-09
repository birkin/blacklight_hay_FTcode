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
# browser = Firefox(options=opts)


def run_checks():
    """ Manages functional-checks. """
    try:
        # check_A()                  # `David Beckwith papers`
        # yoken = YokenCheck()       # `Mel B. Yoken collection`
        # yoken.run_check()
        john_hay = JohnHayCheck()  # `John Hay papers`
        john_hay.run_check()
    except Exception:
        log.exception( 'exception; traceback...' )
        # raise




class JohnHayCheck:

    def __init__(self):
        self.browser = Firefox(options=opts)

    def run_check(self):
        """ Tests Hay `Archives/Manuscripts` `John Hay papers` requirement.
            For reference:
            - annex-hay item, `item_18327071x`
            - 'due' item, `item_183270745`
            - hay-manuscript item, `item_184781917`
            """

        self.load_page()

        ## format
        format_element = self.browser.find_elements_by_class_name( 'blacklight-format' )[1]  # [0] is the word 'Format'
        assert format_element.text == 'Archives/Manuscripts', f'format_element.text, ```{format_element.text}```'

        ## first item info (annex-hay item available item)
        first_item = self.browser.find_element_by_id( 'item_18327071x' )
        # log.info( f'first_item.text, ```{first_item.text}```' )
        ( location, call_number, status ) = self.get_first_item_info( first_item )

        ## first item empties test -- only `annexhay_easyrequest_url`  should show
        for class_type in [ 'scan', 'jcb_url', 'hay_aeon_url', 'ezb_volume_url' ]:
            request_link = first_item.find_element_by_class_name( class_type )
            assert request_link.text == '', f'request_link.text, ```{request_link.text}```'

        ## first item url test -- `easyrequest_hay_url` link SHOULD show
        request_link = first_item.find_element_by_class_name( 'annexhay_easyrequest_url' )
        assert request_link.text.strip() == 'request-access', f'request_link.text, ```{request_link.text}```'

        ## second item info (due item)
        second_item = self.browser.find_element_by_id( 'item_183270745' )
        ( location, call_number, status ) = self.get_second_item_info( second_item )

        ## second item empties test -- no link should show
        for class_type in [ 'scan', 'jcb_url', 'hay_aeon_url', 'ezb_volume_url', 'annexhay_easyrequest_url' ]:
            request_link = second_item.find_element_by_class_name( class_type )
            assert request_link.text == '', f'request_link.text, ```{request_link.text}```'




        # ## third item info (hay manuscript item)
        # third_item = self.browser.find_element_by_id( 'item_184781917' )
        # ( location, call_number, status ) = self.get_third_item_info( third_item )




        self.browser.close()
        log.info( f'Result: test passed.' )  # won't get here unless all asserts pass

        ## end def run_check()

    def load_page( self ):
        """ Hits url; returns browser object.
            Called by run_check() """
        aim = """\n-------\nGoal: Ensure a bib-format of `Archives/Manuscripts` with items of varying locations
shows the proper type of request url -- _if_ the status is `AVAILABLE`. """
        log.info( aim )
        bib = 'b2498067'
        url = f'{settings.ROOT_PAGE_URL}/{bib}'
        log.info( f'hitting url, ```{url}```' )
        #
        self.browser.get( url )
        return

    def get_first_item_info( self, first_item ):
        """ Parses item.
            Called by run_check() """
        log.info( f'first_item.text, ```{first_item.text}```' )
        location = first_item.find_element_by_class_name( 'location' )
        assert location.text == 'ANNEX HAY', f'location.text, ```{location.text}```'
        #
        call_number = first_item.find_element_by_class_name( 'callnumber' )
        assert call_number.text == 'Ms.HAY Box 1', f'call_number.text, ```{call_number.text}```'
        #
        status = first_item.find_element_by_class_name( 'status' )
        assert status.text == 'AVAILABLE', f'status.text, ```{status.text}```'
        return ( location, call_number, status )

    def get_second_item_info( self, second_item ):
        """ Parses item.
            Called by run_check() """
        log.info( f'second_item.text, ```{second_item.text}```' )
        location = second_item.find_element_by_class_name( 'location' )
        assert location.text == 'ANNEX HAY', f'location.text, ```{location.text}```'
        #
        call_number = second_item.find_element_by_class_name( 'callnumber' )
        assert call_number.text == 'Ms.HAY Box 4', f'call_number.text, ```{call_number.text}```'
        #
        status = second_item.find_element_by_class_name( 'status' )
        assert status.text == 'DUE 06-22-18', f'status.text, ```{status.text}```'
        return ( location, call_number, status )

    ## end class JohnHayCheck






def check_A():
    """ Tests Hay `Archives/Manuscripts` `David Beckwith papers` requirement. """

    browser = Firefox(options=opts)

    ## load page
    aim = """\n-------\nGoal: Ensure a format of `Archives/Manuscripts` with a location of `ANNEX HAY` shows the easyrequest_hay request url. """
    log.info( aim )
    bib = 'b5706110'
    url = f'{settings.ROOT_PAGE_URL}/{bib}'
    log.info( f'hitting url, ```{url}```' )
    #
    browser.get( url )

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

    ## empties test
    for class_type in [ 'scan', 'jcb_url', 'hay_aeon_url', 'ezb_volume_url' ]:
        empty_link_element = first_item.find_element_by_class_name( class_type )
        assert empty_link_element.text == '', f'empty_link_element.text, ```{empty_link_element.text}```'
        # print( f'good, no class_type, {class_type}' )

    ## real test -- easyrequest-hay link should show
    request_link = first_item.find_element_by_class_name( 'annexhay_easyrequest_url' )
    assert request_link.text.strip() == 'request-access', f'request_link.text, ```{request_link.text}```'

    browser.close()
    log.info( f'Result: test passed.' )  # won't get here unless all asserts pass

    ## end def check_A()


class YokenCheck:

    def __init__(self):
        self.browser = Firefox(options=opts)

    def run_check(self):
        """ Tests Hay `Archives/Manuscripts` `Mel B. Yoken collection` requirement. """

        self.load_page()

        ## format
        format_element = self.browser.find_elements_by_class_name( 'blacklight-format' )[1]  # [0] is the word 'Format'
        assert format_element.text == 'Archives/Manuscripts', f'format_element.text, ```{format_element.text}```'

        ## first item info
        first_item = self.browser.find_elements_by_class_name( 'bib_item' )[0]
        ( location, call_number, status ) = self.get_first_item_info( first_item )

        ## first item test -- NO links should show
        for class_type in [ 'scan', 'jcb_url', 'hay_aeon_url', 'ezb_volume_url', 'annexhay_easyrequest_url' ]:
            request_link = first_item.find_element_by_class_name( class_type )
            assert request_link.text == '', f'request_link.text, ```{request_link.text}```'

        ## second item info
        second_item = self.browser.find_elements_by_class_name( 'bib_item' )[1]
        ( location, call_number, status ) = self.get_second_item_info( second_item )

        ## second item empties test -- only hay_aeon_url should show, no others
        for class_type in [ 'scan', 'jcb_url', 'annexhay_easyrequest_url', 'ezb_volume_url' ]:
            # log.info( f'class_type, {class_type}' )
            request_link = second_item.find_element_by_class_name( class_type )
            assert request_link.text == '', f'request_link.text, ```{request_link.text}```'

        ## second item hay_aeon_url test -- link SHOULD show
        request_link = second_item.find_element_by_class_name( 'hay_aeon_url' )
        assert request_link.text.strip() == 'request-access', f'request_link.text, ```{request_link.text}```'

        self.browser.close()
        log.info( f'Result: test passed.' )  # won't get here unless all asserts pass

        ## end def run_check()

    def load_page( self ):
        """ Hits url; returns browser object.
            Called by run_check() """
        aim = """\n-------\nGoal: Ensure a format of `Archives/Manuscripts` with a location of `HAY MANUSCRIPTS`
shows the direct Aeon request url -- _if_ the status is `AVAILABLE`. """
        log.info( aim )
        bib = 'b3589814'
        url = f'{settings.ROOT_PAGE_URL}/{bib}'
        log.info( f'hitting url, ```{url}```' )
        #
        self.browser.get( url )
        return

    def get_first_item_info( self, first_item ):
        """ Parses item.
            Called by run_check() """
        log.info( f'first_item.text, ```{first_item.text}```' )
        location = first_item.find_element_by_class_name( 'location' )
        assert location.text == 'HAY MANUSCRIPTS', f'location.text, ```{location.text}```'
        #
        call_number = first_item.find_element_by_class_name( 'callnumber' )
        assert call_number.text == 'Oversize Box 1XX', f'call_number.text, ```{call_number.text}```'
        #
        status = first_item.find_element_by_class_name( 'status' )
        assert status.text == '--', f'status.text, ```{status.text}```'
        return ( location, call_number, status )

    def get_second_item_info( self, second_item ):
        """ Parses item.
            Called by run_check() """
        log.info( f'second_item.text, ```{second_item.text}```' )
        location = second_item.find_element_by_class_name( 'location' )
        assert location.text == 'HAY MANUSCRIPTS', f'location.text, ```{location.text}```'
        #
        call_number = second_item.find_element_by_class_name( 'callnumber' )
        assert call_number.text == 'Ms.2011.038 Box 1', f'call_number.text, ```{call_number.text}```'
        #
        status = second_item.find_element_by_class_name( 'status' )
        assert status.text == 'AVAILABLE', f'status.text, ```{status.text}```'
        return ( location, call_number, status )

    ## end class YokenCheck


run_checks()
try:
    browser.close()
except:
    pass
log.info( '\n-------\nAll checks complete' )

