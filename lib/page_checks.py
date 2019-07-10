import logging, pprint, sys, traceback

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


def check_A():
    """ Tests Hay `Archives/Manuscripts` `David Beckwith papers` requirement. """

    browser = Firefox(options=opts)
    browser.implicitly_wait( settings.BROWSER_WAIT_SECONDS )

    ## load page
    aim = """

-------
Goal: Ensure a format of `Archives/Manuscripts` with a location of `ANNEX HAY` shows the easyrequest_hay request url.
-------"""
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
    log.info( f'first_item.text, ```{first_item.text}```' )
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
        self.browser.implicitly_wait( settings.BROWSER_WAIT_SECONDS )

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
        aim = """

-------
Goal: Ensure a format of `Archives/Manuscripts` with a location of `HAY MANUSCRIPTS` shows the direct Aeon request url -- _if_ the status is `AVAILABLE`.
-------"""
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


class JohnHayCheck:

    def __init__(self):
        self.browser = Firefox(options=opts)
        self.browser.implicitly_wait( settings.BROWSER_WAIT_SECONDS )
        self.bib = 'b2498067'
        self.blast_limits()

    def blast_limits(self):
        """ Warms availability cache to work around localhost and dblightcit lack of 'more' functionality. """
        url = f'{settings.PRODUCTION_ROOT_PAGE_URL}/{self.bib}?limit=false'
        self.browser.get( url )


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

        ## third item info (hay manuscript item)
        third_item = self.browser.find_element_by_id( 'item_184781917' )
        ( location, call_number, status ) = self.get_third_item_info( third_item )

        ## third item empties test
        for class_type in [ 'scan', 'jcb_url', 'ezb_volume_url', 'annexhay_easyrequest_url' ]:
            request_link = third_item.find_element_by_class_name( class_type )
            assert request_link.text == '', f'request_link.text, ```{request_link.text}```'

        ## third item request-link test -- direct Aeon link SHOULD show
        request_link = third_item.find_element_by_class_name( 'hay_aeon_url' )
        assert request_link.text.strip() == 'request-access', f'request_link.text, ```{request_link.text}```'

        self.browser.close()
        log.info( f'Result: test passed.' )  # won't get here unless all asserts pass

        ## end def run_check()

    def load_page( self ):
        """ Hits url; returns browser object.
            Called by run_check() """
        aim = """

-------
Goal: Ensure a bib-format of `Archives/Manuscripts` with items of varying locations shows the proper type of request url -- _if_ the status is `AVAILABLE`.
-------"""
        log.info( aim )
        url = f'{settings.ROOT_PAGE_URL}/{self.bib}?limit=false'
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

    def get_third_item_info( self, third_item ):
        """ Parses item.
            Called by run_check() """
        log.info( f'third_item.text, ```{third_item.text}```' )
        location = third_item.find_element_by_class_name( 'location' )
        assert location.text == 'HAY MANUSCRIPTS', f'location.text, ```{location.text}```'
        #
        call_number = third_item.find_element_by_class_name( 'callnumber' )
        assert call_number.text == 'Ms.HAY Box 20 - Photographs', f'call_number.text, ```{call_number.text}```'
        #
        status = third_item.find_element_by_class_name( 'status' )
        assert status.text == 'AVAILABLE', f'status.text, ```{status.text}```'
        return ( location, call_number, status )

    ## end class JohnHayCheck


class GregorianCheck:

    def __init__(self):
        self.browser = Firefox(options=opts)
        self.browser.implicitly_wait( settings.BROWSER_WAIT_SECONDS )

    def run_check(self):
        """ Tests Hay `Archives/Manuscripts` `Vartan Gregorian papers` requirement.
            For reference:
            - annex-hay RESTRICTED item, `item_142740093`
            - annex-hay non-restricted item, `item_142740287`
            """

        self.load_page()

        ## format
        format_element = self.browser.find_elements_by_class_name( 'blacklight-format' )[1]  # [0] is the word 'Format'
        assert format_element.text == 'Archives/Manuscripts', f'format_element.text, ```{format_element.text}```'

        ## first item info (annex-hay item available item)
        first_item = self.browser.find_element_by_id( 'item_142740093' )
        # log.info( f'first_item.text, ```{first_item.text}```' )
        ( location, call_number, status ) = self.get_first_item_info( first_item )

        ## first item empties test -- NO link should show
        for class_type in [ 'scan', 'jcb_url', 'hay_aeon_url', 'ezb_volume_url', 'annexhay_easyrequest_url' ]:
            request_link = first_item.find_element_by_class_name( class_type )
            assert request_link.text == '', f'request_link.text, ```{request_link.text}```'

        ## second item info (due item)
        second_item = self.browser.find_element_by_id( 'item_142740287' )
        ( location, call_number, status ) = self.get_second_item_info( second_item )

        ## second item empties test
        for class_type in [ 'scan', 'jcb_url', 'hay_aeon_url', 'ezb_volume_url' ]:
            request_link = second_item.find_element_by_class_name( class_type )
            assert request_link.text == '', f'request_link.text, ```{request_link.text}```'

        ## second item link test -- `annexhay_easyrequest_url` link SHOULD show
        request_link = second_item.find_element_by_class_name( 'annexhay_easyrequest_url' )
        assert request_link.text.strip() == 'request-access', f'request_link.text, ```{request_link.text}```'

        self.browser.close()
        log.info( f'Result: test passed.' )  # won't get here unless all asserts pass

        ## end def run_check()

    def load_page( self ):
        """ Hits url; returns browser object.
            Called by run_check() """
        aim = """

-------
Goal: Ensure a bib-format of `Archives/Manuscripts` with items of `RESTRICTED` status cannot be requested.
-------"""
        log.info( aim )
        bib = 'b4115486'
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
        assert call_number.text == 'OF-1C-16 Box 1', f'call_number.text, ```{call_number.text}```'
        #
        status = first_item.find_element_by_class_name( 'status' )
        assert status.text == 'RESTRICTED', f'status.text, ```{status.text}```'
        return ( location, call_number, status )

    def get_second_item_info( self, second_item ):
        """ Parses item.
            Called by run_check() """
        log.info( f'second_item.text, ```{second_item.text}```' )
        location = second_item.find_element_by_class_name( 'location' )
        assert location.text == 'ANNEX HAY', f'location.text, ```{location.text}```'
        #
        call_number = second_item.find_element_by_class_name( 'callnumber' )
        assert call_number.text == 'OF-1C-16 Box 4', f'call_number.text, ```{call_number.text}```'
        #
        status = second_item.find_element_by_class_name( 'status' )
        assert status.text == 'AVAILABLE', f'status.text, ```{status.text}```'
        return ( location, call_number, status )

    ## end class GregorianCheck


class BrownCheck:

    def __init__(self):
        self.browser = Firefox(options=opts)
        self.browser.implicitly_wait( settings.BROWSER_WAIT_SECONDS )
        self.bib = 'b3969016'
        self.blast_limits()

    def blast_limits(self):
        """ Warms availability cache to work around localhost and dblightcit lack of 'more' functionality. """
        url = f'{settings.PRODUCTION_ROOT_PAGE_URL}/{self.bib}?limit=false'
        self.browser.get( url )

    def run_check(self):
        """ Tests Hay `Archives/Manuscripts` `John Nicholas Brown II papers` requirement.
            For reference:
            - annex-hay RESTRICTED-via-callnumber item, `item_184782697`
            - annex-hay non-restricted item, `item_140852803`
            """

        self.load_page()

        ## format
        format_element = self.browser.find_elements_by_class_name( 'blacklight-format' )[1]  # [0] is the word 'Format'
        assert format_element.text == 'Archives/Manuscripts', f'format_element.text, ```{format_element.text}```'

        ## first item info (annex-hay item available, but restricted-via-callnumber item)
        first_item = self.browser.find_element_by_id( 'item_184782697' )
        # log.info( f'first_item.text, ```{first_item.text}```' )
        ( location, call_number, status ) = self.get_first_item_info( first_item )

        ## first item empties test -- NO link should show
        for class_type in [ 'scan', 'jcb_url', 'hay_aeon_url', 'ezb_volume_url', 'annexhay_easyrequest_url' ]:
            request_link = first_item.find_element_by_class_name( class_type )
            assert request_link.text == '', f'request_link.text, ```{request_link.text}```'

        ## second item info (regular annex-hay available item)
        second_item = self.browser.find_element_by_id( 'item_140852803' )
        ( location, call_number, status ) = self.get_second_item_info( second_item )

        ## second item empties test
        for class_type in [ 'scan', 'jcb_url', 'hay_aeon_url', 'ezb_volume_url' ]:
            request_link = second_item.find_element_by_class_name( class_type )
            assert request_link.text == '', f'request_link.text, ```{request_link.text}```'

        ## second item link test -- `annexhay_easyrequest_url` link SHOULD show
        request_link = second_item.find_element_by_class_name( 'annexhay_easyrequest_url' )
        assert request_link.text.strip() == 'request-access', f'request_link.text, ```{request_link.text}```'

        self.browser.close()
        log.info( f'Result: test passed.' )  # won't get here unless all asserts pass

        ## end def run_check()

    def load_page( self ):
        """ Hits url; returns browser object.
            Called by run_check() """
        aim = """

-------
Goal: Ensure a bib-format of `Archives/Manuscripts` -- with items that are `RESTRICTED` via callnumber -- cannot be requested.
-------"""
        log.info( aim )
        url = f'{settings.ROOT_PAGE_URL}/{self.bib}?limit=false'
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
        assert call_number.text == 'Ms.2007.012 Box 142 - RESTRICTED', f'call_number.text, ```{call_number.text}```'
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
        assert call_number.text == 'Ms.2007.012 Box 8', f'call_number.text, ```{call_number.text}```'
        #
        status = second_item.find_element_by_class_name( 'status' )
        assert status.text == 'AVAILABLE', f'status.text, ```{status.text}```'
        return ( location, call_number, status )

    ## end class BrownCheck


class MiscMicrofilmCheck:

    def __init__(self):
        self.browser = Firefox(options=opts)
        self.browser.implicitly_wait( settings.BROWSER_WAIT_SECONDS )
        self.bib = 'b2734709'
        self.first_item_id = 'item_159973284'

    def run_check(self):
        """ Checks that `HAY MICROFLM` items are not requestable. """

        self.load_page()

        ## format
        format_element = self.browser.find_elements_by_class_name( 'blacklight-format' )[1]  # [0] is the word 'Format'
        assert format_element.text == 'Archives/Manuscripts', f'format_element.text, ```{format_element.text}```'

        ## first item info (hay-microfilm, no)
        first_item = self.browser.find_element_by_id( self.first_item_id )
        # log.info( f'first_item.text, ```{first_item.text}```' )
        ( location, call_number, status ) = self.get_first_item_info( first_item )

        ## first item empties test -- NO link should show
        for class_type in [ 'scan', 'jcb_url', 'hay_aeon_url', 'ezb_volume_url', 'annexhay_easyrequest_url' ]:
            request_link = first_item.find_element_by_class_name( class_type )
            assert request_link.text == '', f'request_link.text, ```{request_link.text}```'

        self.browser.close()
        log.info( f'Result: test passed.' )  # won't get here unless all asserts pass

        ## end def run_check()

    def load_page( self ):
        """ Hits url; returns browser object.
            Called by run_check() """
        aim = """

-------
Goal: Ensure a bib-format of `Archives/Manuscripts` -- with items that are `RESTRICTED` via callnumber -- cannot be requested.
-------"""
        log.info( aim )
        url = f'{settings.ROOT_PAGE_URL}/{self.bib}?limit=false'
        log.info( f'hitting url, ```{url}```' )
        #
        self.browser.get( url )
        return

    def get_first_item_info( self, first_item ):
        """ Parses item.
            Called by run_check() """
        log.info( f'first_item.text, ```{first_item.text}```' )
        location = first_item.find_element_by_class_name( 'location' )
        assert location.text == 'HAY MICROFLM', f'location.text, ```{location.text}```'
        #
        call_number = first_item.find_element_by_class_name( 'callnumber' )
        assert call_number.text == 'F5701 reel 2', f'call_number.text, ```{call_number.text}```'
        #
        status = first_item.find_element_by_class_name( 'status' )
        assert status.text == 'USE IN LIBRARY', f'status.text, ```{status.text}```'
        return ( location, call_number, status )

    ## end class MiscMicrofilmCheck
