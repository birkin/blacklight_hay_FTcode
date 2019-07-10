import logging, pprint, sys, time, traceback

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


def check_format( bib ):
    """ Checks format.
        Called by bib item-getters. """
    format = bib.find_elements_by_class_name( 'title-subheading' )[-1]  # initial non-format line may exist
    assert format.text == 'Archives/Manuscripts', f'format.text, `{format.text}`'
    return


class BeckwithResultsCheck:

    def __init__(self):
        self.browser = Firefox(options=opts)
        self.query = 'f[format][]=Archives/Manuscripts&q=beckwith'
        self.first_item_target_callnumber = 'Ms.2010.010 Box 2'
        self.second_item_target_callnumber = 'Ms.2015.016 Box 1, DVD 2 - Andes, Cheri'
        # self.blast_limits()

    def run_check(self):
        """ Checks permutations of `Archives/Manuscripts` `beckwith` search results. """

        self.load_page()

        ## first item (annex-hay item available)
        first_item_row = self.get_item( self.first_item_target_callnumber )
        ( location, call_number, status ) = self.get_item_info( first_item_row )

        ## first item data checks
        assert location.text == 'ANNEX HAY', f'location.text, ```{location.text}```'
        assert call_number.text == self.first_item_target_callnumber, f'call_number.text, ```{call_number.text}```'
        assert 'AVAILABLE' in status.text, f'status.text, ```{status.text}```'  # request-access link will also be here (odd but true)

        ## first item link-check
        assert 'request-access' in status.text, f'status.text, ```{status.text}```'
        link = status.find_element_by_tag_name( 'a' )
        assert 'easyrequest_hay/confirm' in link.get_attribute('href'), link.get_attribute('href')

        ## second item (hay-manuscripts with use-in-library status)
        second_item_row = self.get_item( self.second_item_target_callnumber )
        ( location, call_number, status ) = self.get_item_info( second_item_row )

        ## second item data checks
        assert location.text == 'HAY MANUSCRIPTS', f'location.text, ```{location.text}```'
        assert call_number.text == self.second_item_target_callnumber, f'call_number.text, ```{call_number.text}```'
        assert 'USE IN LIBRARY' in status.text, f'status.text, ```{status.text}```'  # request-access link will also be here (odd but true)

        ## second item link-check
        assert 'request-access' in status.text, f'status.text, ```{status.text}```'
        link = status.find_element_by_tag_name( 'a' )
        assert 'brown.aeon.atlas-sys.com' in link.get_attribute('href'), link.get_attribute('href')

        self.browser.close()
        log.info( f'Result: test passed.' )  # won't get here unless all asserts pass

        ## end def run_check()

    def load_page( self ):
        """ Hits url; returns browser object.
            Called by run_check() """
        aim = """\n-------\nGoal: `ANNEX HAY` location items with status `AVAILABLE` will have an easyrequest-hay link,
      & `HAY MANUSCRIPTS` location items with status `USE IN LIBRARY` will have an Aeon link. """
        log.info( aim )
        url = f'{settings.ROOT_PAGE_URL}?{self.query}'
        log.info( f'hitting url, ```{url}```' )
        #
        self.browser.get( url )
        self.browser.implicitly_wait(2)
        # time.sleep( 1 )  # lets js load up page
        return

    def get_item( self, target_callnumber ):
        """ Grabs bibs, finds correct row and returns it.
            Called by run_check() """
        bibs = self.browser.find_elements_by_css_selector( 'div.document' )
        # assert len(bibs) == 3, len(bibs)
        target_row = 'init'
        for bib in bibs:
            rows = bib.find_elements_by_tag_name( 'tr' )
            for row in rows:
                if target_callnumber in row.text:
                    target_row = row
                    log.debug( f'target_row found, ```{target_row.text}```' )
                    break
            if target_row != 'init':
                check_format( bib )
                break
        log.info( f'target_row.text, ```{target_row.text}```' )
        assert target_callnumber in target_row.text
        return target_row

    def get_item_info( self, first_row ):
        """ Parses item.
            Called by run_check() """
        cells = first_row.find_elements_by_tag_name( 'td' )
        location = cells[0]
        call_number = cells[1]
        status = cells[2]
        return ( location, call_number, status )

    ## end class BeckwithResultsCheck


class YokenResultsCheck:

    def __init__(self):
        self.browser = Firefox(options=opts)
        self.query = 'f[format][]=Archives/Manuscripts&q=yoken'
        self.first_item_target_callnumber = 'Ms.2011.038 Box 1'

    def run_check(self):
        """ Tests `Archives/Manuscripts` `yoken` search results. """

        self.load_page()

        ## first item info (annex-hay item available)
        first_row = self.get_first_item()
        ( location, call_number, status ) = self.get_first_item_info( first_row )

        ## first item data checks
        assert location.text == 'HAY MANUSCRIPTS', f'location.text, ```{location.text}```'
        assert call_number.text == self.first_item_target_callnumber, f'call_number.text, ```{call_number.text}```'
        assert 'AVAILABLE' in status.text, f'status.text, ```{status.text}```'  # request-access link will also be here (odd but true)

        ## first item link-check
        assert 'request-access' in status.text, f'status.text, ```{status.text}```'
        link = status.find_element_by_tag_name( 'a' )
        assert 'brown.aeon.atlas-sys.com' in link.get_attribute('href'), link.get_attribute('href')

        self.browser.close()
        log.info( f'Result: test passed.' )  # won't get here unless all asserts pass

        ## end def run_check()

    def load_page( self ):
        """ Hits url; returns browser object.
            Called by run_check() """
        aim = """\n-------\nGoal: `HAY MANUSCRIPTS` location items with status `AVAILABLE` will have an Aeon link. """
        log.info( aim )
        url = f'{settings.ROOT_PAGE_URL}?{self.query}'
        log.info( f'hitting url, ```{url}```' )
        self.browser.get( url )
        self.browser.implicitly_wait(2)
        return

    def get_first_item( self ):
        """ Grabs bibs, finds second row in first bib.
            Called by run_check() """
        bibs = self.browser.find_elements_by_css_selector( 'div.document' )
        # assert len(bibs) == 1, len(bibs)
        first_bib = bibs[0]
        check_format( first_bib )
        rows = first_bib.find_elements_by_tag_name( 'tr' )
        target_row = 'init'
        for row in rows:
            if self.first_item_target_callnumber in row.text:
                target_row = row
                break
        log.info( f'target_row.text, ```{target_row.text}```' )
        assert self.first_item_target_callnumber in target_row.text
        return target_row

    def get_first_item_info( self, first_row ):
        """ Parses item.
            Called by run_check() """
        cells = first_row.find_elements_by_tag_name( 'td' )
        location = cells[0]
        call_number = cells[1]
        status = cells[2]
        return ( location, call_number, status )

    ## end class YokenCheck


class JohnHayResultsCheck:

    def __init__(self):
        self.browser = Firefox(options=opts)
        self.query = 'f[format][]=Archives/Manuscripts&q=John Hay Papers'
        self.first_item_target_callnumber = 'Ms.HAY Box 2'  # annex-hay, available, yes
        self.second_item_target_callnumber = 'Ms.HAY Box 4'  # annex-hay, due, no
        self.third_item_target_callnumber = 'F5701 reel 2'  # hay-microfilm, no
        self.fourth_item_target_callnumber = '1-SIZE E664.H41 A3 1997ms v.2'  # hay-john-hay, no
        # self.blast_limits()

    def run_check(self):
        """ Checks permutations of `Archives/Manuscripts` `john hay papers` search results. """

        self.load_page()

        ## first item (annex-hay item available)
        first_item_row = self.get_item( self.first_item_target_callnumber )
        ( location, call_number, status ) = self.get_item_info( first_item_row )

        ## first item data checks
        assert location.text == 'ANNEX HAY', f'location.text, ```{location.text}```'
        assert call_number.text == self.first_item_target_callnumber, f'call_number.text, ```{call_number.text}```'
        assert 'AVAILABLE' in status.text, f'status.text, ```{status.text}```'  # request-access link will also be here (odd but true)

        ## first item link-check
        assert 'request-access' in status.text, f'status.text, ```{status.text}```'
        link = status.find_element_by_tag_name( 'a' )
        assert 'easyrequest_hay/confirm' in link.get_attribute('href'), link.get_attribute('href')

        ## second item (annex-hay, due, no)
        second_item_row = self.get_item( self.second_item_target_callnumber )
        ( location, call_number, status ) = self.get_item_info( second_item_row )

        ## second item data checks
        assert location.text == 'ANNEX HAY', f'location.text, ```{location.text}```'
        assert call_number.text == self.second_item_target_callnumber, f'call_number.text, ```{call_number.text}```'
        assert 'DUE 06-22-18' in status.text, f'status.text, ```{status.text}```'  # request-access link will also be here (odd but true)

        ## second item link-check
        assert 'request-access' not in status.text, f'status.text, ```{status.text}```'

        ## third item (hay-microfilm, no)
        third_item_row = self.get_item( self.third_item_target_callnumber )
        ( location, call_number, status ) = self.get_item_info( third_item_row )

        ## third item data checks
        assert location.text == 'HAY MICROFLM', f'location.text, ```{location.text}```'
        assert call_number.text == self.third_item_target_callnumber, f'call_number.text, ```{call_number.text}```'
        assert 'USE IN LIBRARY' in status.text, f'status.text, ```{status.text}```'  # request-access link will also be here (odd but true)

        ## third item link-check
        assert 'request-access' not in status.text, f'status.text, ```{status.text}```'

        ## fourth item (hay-john-hay, no)
        fourth_item_row = self.get_item( self.fourth_item_target_callnumber )
        ( location, call_number, status ) = self.get_item_info( fourth_item_row )

        ## fourth item data checks
        assert location.text == 'HAY JOHN-HAY', f'location.text, ```{location.text}```'
        assert call_number.text == self.fourth_item_target_callnumber, f'call_number.text, ```{call_number.text}```'
        assert 'USE IN LIBRARY' in status.text, f'status.text, ```{status.text}```'  # request-access link will also be here (odd but true)

        ## fourth item link-check
        assert 'request-access' not in status.text, f'status.text, ```{status.text}```'

        self.browser.close()
        log.info( f'Result: test passed.' )  # won't get here unless all asserts pass

        ## end def run_check()

    def load_page( self ):
        """ Hits url; returns browser object.
            Called by run_check() """
        aim = """\n-------\nGoal: `ANNEX HAY` location items with status `AVAILABLE` will have an easyrequest-hay link,
      & `HAY MANUSCRIPTS` location items with status `USE IN LIBRARY` will have an Aeon link. """
        log.info( aim )
        url = f'{settings.ROOT_PAGE_URL}?{self.query}'
        log.info( f'hitting url, ```{url}```' )
        #
        self.browser.get( url )
        self.browser.implicitly_wait(2)
        # time.sleep( 1.66 )  # lets js load up page
        return

    def get_item( self, target_callnumber ):
        """ Grabs bibs, finds correct row and returns it.
            Called by run_check() """
        # log.info( f'target_callnumber, ```{target_callnumber}```' )
        bibs = self.browser.find_elements_by_css_selector( 'div.document' )
        # assert len(bibs) == 10, len(bibs)
        target_row = 'init'
        for bib in bibs:
            rows = bib.find_elements_by_tag_name( 'tr' )
            for row in rows:
                # log.info( f'row.text, ```{row.text}```' )
                if target_callnumber in row.text:
                    target_row = row
                    log.debug( f'target_row found, ```{target_row.text}```' )
                    break
            if target_row != 'init':
                check_format( bib )
                break
        log.info( f'target_row.text, ```{target_row.text}```' )
        assert target_callnumber in target_row.text
        return target_row

    def get_item_info( self, first_row ):
        """ Parses item.
            Called by run_check() """
        cells = first_row.find_elements_by_tag_name( 'td' )
        location = cells[0]
        call_number = cells[1]
        status = cells[2]
        return ( location, call_number, status )

    ## end class JohnHayResultsCheck


class GregorianResultsCheck:

    def __init__(self):
        self.browser = Firefox(options=opts)
        self.query = 'f[format][]=Archives/Manuscripts&q=Vartan Gregorian papers'
        self.first_item_target_callnumber = 'OF-1C-16 Box 2'  # annex-hay, restricted, no
        self.second_item_target_callnumber = 'OF-1C-16 Box 5'  # annex-hay, available, yes
        self.third_item_target_callnumber = 'OF-1ZSE-1'  # hay-archives, use-in-library, yes
        # self.blast_limits()

    def run_check(self):
        """ Checks permutations of `Archives/Manuscripts` `john hay papers` search results. """

        self.load_page()

        ## first item (annex-hay, restricted, no)
        first_item_row = self.get_item( self.first_item_target_callnumber )
        ( location, call_number, status ) = self.get_item_info( first_item_row )

        ## first item data checks
        assert location.text == 'ANNEX HAY', f'location.text, ```{location.text}```'
        assert call_number.text == self.first_item_target_callnumber, f'call_number.text, ```{call_number.text}```'
        assert 'RESTRICTED' in status.text, f'status.text, ```{status.text}```'  # request-access link will also be here (odd but true)

        ## first item link-check
        assert 'foo-request-access' not in status.text, f'status.text, ```{status.text}```'
        # link = status.find_element_by_tag_name( 'a' )
        # assert 'foo' in link.get_attribute('href'), link.get_attribute('href')

        ## second item (annex-hay, available, yes)
        second_item_row = self.get_item( self.second_item_target_callnumber )
        ( location, call_number, status ) = self.get_item_info( second_item_row )

        ## second item data checks
        assert location.text == 'ANNEX HAY', f'location.text, ```{location.text}```'
        assert call_number.text == self.second_item_target_callnumber, f'call_number.text, ```{call_number.text}```'
        assert 'AVAILABLE' in status.text, f'status.text, ```{status.text}```'  # request-access link will also be here (odd but true)

        ## second item link-check
        assert 'request-access' in status.text, f'status.text, ```{status.text}```'
        link = status.find_element_by_tag_name( 'a' )
        assert 'easyrequest_hay' in link.get_attribute('href'), link.get_attribute('href')

        ## third item (hay-archives, use-in-library, yes)
        third_item_row = self.get_item( self.third_item_target_callnumber )
        ( location, call_number, status ) = self.get_item_info( third_item_row )

        ## third item data checks
        assert location.text == 'HAY ARCHIVES', f'location.text, ```{location.text}```'
        assert call_number.text == self.third_item_target_callnumber, f'call_number.text, ```{call_number.text}```'
        assert 'USE IN LIBRARY' in status.text, f'status.text, ```{status.text}```'  # request-access link will also be here (odd but true)

        ## third item link-check
        assert 'request-access' in status.text, f'status.text, ```{status.text}```'
        link = status.find_element_by_tag_name( 'a' )
        assert 'brown.aeon.atlas-sys.com' in link.get_attribute('href'), link.get_attribute('href')

        self.browser.close()
        log.info( f'Result: test passed.' )  # won't get here unless all asserts pass

        ## end def run_check()

    def load_page( self ):
        """ Hits url; returns browser object.
            Called by run_check() """
        aim = """\n-------\nGoal: `ANNEX HAY` location items with status `AVAILABLE` will have an easyrequest-hay link,
      & `HAY MANUSCRIPTS` location items with status `USE IN LIBRARY` will have an Aeon link. """
        log.info( aim )
        url = f'{settings.ROOT_PAGE_URL}?{self.query}'
        log.info( f'hitting url, ```{url}```' )
        #
        self.browser.get( url )
        self.browser.implicitly_wait(2)
        # time.sleep( 1.66 )  # lets js load up page
        return

    def get_item( self, target_callnumber ):
        """ Grabs bibs, finds correct row and returns it.
            Called by run_check() """
        # log.info( f'target_callnumber, ```{target_callnumber}```' )
        bibs = self.browser.find_elements_by_css_selector( 'div.document' )
        # assert len(bibs) == 3, len(bibs)
        target_row = 'init'
        for bib in bibs:
            rows = bib.find_elements_by_tag_name( 'tr' )
            for row in rows:
                # log.info( f'row.text, ```{row.text}```' )
                if target_callnumber in row.text:
                    target_row = row
                    log.debug( f'target_row found, ```{target_row.text}```' )
                    break
            if target_row != 'init':
                check_format( bib )
                break
        log.info( f'target_row.text, ```{target_row.text}```' )
        assert target_callnumber in target_row.text
        return target_row

    def get_item_info( self, first_row ):
        """ Parses item.
            Called by run_check() """
        cells = first_row.find_elements_by_tag_name( 'td' )
        location = cells[0]
        call_number = cells[1]
        status = cells[2]
        return ( location, call_number, status )

    ## end class GregorianResultsCheck


class BrownResultsCheck:

    def __init__(self):
        self.browser = Firefox(options=opts)
        self.query = 'f[format][]=Archives/Manuscripts&q=John Nicholas Brown II papers'
        self.first_item_target_callnumber = 'Ms.2007.012 Box 10'  # annex-hay, available, yes
        self.second_item_target_callnumber = 'Ms.2007.012 Box 142 - RESTRICTED'  # annex-hay, available, but restricted by callnumber, no
        self.blast_limits()

    def blast_limits(self):
        """ Warms availability cache to work around localhost and dblightcit lack of 'more' functionality. """
        url = f'{settings.PRODUCTION_ROOT_PAGE_URL}/b3969016?limit=false'
        log.info( f'limit-blaster url, ```{url}```' )
        self.browser.get( url )

    def run_check(self):
        """ Checks permutations of `Archives/Manuscripts` `john hay papers` search results. """

        self.load_page()

        ## first item (annex-hay, available, yes)
        first_item_row = self.get_item( self.first_item_target_callnumber )
        ( location, call_number, status ) = self.get_item_info( first_item_row )

        ## first item data checks
        assert location.text == 'ANNEX HAY', f'location.text, ```{location.text}```'
        assert call_number.text == self.first_item_target_callnumber, f'call_number.text, ```{call_number.text}```'
        assert 'AVAILABLE' in status.text, f'status.text, ```{status.text}```'  # request-access link will also be here (odd but true)

        ## first item link-check
        assert 'request-access' in status.text, f'status.text, ```{status.text}```'
        link = status.find_element_by_tag_name( 'a' )
        assert 'easyrequest_hay' in link.get_attribute('href'), link.get_attribute('href')

        ## second item (annex-hay, available, but restricted by callnumber, no)
        second_item_row = self.get_item( self.second_item_target_callnumber )
        ( location, call_number, status ) = self.get_item_info( second_item_row )

        ## second item data checks
        assert location.text == 'ANNEX HAY', f'location.text, ```{location.text}```'
        assert call_number.text == self.second_item_target_callnumber, f'call_number.text, ```{call_number.text}```'
        assert 'AVAILABLE' in status.text, f'status.text, ```{status.text}```'  # request-access link will also be here (odd but true)

        ## second item link-check
        assert 'request-access' not in status.text, f'status.text, ```{status.text}```'
        # link = status.find_element_by_tag_name( 'a' )
        # assert 'foo' in link.get_attribute('href'), link.get_attribute('href')

        self.browser.close()
        log.info( f'Result: test passed.' )  # won't get here unless all asserts pass

        ## end def run_check()

    def load_page( self ):
        """ Hits url; returns browser object.
            Called by run_check() """
        aim = """\n-------\nGoal: `ANNEX HAY` location items with status `AVAILABLE` will have an easyrequest-hay link,
      & `HAY MANUSCRIPTS` location items with status `USE IN LIBRARY` will have an Aeon link. """
        log.info( aim )
        url = f'{settings.ROOT_PAGE_URL}?{self.query}'
        log.info( f'hitting url, ```{url}```' )
        #
        self.browser.get( url )
        self.browser.implicitly_wait(2)
        # time.sleep( 1.66 )  # lets js load up page
        return

    def get_item( self, target_callnumber ):
        """ Grabs bibs, finds correct row and returns it.
            Called by run_check() """
        # log.info( f'target_callnumber, ```{target_callnumber}```' )
        bibs = self.browser.find_elements_by_css_selector( 'div.document' )
        # assert len(bibs) == 2, len(bibs)
        target_row = 'init'
        for bib in bibs:
            rows = bib.find_elements_by_tag_name( 'tr' )
            for row in rows:
                # log.info( f'row.text, ```{row.text}```' )
                if target_callnumber in row.text:
                    target_row = row
                    log.debug( f'target_row found, ```{target_row.text}```' )
                    break
            if target_row != 'init':
                check_format( bib )
                break
        log.info( f'target_row.text, ```{target_row.text}```' )
        assert target_callnumber in target_row.text
        return target_row

    def get_item_info( self, first_row ):
        """ Parses item.
            Called by run_check() """
        cells = first_row.find_elements_by_tag_name( 'td' )
        location = cells[0]
        call_number = cells[1]
        status = cells[2]
        return ( location, call_number, status )

    ## end class BrownResultsCheck
