import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
# import os
# from dotenv import load_dotenv
# load_dotenv()
# postgres_password = os.getenv("postgres_password")

from models import create_tables, Publisher, Book, Stock, Shop, Sale

DSN = "postgresql://postgres:postgres_password@localhost:5432/books"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

publisher_id = int(input("Введите ID издателя(автора): "))
data = session.query(Book.title, Shop.name, Sale.count * Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.id == publisher_id ).all()
for book in data:
    print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]}")

session.close()

