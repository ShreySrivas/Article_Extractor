import scrapy
import json
import pandas as pd
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.http.request import Request
class ArticleSpiderSpider(CrawlSpider):
    name = 'article_spider'

    def start_requests(self):
        # Read the input file and extract the URLs
        df = pd.read_excel('ArticleExtractor\Input.xlsx')
        urls = df['URL'].tolist()
        global url_to_id
        url_to_id = dict(zip(df['URL'], df['URL_ID']))
        id_to_url = dict([(value, key) for key, value in url_to_id.items()])
        with open("ArticleExtractor\id_to_url.json", "w") as outfile:
            json.dump(id_to_url, outfile)
        #yield Request(url=urls[0], callback=self.parse)
        for url in urls:
           yield Request(url=url, callback=self.parse)
    def parse(self, response):
        # Extract the article title and text
        
        title = Selector(response).xpath('/html/body/div[6]/article/div[1]/div[1]/div[2]/div/header/h1/text()').extract_first()
        print(title)
        text = Selector(response).xpath('/html/body/div[6]/article/div[2]/div/div[1]/div/div[1]/p/text()').extract()
        print(text)
        # Save the extracted data in a text file with the URL_ID as its file name
        url_id = url_to_id.get(response.url)
        #url_id = response.url.split('/')[-2]
        with open(f'ArticleExtractor\extracted_articles\{url_id}.txt', 'w') as f:
            f.write(title + '\n\n')
            f.write('\n'.join(text))

# Run the spider
process = CrawlerProcess()
process.crawl(ArticleSpiderSpider)
process.start()
