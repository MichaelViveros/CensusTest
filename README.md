# CensusTest
CensusTest takes census data from the Canadian government and lets users answer simple questions to see how they compare to other Canadians.

It is implemented in Python as a Django web application which uses PostgreSQL as a database.

* `mysite` is the project folder which defines the settings for CensusTest and how the server is run
* `censustest` is the application folder which contains the bulk of the code for CensusTest including HTML templates, business logic and database migrations

It also uses the [chartit](https://djangopackages.org/packages/p/django-chartit/) Django package which uses [Highcharts](http://www.highcharts.com/) to create charts.

CensusTest gets it's data from the [2011 Census Profile](http://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/details/page.cfm?Lang=E&Geo1=PR&Code1=01&Geo2=PR&Code2=01&Data=Count&SearchText=Canada&SearchType=Begins&SearchPR=01&B1=All&Custom=&TABID=1) and the [2011 National Household Survey Profile](http://www12.statcan.gc.ca/nhs-enm/2011/dp-pd/prof/details/page.cfm?Lang=E&Geo1=PR&Code1=01&Data=Count&SearchText=Canada&SearchType=Begins&SearchPR=01&A1=All&B1=All&Custom=&TABID=1) which are publicly available from the Canadian government on the [Statistics Canada](http://www12.statcan.gc.ca/census-recensement/2011/dp-pd/index-eng.cfm) website.
