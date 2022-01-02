# -*- coding: utf-8 -*-
'''
Modbus registers objects
'''

FAST_REGISTERS = [
    # regster, description, a   
    [40083, 'EB100-BE1 Current [A]', 10, 'U'],
    None,
    [40081, 'EB100-BE1 Current [A]', 10, 'U'],
    None,
    [40079, 'EB100-BE1 Current [A]', 10, 'U'],
    None,
    [40014, 'BT6 HW Load [°C]', 10, 'S'],
    [40008, 'BT2 Supply temp S1 [°C]', 10, 'S'],
    [40012, 'EB100-EP14-BT3 Return temp [°C]', 10, 'S'],
    [43005, 'Degree Minutes', 10, 'S'],
    [44701, 'EB101-EP14 Actual Cpr Frequency Outdoor Unit [Hz]', 10, 'U'],
    [40782, 'EB101 Cpr Frequency Desired F2040 [Hz]', 1, 'U'],
    [44699, 'EB101-EP14 High Pressure Sensor Outdoor Unit [bar]', 10, 'U'],
    [44700, 'EB101-EP14 Low Pressure Sensor Outdoor Unit [bar]', 10, 'U'],
    [44058, 'EB101-EP14-BT12 Condensor Out [°C]', 10, 'S'],
    [40013, 'BT7 HW Top [°C]', 10, 'S'],
    [44396, 'EB101 Speed charge pump [%]', 1, 'U'],
    [43437, 'Supply Pump Speed EP14 [%]', 1, 'U'],
    [44866, 'EB101-EP14 Current Sensor [A]', 10, 'U'],
    [44059, 'EB101-EP14-BT14 Hot Gas Temp [°C]', 10, 'S'],
]

REGULAR_REGISTERS = [
    [43009, 'Calc Supply Heat S1 [°C]', 10, 'S'],
    [44270, 'Calc Supply Cool S1 [°C]', 10, 'S'],
    [44703, 'EB101-EP14 Defrosting Outdoor Unit', 1, 'U'],
    [44702, 'EB101-EP14 Protection Status Register Outdoor Unit', 1, 'U'],
    [44362, 'EB101-EP14-BT28 Outdoor Temp [°C]', 1, 'S'],
    [44363, 'EB101-EP14-BT28 Evaporator [°C]', 10, 'S'],
    [44060, 'EB101-EP14-BT16 Liquid Line [°C]', 10, 'S'],
    [44055, 'EB101-EP14-BT3 Return Temp [°C]', 10, 'S'],
    [44061, 'EB101-EP14-BT17 Suction [°C]', 10, 'S'],
    [44706, 'EB101-EP14 Calculated Power Outdoor Unit [kW]', 1, 'U'],
    [40072, 'EP14 flow [l/m]', 10, 'U'],
]

SLOW_REGISTERS = [
    [40004, 'BT1 Outdoor Temperature [°C]', 10, 'S'],
    [40067, 'BT1 Outdoor Temperature average [°C]', 10, 'S'],
    [40033, 'BT50 Room Temp S1 [°C]', 10, 'S'],
    [44069, 'EB101-EP14 Compressor Starts', 1, 'U'],
    [44071, 'EB101-EP14 total op. time compr. [h]', 1, 'U'],
    [44073, 'EB101-EP14 total HW op. time compr. [h]', 1, 'U'],
    [40737, 'EB101-EP14 total Cooling op. time compr. [h]', 1, 'U'],
    [44302, 'EP14 Heat Meter - Cooling Cpr [kWh]', 10, 'U'],
    [44308, 'EP14 Heat Meter - Heat Cpr [kWh]', 10, 'U'],
    [44300, 'EP14 Heat Meter - Heat Cpr and Add [kWh]', 10, 'U'],
    [44306, 'EP14 Heat Meter - HW Cpr [kWh]', 10, 'U'],
    [44298, 'EP14 Heat Meter - HW Cpr and Add [kWh]', 10, 'U'],
]
