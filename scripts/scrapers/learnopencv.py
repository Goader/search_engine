import scrapy


class Spider(scrapy.Spider):
    name = "learnopencv"
    start_urls = ['https://learnopencv.com/']

    def parse(self, response):
        ARTICLE_SELECTOR = '.entry-title a ::attr(href)'
        for article_ref in response.css(ARTICLE_SELECTOR).extract():
            yield scrapy.Request(
                response.urljoin(article_ref),
                callback=self.parse_article
            )

        NEXT_PAGE_SELECTOR = '.pagination-next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )

    def parse_article(self, response):
        TITLE_SELECTOR = 'title ::text'
        title = response.css(TITLE_SELECTOR)
        CONTENT_SELECTOR = '.entry-content'
        content = response.css(CONTENT_SELECTOR)
        if content:
            yield {
                'link': response.url,
                'name': title.extract_first(),
                'article': content.extract_first(),
            }
