#!/usr/bin/env python3

from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Dev, Company, Freebie

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()

    fake = Faker()

    devs = []
    for i in range(25):
        dev = Dev(
            name = fake.unique.name()
        )
        session.add(dev)
        session.commit()
        devs.append(dev)

    companies = []
    for i in range(10):
        company = Company(
            name = fake.unique.name(),
            founding_year = fake.date_between('-30y', 'today')
        )
        session.add(company)
        session.commit()
        companies.append(company)

    freebies = []
    for i in range(10):
        random_company = random.choice(companies)
        random_dev = random.choice(devs)
        freebie = Freebie(
            item_name = fake.unique.name(),
            value = random.randint(0, 100),
            company = random_company,
            dev = random_dev
        )
        session.add(freebie)
        session.commit()
    session.close()
