from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, create_engine
from sqlalchemy.orm import relationship, backref , sessionmaker
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)
engine = create_engine('sqlite:///db/companies_devs.db', echo=True)
Session = sessionmaker(bind=engine)

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String())
    value = Column(Integer)
    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    dev = relationship("Dev", back_populates="freebies")
    company = relationship("Company", back_populates="freebies")

    def dev(self):
        return self.dev

    def company(self):
        return self.company

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}."


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    founding_year = Column(Integer)

    freebies = relationship("Freebie", back_populates="company")

    def freebies(self):
        return self.freebies

    def devs(self):
        return [freebie.dev for freebie in self.freebies]

    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(dev=dev, company=self, item_name=item_name, value=value)
        return freebie

    @classmethod
    def oldest_company(cls):
        return min(cls.query.all(), key=lambda company: company.founding_year)


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String())

    freebies = relationship("Freebie", back_populates="dev")

    def freebies(self):
        return self.freebies

    def companies(self):
        return [freebie.company for freebie in self.freebies]

    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        if freebie.dev == self:
            freebie.dev = dev


Base.metadata.create_all(engine)