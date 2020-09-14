###### Parsing tools

Simple tools created to parse csv and xlsx files:

Before use:
    pip install -r requirements.txt
    
Used libraries:

    - Pandas
    - XlsxWriter
    
orders.csv is disordered csv file with with orders for different brands

    The result of use to_xlsx_parser_orders are separated xlsx files
     for every brand for future orders
     
permissions.xlsx consist of two sheets: stores and users

    The result of used to_csv_parser_users_stores is csv file
    for all users and their permissions to stores depending on 
    various conditions(Region, Country, Stream, Channel) 