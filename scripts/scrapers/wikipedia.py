import scrapy
from scrapy.exceptions import CloseSpider
from collections import deque


class Spider(scrapy.Spider):
    name = "wikipedia"
    start_urls = ['https://en.wikipedia.org/wiki/Machine_learning']
    processed = 0
    UPPER_BOUND = 50000

    # using BFS instead of DFS
    queue = deque()

    visited = set()

    def parse(self, response):
        if not response.url.startswith('https://en.wikipedia.org/wiki/') \
                or response.url in self.visited:
            return
        if self.processed >= self.UPPER_BOUND:
            raise CloseSpider('Upper bound exceeded')

        self.visited.add(response.url)
        self.processed += 1

        TITLE_SELECTOR = 'title ::text'
        title = response.css(TITLE_SELECTOR)
        CONTENT_SELECTOR = '.mw-parser-output p ::text'
        content = response.css(CONTENT_SELECTOR).extract()
        if content:
            yield {
                'link': response.url,
                'name': title.extract_first(),
                'article': '. '.join(content),
            }

        NEXT_PAGE_SELECTOR = '.mw-parser-output p a ::attr(href)'
        for next_page in response.css(NEXT_PAGE_SELECTOR).extract():
            if self.processed + len(self.queue) <= self.UPPER_BOUND:
                self.queue.append(next_page)

        while self.queue and self.processed <= self.UPPER_BOUND:
            yield scrapy.Request(
                response.urljoin(self.queue.popleft()),
                callback=self.parse,
                dont_filter=False
            )
