import pandas as pd
import datetime
from mimesis import Generic
import random
import numpy as np

products_head = ['ID', 'Name', 'Price', 'Unit Cost', 'Manufacturer']
customers_head = ['id', 'Name', 'Address', 'City', 'Country', 'Website', 'Email', 'Phone', 'Registration Date']
staff_head = ['id', 'Name', 'Title', 'Address', 'Contract Date', 'Telephone', 'Email', 'Termination Date', 'Office', 'Salary']
sales_head = ['Tx Id', 'Customer id', 'Product ID', 'Sales Date', 'Sales Manager', 'Point of Sales', 'Quantity', 'Total Price']

def main():
    generate_products(340)
    generate_staff(400)
    generate_customers(4000)
    generate_sales('./products.csv', './customers.csv', './employees.csv', 100000)


def generate_customers(n):

    ### Initialize timer, mimesis-class and dataframe
    begin_timer = datetime.datetime.now()
    gen = Generic('en')
    df = pd.DataFrame(columns=customers_head)

    ### Generate information for n customers and add them into dataframe
    for i in range(n):
        id = 21000 + i
        name = gen.business.company()
        address = gen.address.address()
        city = gen.address.city()
        country = gen.address.country()
        web = gen.internet.home_page()
        email = gen.person.email()
        phone = gen.person.telephone()
        registered = gen.datetime.datetime()
        df.loc[i] = [id, name, address, city, country, web, email, phone, registered]

    print(f'Generated customer-table in {datetime.datetime.now() - begin_timer}\n')
    df.to_csv('./customers.csv', index=False)

def generate_products(n):

    ### Initialize timer, mimesis-class and dataframe
    begin_timer = datetime.datetime.now()
    gen = Generic('en')
    df = pd.DataFrame(columns=products_head)

    ### Generate information for n products and add them into dataframe
    for i in range(n):
        if i % 4 == 0:
            name = gen.hardware.graphics()
        if i % 5 == 0:
            name = gen.hardware.cpu()
        else:
            name = gen.hardware.phone_model()
        id = name[:3].upper() + str(gen.numbers.integer_number(300,900))
        price = gen.random.uniform(200,1040, 2)
        unit_cost = round(gen.random.uniform(0.2,0.95,2) * price, 2)
        manufacturer = name.split(' ')[0]

        df.loc[i] = [id, name, price, unit_cost, manufacturer]
    print(f'Generated product-table in {datetime.datetime.now() - begin_timer}\n')
    df.to_csv('./products.csv', index=False)

def generate_staff(n):
    
    ### Initialize timer, mimesis-class and dataframe
    begin_timer = datetime.datetime.now()
    gen = Generic('en')
    df = pd.DataFrame(columns=staff_head)

    ### Generate information for n employees and add them into dataframe
    for i in range(n):
        name = gen.person.full_name()
        title = gen.person.occupation()
        address = gen.address.address()
        phone = gen.person.telephone()
        office = gen.address.continent()
        contract_date = gen.datetime.date(2012, 2021)
        email = gen.person.email()
        salary = int(np.random.normal(loc=3200, scale=1000))

        if i % 4 == 0: # Lazy way to insert expired contracts into the data
            contract_len = datetime.timedelta(random.randint(120,900))
            termination_date = contract_date + contract_len
        else:
            termination_date = np.nan
        
        df.loc[i] = [i, name, title, address, contract_date, phone, email, termination_date, office, salary]
    
    print(f'Generated staff-table in {datetime.datetime.now() - begin_timer}\n')
    df.to_csv('./employees.csv', index=False)

def generate_sales(products, customers, staff, n):
    begin_timer = datetime.datetime.now()
    
    ### Reduce input tables to numpy arrays to make sampling faster 
    df = pd.DataFrame(columns=sales_head)
    cust = pd.read_csv(customers).id.values
    prod = pd.read_csv(products).values
    staff = pd.read_csv(staff).id.values
    gen = Generic('en')
    
    ### Select random customers, products and employees and generate sales events for them 
    for i in range(n):
        cust_id = cust[np.random.choice(cust.shape[0])]
        product = prod[np.random.choice(prod.shape[0])]
        sales_person_id = staff[np.random.choice(staff.shape[0])]
        sales_date = gen.datetime.datetime(2012, 2021)
        pos = random.choice(['Webstore', 'Wholesale', 'Flagship', 'Reseller'])
        qty = np.random.randint(6, 400)
        total_price = qty * product[2]
        df.loc[i] = [i, cust_id, product[0], sales_date, sales_person_id, pos, qty, total_price]
    
    print(f'Generated sales-table in {datetime.datetime.now() - begin_timer}\n')
    df.to_csv('./sales.csv', index=False)

main()