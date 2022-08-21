# Unit 12 Homework: Mission to Mars

In this assignment, you will build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. The following information outlines what you need to do.



## Part  1: Scraping

Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.

* Create a Jupyter Notebook file called `mission_to_mars.ipynb`. Use this file to complete all your scraping and analysis tasks. The following information outlines what you need to scrape.

### NASA Mars News

* Scrape the [Mars News Site](https://redplanetscience.com/) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

```python
# Example:
    html = browser.html   
    mars_soup = bs(html, "html.parser")
    news_title= mars_soup.find_all('div',      class_='content_title')[0].text
    news_date= mars_soup.find_all('div', class_='list_date')[0].text 
    news_p= mars_soup.find_all('div', class_='article_teaser_body')[0].text
```

### JPL Mars Space Images—Featured Image

* Visit the URL for the Featured Space Image site [here](https://spaceimages-mars.com).

* Use Splinter to navigate the site and find the image URL for the current Featured Mars Image, then assign the URL string to a variable called `featured_image_url`.

* Be sure to find the image URL to the full-sized `.jpg` image.

* Be sure to save a complete URL string for this image.

```python
# Example:
    jpl_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_url)
    html = browser.html
    img_soup = bs(html, "html.parser")
    relative_image_path=img_soup.find_all('img', class_='headerimage fade-in')[0]["src"]
    featured_image_url= (f'{jpl_url}{relative_image_path}')
```

### Mars Facts

* Visit the [Mars Facts webpage](https://galaxyfacts-mars.com) and use Pandas to scrape the table containing facts about the planet including diameter, mass, etc.

* Use Pandas to convert the data to a HTML table string.

### Mars Hemispheres

* Visit the [astrogeology site](https://marshemispheres.com/) to obtain high-resolution images for each hemisphere of Mars.

* You will need to click each of the links to the hemispheres in order to find the image URL to the full-resolution image.

* Save the image URL string for the full resolution hemisphere image and the hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.

* Append the dictionary with the image URL string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

```python
# Example:
    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)
    html = browser.html
    hemi_soup = bs(html, "html.parser")
    mars_hemi=hemi_soup.find_all('div', class_='item')
    hemi_href=[]
    for row in mars_hemi:
        hemi_href.append(hemi_url+ (row.find('a', class_='itemLink product-item')['href']))
    # empty list for hemispheres
    hemi_img_urls = []
    # loop to get title and link of image
    for url in hemi_href:
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        title = soup.find('h2', class_ = 'title').text
        par_url=soup.find('img', class_ = 'wide-image')['src']
        img_url = hemi_url + par_url
        hemi_img_urls.append({'title': title, 'img_url': img_url})

```

- - -

## Part 2: MongoDB and Flask Application

* Started by converting Jupyter notebook into a Python script called `scrape_mars.py` by using a function called `scrape`. This function executes all your scraping code and returns one Python dictionary containing all the scraped data.

* Next, created a route called `/scrape` that imported`scrape_mars.py` script and called `scrape` function.

  * Stored the return value in Mongo as a Python dictionary.

* Created a root route `/` that queries Mongo database and pass the Mars data into an HTML template for displaying the data.

* Created a template HTML file called `index.html` that takes the Mars data dictionary and display all the data in the appropriate HTML elements.

![final_app_part1.png](images/final_app.png)

- - -
