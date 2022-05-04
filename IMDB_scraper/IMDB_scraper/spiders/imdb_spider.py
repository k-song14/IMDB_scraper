# to run
# scrapy crawl imdb_spider -o movies.csv

import scrapy
from scrapy.linkextractors import LinkExtractor

class ImdbSpider(scrapy.Spider):
    name='imdb_spider'

    start_urls = ['https://www.imdb.com/title/tt1638002/']

#parse method to know what to do with the response object

    def parse(self,response):
        '''parse method; begins at our initial page (imdb for movie)
        goes to our desired next page (cast + crew).
        '''
        # we know that our next page is: 
        # https://www.imdb.com/title/tt1638002/fullcredits/?ref_=tt_cl_sm
        # we join the urls to get our next page

        next_page = response.urljoin("https://www.imdb.com/title/tt1638002/fullcredits/?ref_=tt_cl_sm")
        
        #this gives us the url we want

        #once we get to the next page, call on parse_full_credits method
        yield scrapy.Request(next_page, callback=self.parse_full_credits)

    def parse_full_credits(self, response):
        '''generates and visits sites of all actors in cast and crew
        section of our movie
        '''
        #empty vector to store joint urls
        actor_page = []

        #list of relative paths for each actor
        actors = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        #joins url for each relative path in actors; appends to list actor_page
        for i in actors:
            actor_page.append(response.urljoin(i))

        #yields request for each url in list
        for link in actor_page:
            yield scrapy.Request(link, callback=self.parse_actor_page)

    def parse_actor_page(self, response):
        '''creates dictionary with movies worked on by actor and
        corresponding actor name
        '''
        #extracts name from header
        actor_name = response.css("div div table tbody tr td h1 span.itemprop::text").get()
        #extracts movies and tv shows, puts them in a list
        movie_or_TV_name = response.css("div b a::text").getall()

        for name in movie_or_TV_name:

            yield{

            "actor": actor_name,
            "movie_or_TV_name": name

        }


        
