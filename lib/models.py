from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy


convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind = engine)
session = Session()

class Company(Base):
    __tablename__ = 'companies'

    

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship('Freebie', back_populates='company', cascade='all, delete-orphan')
    devs = association_proxy('freebies', 'dev', creator=lambda de: Freebie(dev=de))

    session = None


    def __repr__(self):
        return f'<Company {self.name}>'
    
    def give_freebie(self, dev, item_name, value):
        new_freebie = Freebie(
            item_name=item_name,
            value=value,
            company = self,
            dev=dev
        )
        session.add(new_freebie)
        session.commit()

    @classmethod
    def oldest_company(cls):
        return session.query(cls).order_by(cls.founding_year).first()
    


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    freebies = relationship('Freebie', back_populates='dev')
    companies = association_proxy('freebies', 'company', creator=lambda co: Freebie(company=co))

    def __repr__(self):
        return f'<Dev {self.name}>'
    
    def received_one(self, item_name):
        for fb in self.freebies:
            if fb.item_name == item_name:
                return True
        return False
    
    def give_away(self, dev, freebie):
        if self.received_one(freebie.item_name):
            freebie.dev = dev
            session.add(freebie)
            session.commit()
            return f'{self.name} gave {freebie.id} to {dev.name}'
        return 'I don\'t have that freebie!'
    
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))

    company = relationship('Company', back_populates='freebies')
    dev = relationship('Dev', back_populates='freebies')

    def __repr__(self):
        return f'<Freebie {self.id}>'

    def print_details(self):
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}'
    
