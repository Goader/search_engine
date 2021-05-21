# import scrapy
#
#
# class Spider(scrapy.Spider):
#     name = "stackoverflow"
#     start_urls = ['https://stackoverflow.com/questions/tagged/tensorflow?tab=votes&pagesize=50',
#                   'https://stackoverflow.com/questions/tagged/deep-learning?tab=votes&pagesize=50',
#                   'https://stackoverflow.com/questions/tagged/machine-learning?tab=votes&pagesize=50',
#                   'https://stackoverflow.com/questions/tagged/keras?tab=votes&pagesize=50']
#
#     def parse(self, response):
#         ARTICLE_SELECTOR = '.question-hyperlink ::attr(href)'
#         for article_ref in response.css(ARTICLE_SELECTOR).extract():
#             yield scrapy.Request(
#                 response.urljoin(article_ref),
#                 callback=self.parse_article
#             )
#
#         NEXT_PAGE_SELECTOR = '.s-pagination--item.js-pagination-item[rel="next"]::attr(href)'
#         next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
#         if next_page:
#             print('\n'*20)
#             yield scrapy.Request(
#                 response.urljoin(next_page),
#                 callback=self.parse
#             )
#
#     def parse_article(self, response):
#         TITLE_SELECTOR = 'title ::text'
#         title = response.css(TITLE_SELECTOR)
#
#         CONTENT_SELECTOR = '.s-prose.js-post-body ::text'
#         yield {
#             'link': response.url,
#             'name': title.extract_first(),
#             'article': '. '.join(response.css(CONTENT_SELECTOR).extract()),
#         }
