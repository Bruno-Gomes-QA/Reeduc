from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel

Base = declarative_base()
metadata = Base.metadata

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    department = relationship("Department")
    price = Column(Float, nullable=False)
    created = Column(DateTime, nullable=False, default=func.now())
    updated = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'department_id': self.department_id,
            'department': self.department,
            'price': self.name,
            'created': self.created,
            'updated': self.updated
        }


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship("Product")
    quantity = Column(Integer, nullable=False)
    location = Column(String(255), nullable=False)
    entry_date = Column(DateTime, nullable=False, default=func.now())

class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    status = Column(Integer, default=0)
    sale_date = Column(DateTime, nullable=False, default=func.now())

class SaleItem(Base):
    __tablename__ = 'sale_items'

    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey('sales.id'), nullable=False)
    sale = relationship("Sale")
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship("Product")
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)


class ProductModel(BaseModel):
    name: str
    department_id: int
    price: float