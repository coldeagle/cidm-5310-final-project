# SQL Alchemy ORM file that creates the database tables
from sqlalchemy import Column, Integer, MetaData, String, Table, Float, Date, UnicodeText, ForeignKey
from sqlalchemy.orm import registry
from models.models import Airline, AirlineQuarterlyNums, Airport, ConnectingMarketFareInfo, Market, MarketFares, MishandledItemsInfo, MishandledPassengerInfo, LastDone

metadata = MetaData()

mapper_registry = registry()


airline_items_mishandles = Table(
    'airline_items_mishandles',
    mapper_registry.metadata,
    Column('Id', UnicodeText(255), primary_key=True, unique=True),
    Column('AirlineCode', String(255), ForeignKey('airlines.Code')),
    Column('MishandledBags', Integer),
    Column('MishandledChairs', Integer),
    Column('Month', Integer),
    Column('Quarter', Integer),
    Column('TotalBags', Integer),
    Column('TotalChairs', Integer),
    Column('Year', Integer),
)

airline_passenger_mishandles = Table(
    'airline_passenger_mishandles',
    mapper_registry.metadata,
    Column('Id', UnicodeText(255), primary_key=True, unique=True),
    Column('CompPaid', Integer),
    Column('MktAirlineCode', String(255), ForeignKey('airlines.Code')),
    Column('Month', Integer),
    Column('NumComp', Integer),
    Column('NumDowngraded', Integer),
    Column('NumUpgraded', Integer),
    Column('OpAirlineCode', String(255), ForeignKey('airlines.Code')),
    Column('Quarter', Integer),
    Column('TotalBoarding', Integer),
    Column('TotalDenied', Integer),
    Column('Year', Integer),
)

airline_quarterly_numbers = Table(
    'airline_quarterly_numbers',
    mapper_registry.metadata,
    Column('Id', UnicodeText(255), primary_key=True, unique=True),
    Column('Carrier', String(255), ForeignKey('airlines.Code')),
    Column('ItemName', String(255)),
    Column('Quarter', Integer),
    Column('Value', Float),
    Column('Year', Integer),
)

airlines = Table(
    'airlines',
    mapper_registry.metadata,
    Column('Id', Integer, primary_key=True, unique=True),
    Column('Code', String(255), unique=True),
    Column('Name', String(255)),
    Column('UniqueName', String(255), unique=True),
)

airports = Table(
    'airports',
    mapper_registry.metadata,
    Column('Id', Integer, primary_key=True, unique=True),
    Column('Code', String(255), unique=True),
    Column('CityId', Integer, ForeignKey('markets.Id')),
)

connecting_market_fare_info = Table(
    'connecting_market_fare_info',
    mapper_registry.metadata,
    Column('Id', UnicodeText(255), primary_key=True, unique=True),
    Column('Carrier', String(255), ForeignKey('airlines.Code')),
    Column('City1', Integer, ForeignKey('markets.Id')),
    Column('City2', Integer, ForeignKey('markets.Id')),
    Column('Fare', Float),
    #Column('FareLow', Float),
    Column('CarrierAvgFare', Float),
    Column('CarrierPassengerShare', Float),
    Column('Quarter', Integer),
    Column('Year', Integer),
)

connecting_market_fare_info_MultiCarrier = Table(
    'connecting_market_fare_info_MultiCarrier',
    mapper_registry.metadata,
    Column('Id', UnicodeText(255), primary_key=True, unique=True),
    Column('CarrierLg', String(255), ForeignKey('airlines.Code')),
    Column('CarrierLow', String(255), ForeignKey('airlines.Code')),
    Column('City1', Integer, ForeignKey('markets.Id')),
    Column('City2', Integer, ForeignKey('markets.Id')),
    Column('Fare', Float),
    Column('FareLow', Float),
    Column('LfMs', Float),
    Column('NumPassengers', Float),
    Column('NsMiles', Integer),
    Column('Quarter', Integer),
    Column('Year', Integer),
)

markets = Table(
    'markets',
    mapper_registry.metadata,
    Column('Id', Integer, primary_key=True, unique=True),
    Column('Name', String(255), unique=False),
)

market_fares = Table(
    'market_fares',
    mapper_registry.metadata,
    Column('Id', UnicodeText(255), primary_key=True, unique=True),
    Column('AirportId', Integer, ForeignKey('airports.Id')),
    Column('CityId', Integer, ForeignKey('markets.Id')),
    Column('TotalAvgHubFare', Float),
    Column('TotalFaredPas', Integer),
    Column('TotalMkts', Integer),
    Column('TotalPerLowFare', Float),
    Column('TotalPerPremium', Float),
    Column('Quarter', Integer),
    Column('Year', Integer),
)

last_done = Table(
    'last_done',
    mapper_registry.metadata,
    Column('LastUpdated', Date)
)


def start_mappers():
    mapper_registry.map_imperatively(MishandledItemsInfo, airline_items_mishandles)
    mapper_registry.map_imperatively(MishandledPassengerInfo, airline_passenger_mishandles)
    mapper_registry.map_imperatively(AirlineQuarterlyNums, airline_quarterly_numbers)
    mapper_registry.map_imperatively(Airline, airlines)
    mapper_registry.map_imperatively(Airport, airports)
    mapper_registry.map_imperatively(ConnectingMarketFareInfo, connecting_market_fare_info)
    mapper_registry.map_imperatively(Market, markets)
    mapper_registry.map_imperatively(MarketFares, market_fares)
    mapper_registry.map_imperatively(LastDone, last_done)


