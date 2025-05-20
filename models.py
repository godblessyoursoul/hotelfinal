from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from db import Base, Session


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    streets = relationship("Street", back_populates="city")


class Street(Base):
    __tablename__ = 'streets'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    house_number = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"))

    city = relationship("City", back_populates="streets")
    clients = relationship("Client", back_populates="address")


class Passport(Base):
    __tablename__ = 'passports'

    id = Column(Integer, primary_key=True)
    series = Column(String, nullable=False)
    number = Column(String, nullable=False)
    issue_date = Column(Date, nullable=False)
    issued_by = Column(String, nullable=False)

    clients = relationship("Client", back_populates="passport")


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    middle_name = Column(String)
    birth_date = Column(Date, nullable=False)
    phone_number = Column(String, nullable=False)
    arrival_date = Column(Date, nullable=False)
    departure_date = Column(Date, nullable=False)

    passport_id = Column(Integer, ForeignKey("passports.id"))
    address_id = Column(Integer, ForeignKey("streets.id"))

    passport = relationship("Passport", back_populates="clients")
    address = relationship("Street", back_populates="clients")
    bookings = relationship("Booking", back_populates="client")


class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    booking_services = relationship("BookingService", back_populates="service")


class Price(Base):
    __tablename__ = 'price_list'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)

    booking_prices = relationship("BookingPrice", back_populates="price")


class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    room_category = Column(String, nullable=False)
    departure_date = Column(Date, nullable=False)

    client = relationship("Client", back_populates="bookings")
    booking_services = relationship("BookingService", back_populates="booking")
    booking_prices = relationship("BookingPrice", back_populates="booking")


class BookingService(Base):
    __tablename__ = 'booking_services'

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    service_id = Column(Integer, ForeignKey("services.id"))

    booking = relationship("Booking", back_populates="booking_services")
    service = relationship("Service", back_populates="booking_services")


class BookingPrice(Base):
    __tablename__ = 'booking_prices'

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    price_id = Column(Integer, ForeignKey("price_list.id"))

    booking = relationship("Booking", back_populates="booking_prices")
    price = relationship("Price", back_populates="booking_prices")
