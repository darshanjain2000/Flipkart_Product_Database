# Flipkart_Product_Database
In this project, I've recreated the Flipkart search box. When the user searches for a product/category in the box:-

-First, the program scrapes all products displayed on the first page of the results using BeautifulSoup and takes out relevant information.

-Each product has a link which directs to it's product page. The program then opens each link and scrapes reviews for each product.(BeautifulSoup)

-The data is stored in a SQL Database using sqllite3 (Here by the name of FLIPKART).

-The program fetches data from the database and the user is able to traverse through the data using the UI built from Tkinter.

-Data Analysis is performed using Seaborn
