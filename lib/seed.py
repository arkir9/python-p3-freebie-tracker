#!/usr/bin/env python3

# Script goes here!
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from models import Base, Company, Dev, Freebie


fake = Faker()


engine = create_engine('sqlite:///db/companies_devs.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


companies = [Company(name=fake.company(), founding_year=fake.year()) for _ in range(5)]
session.add_all(companies)
session.commit()


devs = [Dev(name=fake.name()) for _ in range(10)]
session.add_all(devs)
session.commit()


freebies = [
    Freebie(
        item_name=fake.word(),
        value=fake.random_int(min=1, max=1000),
        dev=fake.random_element(elements=devs),
        company=fake.random_element(elements=companies)
    ) for _ in range(20)
]
session.add_all(freebies)
session.commit()

