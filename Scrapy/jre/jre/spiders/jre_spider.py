from scrapy import Spider
from jre.items import JreItem
from scrapy import Request



# globally set up my list of tags to iterate through.
tags1 = ['activists', 'actors', 'artists', 'athletes-fighters-martial-arts', 'authors', 'auto-moto']
tags2 = ['business', 'comedians', 'filmmakers', 'food-nutrition', 'health', 'hunters', 'inventors']
tags3 = ['it-game-dev-programming', 'journalists', 'military-law-enforcement', 'miscellaneous', 'models']
tags4 = ['musicians', 'politics', 'writers']
tags = tags1 + tags2 + tags3 + tags4


class JRESpider(Spider):
    name = 'jre_spider'
    allowed_urls = ['https://www.jrepodcast.com/']
    start_urls = ['https://www.jrepodcast.com/episodes/{}/'.format(t) for t in tags]
    #start_urls = ['https://www.jrepodcast.com/']

    def parse(self, response):
        #categories = ['https://www.jrepodcast.com/episodes/{}/'.format(tag) for tag in tags]
        for tag in tags:
            cat_url = 'https://www.jrepodcast.com/episodes/{}/'.format(tag)
            yield Request(url=cat_url, meta={'tag':tag}, callback=self.parse_first_page)


    def parse_first_page(self, response):
        # Find the total number of pages in the result so that we can decide how many urls to scrape next

        tag = response.meta['tag']
        page_number_text_list = response.xpath('//*[@class="page-numbers"]//text()').extract()
        url = ['https://www.jrepodcast.com/episodes/{}/'.format(tag)]


        if len(page_number_text_list) != 0:
            number_pages = int(page_number_text_list[-1])
            suffix_list = ['page/{}/'.format(x) for x in range(2, number_pages+1)]
            urls = url + [url[0] + item for item in suffix_list]
        else:
            urls = url
        for u in urls:
            yield Request(url=u, meta={'tag': tag}, callback=self.parse_result_page)






    def parse_result_page(self, response):
        tag = response.meta['tag']
        ep_list = response.xpath('//*[@class="site-archive-posts"]//text()').extract()

        #split ep_list into new lists of items per episode.


        for e in range(1, len(ep_list), 8):
            # split ep_list into new lists of items per episode.
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
            item['tag'] = tag
            yield item
