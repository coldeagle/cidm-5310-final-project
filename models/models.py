# Contains the base models for the ORM to use for construction

from datetime import date
from typing import Optional
from dataclasses import dataclass


@dataclass
class Airline:
    Id: int
    Code: str
    Name: str
    UniqueName: str

    def __init__(
            self,
            id: int,
            code: str,
            name: str,
            unique_name
    ):
        self.Id = id
        self.Code = code
        self.Name = name
        self.UniqueName = unique_name


@dataclass
class AirlineQuarterlyNums:
    Id: str
    Carrier: str
    ItemName: str
    Quarter: int
    Value: float
    Year: int

    def __init__(
            self,
            id: Optional[str],
            carrier: str,
            item_name: str,
            quarter: int,
            value: float,
            year: int
    ):
        self.Id = f'{year}-{quarter}-{carrier}-{item_name}' if id is None else id
        self.Carrier = carrier
        self.ItemName = item_name
        self.Quarter = quarter
        self.Value = value
        self.Year = year


@dataclass
class Airport:
    Id: int
    Code: str
    CityId: int

    def __init__(
            self,
            id: int,
            code: str,
            city_id: int,
    ):
        self.Id = id
        self.Code = code
        self.CityId = city_id


@dataclass
class ConnectingMarketFareInfo:
    Id: str
    Carrier: str
    City1: int
    City2: int
    Fare: float
    #FareLow: float
    CarrierAvgFare: float
    CarrierPassengerShare: float
    Quarter: int
    Year: int

    def __init__(
            self,
            id: Optional[str],
            carrier: str,
            city_1: int,
            city_2: int,
            fare: float,
            car_avg_fare: float,
            car_passenger_share: float,
            quarter: int,
            year: int,
    ):
        self.Id = f'{year}-{quarter}-{city_1}-{city_2}-{carrier}' if id is None else id
        self.Carrier = carrier
        self.City1 = city_1
        self.City2 = city_2
        self.Fare = fare
        self.CarrierAvgFare = car_avg_fare
        self.CarrierPassengerShare = car_passenger_share
        self.Quarter = quarter
        self.Year = year


@dataclass
class ConnectingMarketFareInfoMultiCarrier:
    Id: str
    CarrierLg: str
    CarrierLow: str
    City1: int
    City2: int
    Fare: float
    FareLow: float
    LfMs: float
    NumPassengers: float
    NsMiles: int
    Quarter: int
    Year: int

    def __init__(
            self,
            id: Optional[str],
            carrier_lg: str,
            carrier_low: str,
            city_1: int,
            city_2: int,
            fare: float,
            fare_low: float,
            lf_ms: float,
            num_passengers: float,
            ns_miles: int,
            quarter: int,
            year: int,
    ):
        self.Id = f'{year}-{quarter}-{city_1}-{city_2}' if id is None else id
        self.CarrierLg = carrier_lg
        self.CarrierLow = carrier_low
        self.City1 = city_1
        self.City2 = city_2
        self.Fare = fare
        self.FareLow = fare_low
        self.LfMs = lf_ms
        self.NumPassengers = num_passengers
        self.NsMiles = ns_miles
        self.Quarter = quarter
        self.Year = year


@dataclass
class Market:
    Id: int
    Name: str

    def __init__(
            self,
            id: int,
            name: str
    ):
        self.Id = id
        self.Name = name


@dataclass
class MarketFares:
    Id: str
    AirportId: int
    CityId: int
    Quarter: int
    TotalAvgHubFare: float
    TotalFaredPas: int
    TotalMkts: int
    TotalPerLowFare: float
    TotalPerPremium: float
    Year: int

    def __init__(
            self,
            id: Optional[str],
            airport_id: int,
            city_id: int,
            quarter: int,
            total_avg_hub_fare: float,
            total_fared_passengers: int,
            total_mkts: int,
            total_per_low_fare: float,
            total_per_premium: float,
            year: int
    ):
        self.Id = f'{year}-{quarter}-{airport_id}' if id is None else id
        self.AirportId = airport_id
        self.CityId = city_id
        self.Quarter = quarter
        self.TotalAvgHubFare = total_avg_hub_fare
        self.TotalFaredPas = total_fared_passengers
        self.TotalMkts = total_mkts
        self.TotalPerLowFare = total_per_low_fare
        self.TotalPerPremium = total_per_premium
        self.Year = year


@dataclass
class MishandledItemsInfo:
    Id: str
    AirlineCode: str
    MishandledBags: int
    MishandledChairs: int
    Month: int
    Quarter: int
    TotalBags: int
    TotalChairs: int
    Year: int

    def __init__(
            self,
            id: Optional[str],
            mishandled_bags: Optional[int],
            mishandled_chairs: Optional[int],
            airline_code: str,
            month: int,
            quarter: int,
            total_bags: int,
            total_chairs: int,
            year: int
    ):
        self.Id = f'{year}-{month:02d}-Q{quarter}-{airline_code}' if id is None else id
        self.AirlineCode = airline_code
        self.MishandledBags = 0 if mishandled_bags is None else mishandled_bags
        self.MishandledChairs = 0 if mishandled_chairs is None else mishandled_chairs
        self.Month = month
        self.Quarter = quarter
        self.TotalBags = total_bags
        self.TotalChairs = total_chairs
        self.Year = year


@dataclass
class MishandledPassengerInfo:
    Id: str
    CompPaid: int
    MktAirlineCode: str
    Month: int
    NumComp: int
    NumDowngraded: int
    NumUpgraded: int
    OpAirlineCode: str
    Quarter: int
    TotalBoarding: int
    TotalDenied: int
    Year: int

    def __init__(
            self,
            id: Optional[str],
            comp_paid: Optional[int],
            num_comp: Optional[int],
            num_downgraded: Optional[int],
            num_upgraded: Optional[int],
            total_denied: Optional[int],
            mkt_airline_code: str,
            month: int,
            quarter: int,
            op_airline_code: str,
            total_boarding: int,
            year: int
    ):
        self.Id = f'{year}-{month:02d}-Q{quarter}-{mkt_airline_code}-{op_airline_code}' if id is None else id
        self.MktAirlineCode = mkt_airline_code
        self.OpAirlineCode = op_airline_code
        self.CompPaid = 0 if comp_paid is None else comp_paid
        self.NumComp = 0 if num_comp is None else num_comp
        self.NumDowngraded = 0 if num_downgraded is None else num_downgraded
        self.NumUpgraded = 0 if num_upgraded is None else num_upgraded
        self.Month = month
        self.Quarter = quarter
        self.TotalBoarding = total_boarding
        self.TotalDenied = total_denied
        self.Year = year


@dataclass
class LastDone:
    LastUpdated: date

    def __init__(self):
        self.LastUpdated = date.today()
