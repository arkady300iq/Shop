import sqlite3
db = sqlite3.connect('shop.db')

db.execute('''CREATE TABLE  IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL);''')

db.execute('''CREATE TABLE IF NOT EXISTS customers ( 
    customer_id INTEGER PRIMARY KEY, 
    first_name TEXT NOT NULL, 
    last_name TEXT NOT NULL, 
    email TEXT NOT NULL UNIQUE);''')

db.execute('''CREATE TABLE IF NOT EXISTS orders ( 
    order_id INTEGER PRIMARY KEY, 
    customer_id INTEGER NOT NULL, 
    product_id INTEGER NOT NULL, 
    quantity INTEGER NOT NULL, 
    order_date DATE NOT NULL, 
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id), 
    FOREIGN KEY (product_id) REFERENCES products(product_id));''')


def add_product(db, name, category, price):
    db.execute(f'''INSERT INTO products(name, category, price) 
               VALUES(?, ?, ?)''', (name, category, price))
    db.commit()

def add_customers(db, first_name, last_name, email):
     db.execute(f'''INSERT INTO customers(first_name, last_name, email)
                VALUES(?, ?, ?)''', (first_name, last_name, email))
     db.commit()

def make_order(db, customer_id, product_id, quantity, order_date):
     db.execute(f'''INSERT INTO orders(customer_id, product_id, quantity, order_date)
                VALUES(?, ?, ?, ?)''', (customer_id, product_id, quantity, order_date))
     db.commit()

def total_sales(db):
     cursor = db.execute(f'''SELECT SUM(products.price * orders.quantity) AS total_quantity
                FROM orders 
                JOIN products ON products.product_id = orders.product_id''')
     return cursor.fetchone()[0]

def customers_orders(db):
     cursor = db.execute(f'''SELECT customers.first_name, customers.last_name, COUNT(orders.order_id) AS order_count
                         FROM customers
                         JOIN orders ON customers.customer_id = orders.customer_id
                         GROUP BY customers.customer_id''')
     return cursor.fetchall()

def average_orders(db):
     cursor = db.execute(f'''SELECT AVG(products.price * orders.quantity) AS average_order
                         FROM orders
                         JOIN products ON products.product_id = orders.product_id''')
     return cursor.fetchone()[0]

def most_popular_category(db):
     cursor = db.execute('''SELECT products.category, COUNT(orders.order_id) AS order_count
                           FROM orders 
                           JOIN products ON orders.product_id = products.product_id
                           GROUP BY products.category
                           ORDER BY order_count DESC
                           LIMIT 1''')
     popular_category = cursor.fetchone()
     return popular_category if popular_category else ("None", 0)
    
def total_products_per_category(db):
    cursor = db.execute('''SELECT category, COUNT(*) AS product_count 
                           FROM products 
                           GROUP BY category''')
    return cursor.fetchall()

def update_prices(db, category, percentage):
    db.execute ('''UPDATE products
               SET price = price * (1 + ? / 100)
               WHERE category = ?''', (category, percentage))
    db.commit()


while True:
        print('''
Що ви хочете зробити?

1 - Додавання продуктів:
2 - Додавання клієнтів:
3 - Замовлення товарів:
4 - Сумарний обсяг продажів:
5 - Кількість замовлень на кожного клієнта:
6 - Середній чек замовлення:
7 - Найбільш популярна категорія товарів:
8 - Загальна кількість товарів кожної категорії:
9 - Оновлення цін категорії на 10% більші:
0 - Вийти:
              
        ''')
        choice = int(input("Виберіть опцію от 1 до 12:"))

        if choice == 1:
            name = input('Name:')
            category = input('Category:')
            price = int(input('Price:'))
            add_product(db, name, category, price)
            print(f'Product {name} added successfully')
        
        if choice == 2:
             first_name = input('First name:')
             last_name = input('Last name:')
             email = input('Email:')
             add_customers(db, first_name, last_name, email)
             print(f'customer {first_name} added successfully')

        if choice == 3:
             customer_id = int(input('Customer id:'))
             product_id = int(input('Product id'))
             quantity = int(input('Quantity:'))
             order_date = int(input('Order date:'))
             make_order(db, customer_id, product_id, quantity, order_date)
             print(f'Order {customer_id} added successfully')

        if choice == 4:
            total = total_sales(db)
            print(f'Total sales: {total}')

        if choice == 5:
            orders = customers_orders(db)
            for order in orders:
                print(f'{order[0]} {order[1]}: {order[2]} orders')
        
        if choice == 6:
             average = average_orders(db)
             print(f'Average orders values: {average}')
        
        if choice == 7:
            category = most_popular_category(db)
            print(f'Most popular category: {category[0]} with {category[1]} orders')
                    
        if choice == 8:
            totals = total_products_per_category(db)
            for total in totals:
                print(f'{total[0]}: {total[1]} products')

        if choice == 9:
            update_prices(db, 'smartphones', 10)
            print('Prices updated successfully')

        if choice == 0:
             break



    
             
            

        