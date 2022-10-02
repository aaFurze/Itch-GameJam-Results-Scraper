# Itch-GameJam-Results-Scraper
### A Program that scrapes aggregated data on results/rating figures from an itch.io GameJam. (See data folder for example csv files).

# Contents

###  * What this WebScraper does
###  * What this WebScraper does not do
###  * Pre-requisites/Requirements to use the WebScraper
###  * Using the WebScraper
###  * Some Edge cases and problems that can arise

  
  
   
<br/><br/><br/>

# What This WebScraper Does
This webscraper: 
- Provides a basic console interface to run the scraper from start to finish.
- When given a url for a itch.io GameJam's (first) results page, asynchronously retrives submission data for the first n submissions to the jam. This data includes submission:
  - Title
  - Author
  - Number of Ratings recieved
  - Final Ranking, Score and Raw Score it recieved in each category that the GameJam uses.
- Saves results in a .csv file.
- Provides basic cleaning of the GameJams category names (.csv file column names are lowercase + "-", "/", "_" only)
<br/><br/>

# What This WebScraper Does Not Do
This Webscraper does not:
- Retrieve results from non-ranked GameJams.
- Retrieve results from GameJams that are ongoing.
- Retrieve results from non-itch.io GameJams.
- Retrieve data on comments or individual ratings given to a particular game.
- Retrive or combine data from multiple GameJams into one file.
- Provide additional cleaning to the actual data.
- Save in file formats other than .csv (e.g. .json .xlsx)
- Analyse of Data retrieved.
<br/><br/>

# Pre-requisites/Requirements to use the WebScraper.

- Python version 3.6+ (Program originally written using Python 3.10.6 interpreter)
- A standard Command line/prompt or Console (for setting up and running the program)

### Setting up the Virtual Environment
It is good practice to create a virtual environment for this project (and for any other project with non-standard-library dependencies).
See this guide for how to setup and activate a virtual environment: [Python docs](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment "Python docs")

NOTE: Ensure that you activate the environment once you have created it.

To install the relevant packages, select the directory that requirements.txt is in and run the following command:
```
pip install -r requirements.txt
```

To check that all the packages have been installed, run the following command:
```
pip list
```
This should produce an output that looks contains these items
```
anyio           3.6.1
beautifulsoup4  4.11.1
bs4             0.0.1
certifi         2022.9.14
h11             0.12.0
httpcore        0.15.0
httpx           0.23.0
idna            3.4
lxml            4.9.1
numpy           1.23.3
pandas          1.5.0
python-dateutil 2.8.2
pytz            2022.2.1
rfc3986         1.5.0
six             1.16.0
sniffio         1.3.0
soupsieve       2.3.2.post1
```

If all of these commands were executed successfully, you can now use the Scraper.

<br/>
<br/>

# Using the WebScraper
To run the scraper from a command line, open your command line/terminal of choice and navigate to the directory containing the project.

Run the following command to start the program:
NOTE: Replace "python" with "python3" if you have python version 2 and 3 installed on your computer.
```
python main.py
```
<br/>
<br/>

You will be met with the following prompt:
```
Enter the base url of the GameJam you would like to scrape score data for. e.g. https://itch.io/jam/kenney-jam-2022/results  

```
Copy in or manually type out the url of the GameJam results you want to retrieve data for.
- NOTE: Ensure that the url matches the desired format. It must:
 - Be a valid url: "https://_______.com"
 - Be an itch.io Jam page: "itch.io/jam"
 - Link to the results page of the Jam at the end of the url: "/results"

<br/>
<br/>

Next, you will be met with the following prompt:
```
Enter the maximum number of results you would like to retrieve (default value = 2000): 

```
Enter either a whole number (e.g. 620) to the maximum number of results retrieved, or nothing to set it to the default value.
- NOTE: The number of submissions actually retrived will be a multiple of 20 (rounded down).
- NOTE: Entering a number below 20 will set the maximum number of results retrived to 20.

<br/>
<br/>

Finally, you will be met with the following prompt:
```
Enter what you want to save the file as. (Do not include .csv at the end):

```
Enter what you want to save the results as. A .csv file will created by the program in the /data folder.
- NOTE: Invalid characters (non-numbers, letters or "-" "_") will be removed automatically. Spaces will be converted into "-" characters.

<br/>
<br/>
<br/>

Once you have entered the file's save name, the program will start running.
The current status of the program will be printed to the console as it runs.
The program will typically run for a few seconds, although it could run for longer depending on the number of submissions retrieved, the specifications of your computer, and the quality of your internet connection.
Once the program has successfully run, it will print the following statements:
```
Saving results...
Execution Successful.
```

You should now be able to access your data in the /data folder.


<br/>
<br/>
<br/>



Thank you for using my WebScraper.
If you have find any problems with the WebScraper, please log them as a [GitHub issue](https://github.com/aaFurze/Itch-GameJam-Results-Scraper/issues "GitHub Issues link").


<br/>
<br/>
<br/>

Last tested: 28th September, 2022  
URLs tested on:  
  https://itch.io/jam/gmtk-jam-2022/results   
  https://itch.io/jam/wowie-jam-4/results  
  https://itch.io/jam/game-off-2017  
  https://itch.io/jam/kenney-jam-2022  
  https://itch.io/jam/brackeys-5/results  
