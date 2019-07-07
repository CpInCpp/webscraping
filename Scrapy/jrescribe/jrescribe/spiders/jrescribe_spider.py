from scrapy import Spider
from jrescribe.items import JrescribeItem
from scrapy import Request
from scrapy.utils.python import to_native_str
from six.moves.urllib.parse import urljoin

class JREScribeSpider(Spider):
    name = 'jrescribe_spider'
    allowed_urls = ['https://jrescribe.com/']
    start_urls = ['https://jrescribe.com/transcripts/p1264.html']
    handle_httpstatus_list = [301, 302]
    def parse(self, response):
        if response.status >= 300 and response.status < 400:

            # HTTP header is ascii or latin1, redirected url will be percent-encoded utf-8
            location = to_native_str(response.headers['location'].decode('latin1'))

            # get the original request
            request = response.request
            # and the URL we got redirected to
            redirected_url = urljoin(request.url, location)

            if response.status in (301, 307) or request.method == 'HEAD':
                redirected = request.replace(url=redirected_url, callback=self.parse_result_page)
                yield redirected
            else:
                redirected = request.replace(url=redirected_url, method='GET', body='', callback=self.parse_result_page)
                redirected.headers.pop('Content-Type', None)
                redirected.headers.pop('Content-Length', None)
                yield redirected


    def parse_result_page(self, response):
        paragraph_list = response.xpath('//*[@id="app"]/div/div[3]/div[1]//p//text()').extract()
        #text = ' '.join(paragraph_list)

        #split ep_list into new lists of items per episode.

        item = JrescribeItem()
        item['text'] = paragraph_list
        yield item