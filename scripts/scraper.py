import os
import time


if __name__ == '__main__':
    SCRAPERS_DIR = 'scrapers'
    JSONS_DIR = 'jsons'

    for json_file in os.listdir(JSONS_DIR):
        os.remove(os.path.join(JSONS_DIR, json_file))

    time.sleep(1)

    for scraper in os.listdir(SCRAPERS_DIR):
        if scraper.endswith('.py'):
            json_name = scraper[:scraper.rfind('.')] + '.json'
            os.system(f'scrapy runspider {os.path.join(SCRAPERS_DIR, scraper)} -O {os.path.join(JSONS_DIR, json_name)}')
