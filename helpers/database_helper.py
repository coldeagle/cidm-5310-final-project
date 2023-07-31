# This helper fills in the database from API calls
import dateutil.utils
from sqlalchemy import create_engine, Table, select, insert
from sqlalchemy.orm import sessionmaker
from helpers import api_helper, type_helper
from models import models, orm
from models.orm import metadata, start_mappers, mapper_registry
from dataclasses import asdict
import pandas as pd
import dotenv
import os
dotenv.load_dotenv()

db = None


def getEngine() -> create_engine:
    engine = create_engine(os.environ.get('DB_PATH'), echo=False)
    try:
        mapper_registry.metadata.create_all(bind=engine)
    except Exception:
        pass
    try:
        start_mappers()
    except Exception:
        pass
    global db
    db = engine
    return engine


def load_data():
    global db
    db = getEngine()

#    try:
    Session = sessionmaker(bind=db)
    session = Session()
    # Making sure we haven't already pulled today, we only want to hit up the API's once a day
    if len(session.execute(select(orm.last_done).filter_by(LastUpdated=dateutil.utils.today().date())).all()) == 0:
        get_and_add_quarterly_airline()
        get_and_add_fare_info_high_low()
        get_and_add_ConnectingMarketFareInfoMultiCarrier()
        get_and_add_involuntary_denied_boarding()
        get_and_add_mishandled_items()
        # Creating a last updated record, so we only pull once a day
        set_last_updated(session)
#   except Exception as e:
#        print(e)

    #print(quarterly_airline_numbers_list)


def get_and_add_quarterly_airline():
    db_list = []
    df = api_helper.do_callout('evch-7vws', 'year,quarter,item_name,uniquecarriername,uniquecarrier,airlineid, val', "year=2020 and uniquecarriername != ''")
    handle_airline_op_mapping(df=df, carrier_name='uniquecarriername', u_carrier_name='uniquecarriername', id_field='airlineid', code_field='uniquecarrier')

    for row_index, row in df.iterrows():
        db_list.append(asdict(models.AirlineQuarterlyNums(
                year=row['year'],
                quarter=row['quarter'],
                item_name=row['item_name'],
                carrier=row['uniquecarrier'],
                value=row['val'],
                id=None
            )))

    df = handle_to_sql_from_models(db_list=db_list, index_fld='Id', table_name='airline_quarterly_numbers', if_exists='replace', include_index=True)


def get_and_add_fare_info_high_low():
    db_list = []
    df = api_helper.do_callout('bkh6-tj42', '*', 'year="2020"')

    for row_index, row in df.iterrows():
        db_list.append(asdict(models.ConnectingMarketFareInfo(
            carrier=row['car'],
            city_1=row['citymarketid_1'],
            city_2=row['citymarketid_2'],
            fare=row['mkt_fare'],
            car_avg_fare=row['caravgfare'],
            car_passenger_share=row['carpaxshare'],
            quarter=row['quarter'],
            year=row['year'],
            id=None
        )))

    handle_city_high_low(df)
    df = handle_to_sql_from_models(db_list=db_list, index_fld='Id', table_name='connecting_market_fare_info', if_exists='replace', include_index=True)


def get_and_add_ConnectingMarketFareInfoMultiCarrier():
    df = api_helper.do_callout('yj5y-b2ir', '*', 'year="2020"')

    db_list = []
    for row_index, row in df.iterrows():
        db_list.append(asdict(models.ConnectingMarketFareInfoMultiCarrier(
            carrier_lg=row['carrier_lg'],
            carrier_low=row['carrier_low'],
            city_1=row['citymarketid_1'],
            city_2=row['citymarketid_2'],
            fare=row['fare_lg'],
            fare_low=row['fare_low'],
            lf_ms=row['lf_ms'],
            num_passengers=row['passengers'],
            ns_miles=row['nsmiles'],
            quarter=row['quarter'],
            year=row['year'],
            id=None
        )))

    df = handle_to_sql_from_models(db_list=db_list, index_fld='Id', table_name='connecting_market_fare_info_MultiCarrier', if_exists='replace', include_index=True)


def get_and_add_mishandled_items():
    df = api_helper.do_callout('6u8d-47ih', 'year, month, quarter, airline_id, carrier, carrier_name, unique_carrier, unique_carrier_name, mishandled_baggage, enplaned_baggage, mishandled_wchr_sctr, enplaned_wchr_sctr, form_type', 'year="2020"')
    df = type_helper.set_types(df)
    handle_airline_op_mapping(df=df, carrier_name='carrier_name', u_carrier_name='unique_carrier_name', id_field='airline_id', code_field='carrier')
    df_grouped = df.groupby(['year', 'month', 'unique_carrier'])
    db_list = []

    for group_name, df_group in df_grouped:
        quarter = None
        month = None
        year = None
        mishandled_bags = 0
        mishandled_chairs = 0
        airline_code = None
        total_bags = 0
        total_chairs = 0

        for row_index, row in df_group.iterrows():
            quarter = row['quarter']
            month = row['quarter']
            year = row['year']
            mishandled_bags += row['mishandled_baggage']
            mishandled_chairs += row['mishandled_wchr_sctr']
            airline_code = row['unique_carrier']
            total_bags += row['enplaned_baggage']
            total_chairs += row['enplaned_wchr_sctr']

        rec = asdict(models.MishandledItemsInfo(
            id=None,
            quarter=quarter,
            month=month,
            year=year,
            mishandled_bags=mishandled_bags,
            mishandled_chairs=mishandled_chairs,
            airline_code=airline_code,
            total_bags=total_bags,
            total_chairs=total_chairs
        ))

        db_list.append(rec)

    df = handle_to_sql_from_models(db_list=db_list, index_fld='Id', table_name='airline_items_mishandles', if_exists='replace', include_index=True)


def get_and_add_involuntary_denied_boarding():
    df = api_helper.do_callout('xyfb-hgtv', 'year, month, quarter, mkt_unique_carrier, mkt_unique_carrier_name, mkt_carrier_name, mkt_carrier_airline_id, op_carrier, op_carrier_airline_id, op_carrier_name, op_unique_carrier_name, op_unique_carrier, pax_comp_1, pax_comp_2, pax_upgrade, pax_downgrade, tot_boarding, comp_paid_1, comp_paid_2, comp_paid_3', 'year="2020"')
    df = type_helper.set_types(df)
    handle_airline_op_mapping(df=df, carrier_name='op_carrier_name', u_carrier_name='op_unique_carrier_name', id_field='op_carrier_airline_id', code_field='op_unique_carrier')
    handle_airline_op_mapping(df=df, carrier_name='mkt_carrier_name', u_carrier_name='mkt_unique_carrier_name', id_field='mkt_carrier_airline_id', code_field='mkt_unique_carrier')

    df['total_comped'] = df['pax_comp_1'] + df['pax_comp_2']
    df['total_comp_paid'] = df['comp_paid_1'] + df['comp_paid_2'] + df['comp_paid_3']
    df['total_denied'] = df['pax_upgrade'] + df['pax_downgrade']
    df_grouped = df.groupby(['year', 'month', 'op_unique_carrier'])

    db_list = []
    for group_name, df_group in df_grouped:
        total_denied = 0
        total_boarding = 0
        num_comp = 0
        comp_paid = 0
        num_upgraded = 0
        num_downgraded = 0
        month = None
        quarter = None
        year = None
        mkt_airline_code = None
        op_airline_code = None

        for row_index, row in df_group.iterrows():
            total_denied += row['total_denied']
            total_boarding += row['tot_boarding']
            num_comp += row['total_comped']
            comp_paid += row['total_comp_paid']
            num_upgraded += row['pax_upgrade']
            num_downgraded += row['pax_downgrade']
            quarter = row['quarter']
            year = row['year']
            mkt_airline_code = row['mkt_unique_carrier']
            op_airline_code = row['op_unique_carrier']
            month = row['month']

        db_list.append(asdict(models.MishandledPassengerInfo(
            quarter=quarter,
            year=year,
            total_denied=total_denied,
            total_boarding=total_boarding,
            num_comp=num_comp,
            comp_paid=comp_paid,
            num_upgraded=num_upgraded,
            num_downgraded=num_downgraded,
            mkt_airline_code=mkt_airline_code,
            op_airline_code=op_airline_code,
            month=month,
            id=None
        )))

    df = handle_to_sql_from_models(db_list=db_list, index_fld='Id', table_name='airline_passenger_mishandles', if_exists='replace', include_index=True)


def handle_airline_op_mapping(df: pd.DataFrame, id_field: str, code_field: str, u_carrier_name: str, carrier_name: str):
    new_df = pd.DataFrame({'Id': df[id_field], 'Code': df[code_field], 'UniqueName': df[u_carrier_name], 'Name': df[carrier_name]})
    new_df = new_df.set_index('Id')
    new_df.to_sql('airlines', con=db, if_exists='replace', index=True)

def handle_airports(df: pd.DataFrame):
    db_list = []



def handle_city_high_low(df: pd.DataFrame):
    df2 = pd.DataFrame({'Id': df['citymarketid_1'], 'Name': df['city1']})
    df2 = df2.set_index('Id')
    df3 = pd.DataFrame({'Id': df['citymarketid_2'], 'Name': df['city2']})
    df3 = df3.set_index('Id')
    df_combined = pd.concat([df2.drop_duplicates(ignore_index=False), df3.drop_duplicates(ignore_index=False)], axis=0)
    df_combined = df_combined.drop_duplicates(ignore_index=False, keep='first')
    df_combined = type_helper.set_types(df_combined)
    df_combined.to_sql('markets', con=db, if_exists='replace', index=True)


def handle_to_sql_from_models(db_list: list, index_fld: str, table_name: str, if_exists: str, include_index: bool):
    df = pd.DataFrame.from_records(db_list)
    df = df.set_index(index_fld)
    df = type_helper.set_types(df)
    df.to_sql(table_name, con=db, if_exists=if_exists, index=include_index)

    return df


def set_last_updated(session):
    session.execute(insert(orm.last_done), [{'LastUpdated': dateutil.utils.today()}])
    session.commit()

