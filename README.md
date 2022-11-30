# Dropshipping Online Store API (based on PrintfulAPI)
**Dropshipping Online Store API** - educational project, online store API, the project uses PrintfulAPI 
for get data product of your store on the Printful marketplace. This project has a fairly high 
accuracy in available sizes, colors, and other product data. You will have only up-to-date data 
to the minute, so a buyer can't order the product, which not in Printful stock on order moment.
Each of your product data will be stored in the NoSQL database for one minute because Printful API 
has a limited of number requests, with 120 requests in one minute. All requests were implemented
asynchronously, so we got quick responses. One user request may consist of a few dozen requests to 
Printful API, but we can get response during couple-few seconds, or faster if need data stored in database.
---
Available to you the following: 
* Get all your products by(up to) 12 products on each page of catalog
* Product data by specific product id in your store and global id(Printful catalog)
* Get filtered products data
* Make order

-----

### Navigation:

* [Launch]()
  * [standard](#standard)
  * [using docker-compose](#docker)
* [Go to auto docs](#go_to_site)
* [More about the project](#more_about_project_EN)
***
<br>
<br>



Launch
---
#### Standard<a name="standard"></a>
___
Before starting, you must check for the existence of a virtual environment or create one if necessary.
If you are use Linux then you need write `python` or `python3` before commands listed below
In the directory with `requirements.txt` need running
``` 
pip install -r requirements.txt
```
Then you need install Redis or use docker for this purpose, it is desirable to use port 6379 or set up 
connection with redis in .env file.
<br> 
Then you can run project use command:
```
uvicorn main:app --reload
```
And you can run tests, run: ```pytest tests```

<br>
<br>
<br>

#### Docker-compose<a name="docker"></a>
___
Before using docker, you must be Docker Desktop running
In directory with docker-compose.yml need to run:
```docker-compose up --build```

For stop container, you need to run `Ctrl+C` or 
```docker-compose stop```

For renewal him, you need run:
```docker-compose up```

For delete container with volumes and image, you need to run:
```docker-compose down --volumes --rmi local```

To available the container's bash you need to run:
```docker-compose exec -it online_store bash```

Inside which you can, for example, call the tests:
```pytest tests```

<br>
<br>

Go to auto docs<a name="go_to_site"></a>
---
Next, follow the path http://localhost:8000/docs
<br>
<br>
<br>


More about the project <a name='more_about_project_EN'></a>
---


### Store(DB)
We store data about product, products ids of catalog pages, all products ids of  your online store and orders which
didn't fit in available requests quantity. Only orders data haven't limited time to live, but other stored data have 
time to live equal one minute.
* Data about a product. It is ready data, for example, of which consists a catalog. The decision was made to store 
  basic data in this way because this method guarantees flexible properties and queries economy. This data can be used 
  to respond to product request, catalog request, or catalog filtering request. Product data contain base product data 
  from your store and several additional fields: available colors, sizes and field, which binds each size with list of 
  objects from corresponding available colors, variant ids, prices. Additional fields are based on data from Printful 
  Catalog.
* Data about catalog page. It is data about catalog page number and list from ids products of your online store, which
  placed on this page.
* All products ids. It is list contains all products ids of your online store which we find after filtering your 
  products.
* Data of orders. This is data about orders which didn't fit in available requests quantity so were saved. They 
  contain client and ordered products data.

### Token
You need store OAuth token, you can do it here https://developers.printful.com/tokens/add-new-token. You can make token 
with full access, then everything will work fine, or you can make token with selective access. You need access to view 
store products, view and manage orders

### Products
This project is for a limited type products, its tests with hoodies, sweatshirts, T-shirts, pants, shorts, and more. 
Project worked with clothes below or above the belt and also tested the same types of products with a print on the 
entire product. Project behavior with other product types is unpredictable. Perhaps the list of available product types 
will be increased