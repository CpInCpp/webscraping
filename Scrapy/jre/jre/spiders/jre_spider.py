from scrapy import Spider
from jre.items import JreItem
from scrapy import Request


class JRESpider(Spider):
    name = 'jre_spider'
    allowed_urls = ['https://www.jrepodcast.com/']
    start_urls = ['https://www.jrepodcast.com/']

    def parse(self, response):
        # Find the total number of pages in the result so that we can decide how many urls to scrape next
        text = response.xpath('//*[@id="site-main"]/div[2]/div/nav/div/a[6]/text()').extract_first()
        number_pages = int(text)

        # List comprehension to construct all the urls
        result_urls = ['https://www.jrepodcast.com/page/{}/'.format(x) for x in range(2, number_pages + 1)]
        result_urls = self.start_urls + result_urls
        # Yield the requests to different search result urls,
        # using parse_result_page function to parse the response.
        for url in result_urls:
            yield Request(url=url, callback=self.parse_result_page)

    def parse_result_page(self, response):
        ep_list = response.xpath('//ul[@class="site-archive-posts"]//text()').extract()

        #split ep_list into new lists of items per episode.
        # runtime = [ep_list[e] for e in range(1, len(ep_list), 8)]
        # title = []
        # airdate = []
        # views = []
        # likes = []
        # dislikes = []
        # ratio = []

        # [runtime.append(ep_list[e]) for e in range(1,len(ep_list+1),8)]
        # [title.append(ep_list[e]) for e in range(2, len(ep_list + 1), 8)]
        # [airdate.append(ep_list[e]) for e in range(3, len(ep_list + 1), 8)]
        # [views.append(ep_list[e]) for e in range(4, len(ep_list + 1), 8)]
        # [likes.append(ep_list[e]) for e in range(5, len(ep_list + 1), 8)]
        # [dislikes.append(ep_list[e]) for e in range(6, len(ep_list + 1), 8)]
        # [ratio.append(ep_list[e]) for e in range(7, len(ep_list + 1), 8)]

        for e in range(1, len(ep_list), 8):
            runtime = ep_list[e]
            title = ep_list[e + 1]
            airdate = ep_list[e + 2]
            views = ep_list[e + 3]
            likes = ep_list[e + 4]
            dislikes = ep_list[e + 5]
            ratio = ep_list[e + 6]

            item = JreItem()  # should this go outside the for loop?
            item['runtime'] = runtime
            item['ep_title'] = title
            item['airdate'] = airdate
            item['views'] = views
            item['likes'] = likes
            item['dislikes'] = dislikes
            item['ratio'] = ratio
            yield item
