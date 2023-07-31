# Checks if the passed string is a float
import pandas as pd


def is_float(val: str):
    returnVal = False
    val = '0'+val if val.startswith('.') else val
    splitStr = val.strip().replace(' ','').replace('-', '', 1).replace(',', '').split('.')
    if len(splitStr) == 2:
        returnVal = True
        for s in splitStr:
            if not s.isnumeric():
                returnVal = False
            if not returnVal:
                break

    return returnVal


# Checks if the passed string is an int
def is_int(val: str):
    returnVal = False
    splitStr = val.strip().replace(' ','').replace('-', '', 1).replace(',', '').split('.')

    if len(splitStr) == 1:
        returnVal = splitStr[0].isnumeric()

    return returnVal


def is_date(val: str):
    splitStr = val.strip().replace(' ','').split('-')
    returnVal = False
    if len(splitStr) != 3:
        splitStr = val.strip().replace(' ', '').split('/')
    if len(splitStr) == 3:
        if ((len(splitStr[0]) == 4 and len(splitStr[2]) <= 2) or (len(splitStr[2]) == 4 and len(splitStr[0]) <= 2)) and len(splitStr[1]) <= 2:
            for s in splitStr:
                returnVal = s.isnumeric()
                if not returnVal:
                    break

    return returnVal


def is_time(val: str):
    splitStr = val.strip().replace(' ', '').split(':')
    returnVal = len(splitStr) == 3 or len(splitStr) == 2
    if (returnVal):
        returnVal = len(splitStr[0]) == 2 and splitStr[0].isnumeric() and len(splitStr[1]) == 2 and splitStr[1].isnumeric()

    return returnVal


def is_datetime(val: str):
    returnVal = False
    splitStr = val.strip().split(' ')
    if len(splitStr) == 1:
        splitStr = val.strip().split('T')
    if (len(splitStr) == 2):
        returnVal = is_date(splitStr[0]) and is_time(splitStr[1])

    return returnVal


def is_bool(val: str):
    return str(val) == 'False' or str(val) == 'True'


# Gets the type
def get_type(val: str):
    type = 'str'
    type = 'bool' if is_bool(val) else type
    if type != 'bool':
        type = 'float' if is_float(val) else type
        if type != 'float':
            type = 'int' if is_int(val) else type
            type = 'date' if is_date(val) else type
            type = 'time' if is_time(val) else type
            type = 'date_time' if is_datetime(val) else type

    return type


def set_types(df: pd.DataFrame):

    for col in df.columns:
        described = df[col].describe()
        if described.dtype == 'object':
            if df[col] is not None:
                try:
                    type = get_type(described.top)

                    if type == 'date' or type == 'date_time':
                        df[col] = pd.to_datetime(df[col])
                    if type == 'int' or type == 'float':
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                        df[col] = df[col].fillna(0)

                    if type != 'date' and type != 'date_time' and type != 'time' and type != 'None' and type is not None:
                        if type == 'str':
                            df[col] = df[col].astype(pd.StringDtype(), copy=False)
                        else:
                            df[col] = df[col].astype(type, copy=False)

                except Exception as e:
                    print(e)
                    pass
    return df
