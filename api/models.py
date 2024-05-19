# coding: utf-8
from sqlalchemy import (
    Column,
    DECIMAL,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
    Table,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    account_type = Column(String(255))
    account_name = Column(String(255))
    account_description = Column(String(1000))
    balance = Column(DECIMAL(10, 2))
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
    )

    def serialize(self):
        return {
            'id': self.id,
            'account_type': self.account_type,
            'account_name': self.account_name,
            'account_description': self.account_description,
            'balance': float(self.balance),
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(1000))
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
    )

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


class MovType(Base):
    __tablename__ = 'mov_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(1000))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }


class PeopleType(Base):
    __tablename__ = 'people_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
    )

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(1000))
    tel = Column(String(255))
    password = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
    )

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'tel': self.tel,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    table_name = Column(String(255))
    operation_type = Column(String(255))
    old_value = Column(String(1000))
    new_value = Column(String(1000))
    user_id = Column(ForeignKey('users.id', ondelete='RESTRICT'))

    user = relationship('User')

    def serialize(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'table_name': self.table_name,
            'operation_type': self.operation_type,
            'old_value': self.old_value,
            'new_value': self.new_value,
            'user_id': self.user_id,
        }


class People(Base):
    __tablename__ = 'peoples'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(1000))
    tel = Column(String(30))
    cpf = Column(String(16))
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
    )
    status = Column(Integer)
    people_type_id = Column(ForeignKey('people_types.id', ondelete='SET NULL'))

    people_type = relationship('PeopleType')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'tel': self.tel,
            'cpf': self.cpf,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'people_type_id': self.people_type_id,
        }


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    product_name = Column(String(255))
    product_description = Column(String(1000))
    buy_price = Column(DECIMAL(10, 2))
    sale_price = Column(DECIMAL(10, 2))
    stock = Column(DECIMAL(10, 2))
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
    )
    department_id = Column(ForeignKey('departments.id', ondelete='SET NULL'))

    department = relationship('Department')

    def serialize(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'product_description': self.product_description,
            'buy_price': float(self.buy_price),
            'sale_price': float(self.sale_price),
            'stock': float(self.stock),
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'department_id': self.department_id,
        }


class MovProduct(Base):
    __tablename__ = 'mov_products'

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
    )
    status = Column(Integer)
    mov_type_id = Column(ForeignKey('mov_types.id', ondelete='SET NULL'))
    product_id = Column(ForeignKey('products.id', ondelete='SET NULL'))
    people_id = Column(ForeignKey('peoples.id', ondelete='SET NULL'))
    user_id = Column(ForeignKey('users.id', ondelete='SET NULL'))

    mov_type = relationship('MovType')
    people = relationship('People')
    product = relationship('Product')
    user = relationship('User')

    def serialize(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'status': self.status,
            'mov_type_id': self.mov_type_id,
            'product_id': self.product_id,
            'people_id': self.people_id,
            'user_id': self.user_id,
        }


class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True)
    description = Column(String(1000))
    purchase_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    status = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
    )
    people_id = Column(ForeignKey('peoples.id', ondelete='SET NULL'))

    people = relationship('People')

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'purchase_date': self.purchase_date,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'people_id': self.people_id,
        }


class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    sale_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
    )
    description = Column(String(1000))
    status = Column(Integer)
    people_id = Column(ForeignKey('peoples.id', ondelete='SET NULL'))

    people = relationship('People')

    def serialize(self):
        return {
            'id': self.id,
            'sale_date': self.sale_date,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'people_id': self.people_id,
        }


class AccountsPayable(Base):
    __tablename__ = 'accounts_payables'

    id = Column(Integer, primary_key=True)
    due_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    amount = Column(DECIMAL(10, 2))
    description = Column(String(1000))
    status = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
    )
    purchase_id = Column(ForeignKey('purchases.id', ondelete='SET NULL'))
    account_id = Column(ForeignKey('accounts.id', ondelete='SET NULL'))
    people_id = Column(ForeignKey('peoples.id', ondelete='SET NULL'))

    account = relationship('Account')
    purchase = relationship('Purchase')
    people = relationship('People')

    def serialize(self):
        return {
            'id': self.id,
            'due_date': self.due_date,
            'amount': float(self.amount),
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'purchase_id': self.purchase_id,
            'account_id': self.account_id,
        }


class AccountsReceivable(Base):
    __tablename__ = 'accounts_receivables'

    id = Column(Integer, primary_key=True)
    description = Column(String(1000))
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    status = Column(Integer)
    due_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
    )
    amount = Column(DECIMAL(10, 2))
    sale_id = Column(ForeignKey('sales.id', ondelete='SET NULL'))
    account_id = Column(ForeignKey('accounts.id', ondelete='SET NULL'))
    people_id = Column(ForeignKey('peoples.id', ondelete='SET NULL'))

    account = relationship('Account')
    sale = relationship('Sale')
    people = relationship('People')

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'created_at': self.created_at,
            'status': self.status,
            'due_date': self.due_date,
            'updated_at': self.updated_at,
            'amount': float(self.amount),
            'sale_id': self.sale_id,
            'account_id': self.account_id,
        }


t_product_mov_purchase = Table(
    'product_mov_purchase',
    metadata,
    Column(
        'mov_product_id', ForeignKey('mov_products.id', ondelete='RESTRICT')
    ),
    Column('purchase_id', ForeignKey('purchases.id', ondelete='SET NULL')),
)


t_product_mov_sale = Table(
    'product_mov_sale',
    metadata,
    Column(
        'mov_product_id', ForeignKey('mov_products.id', ondelete='RESTRICT')
    ),
    Column('sale_id', ForeignKey('sales.id', ondelete='SET NULL')),
)
