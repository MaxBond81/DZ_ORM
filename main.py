
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Stock, Shop, Sale

DSN = "postgresql://postgres:postgres@localhost:5432/books"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()

def getshops(author):
    data = session.query(Book.title, Shop.name, Sale.count * Sale.price, Sale.date_sale).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)

    if author.isdigit():
        result = data.filter(Publisher.id == author).all()
    else:
        result = data.filter(Publisher.name == author).all()
    for title_book, name_shop, count_sale, date_sale in result:
        print(f"{title_book: <40} | {name_shop: <10} | {count_sale: <8} | {date_sale.strftime('%d-%m-%Y')}")

if __name__ == '__main__':

    author = input("Введите имя или айди автора: ")
    getshops(author)

