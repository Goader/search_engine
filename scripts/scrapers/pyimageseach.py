import scrapy


class Spider(scrapy.Spider):
    name = "pyimagesearch"
    # 'https://learnopencv.com/object-tracking-using-opencv-cpp-python/',
    # start_urls = ['https://www.pyimagesearch.com/2018/07/30/opencv-object-tracking/']
    start_urls = ['https://www.pyimagesearch.com/topics/']

    def parse(self, response):
        TOPIC_SELECTOR = '.topic'
        for topic in response.css(TOPIC_SELECTOR):
            TOPIC_REF_SELECTOR = '.topic__title a ::attr(href)'
            for topic_ref in topic.css(TOPIC_REF_SELECTOR).extract():
                yield scrapy.Request(
                    response.urljoin(topic_ref),
                    callback=self.parse_topic
                )

    def parse_topic(self, response):
        ARTICLE_SELECTOR = '.post-summary'
        for article in response.css(ARTICLE_SELECTOR):
            ARTICLE_REF_SELECTOR = '.post-summary a ::attr(href)'
            for article_ref in article.css(ARTICLE_REF_SELECTOR).extract():
                yield scrapy.Request(
                    response.urljoin(article_ref),
                    callback=self.parse_article
                )

        NEXT_PAGE_SELECTOR = '.pagination-next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse_topic
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
