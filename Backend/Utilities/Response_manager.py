import random

def Att_encoder(data: dict):
    for emp in data:
        # Calculate attendance salary
        if emp['iconAM'] == 'square' and emp['iconPM'] == 'square':
            emp['attendance_code'] = 0
            emp['att_sal'] = 0 * (emp['Basic_Per_Day'] if emp['Basic_Per_Day'] is not None else 0)
        elif emp['iconAM'] == 'check-square' and emp['iconPM'] == 'square':
            emp['attendance_code'] = 2
            emp['att_sal'] = 0.5 * (emp['Basic_Per_Day'] if emp['Basic_Per_Day'] is not None else 0)
        elif emp['iconAM'] == 'square' and emp['iconPM'] == 'check-square':
            emp['attendance_code'] = 3
            emp['att_sal'] = 0.5 * (emp['Basic_Per_Day'] if emp['Basic_Per_Day'] is not None else 0)
        elif emp['iconAM'] == 'check-square' and emp['iconPM'] == 'check-square':
            emp['attendance_code'] = 1
            emp['att_sal'] = 1 * (emp['Basic_Per_Day'] if emp['Basic_Per_Day'] is not None else 0)
        else:
            emp['att_sal'] = 0

        # Calculate OT salary
        if emp['iconAM_OT'] == 'square' and emp['iconPM_OT'] == 'square':
            emp['OT'] = 0
            emp['OT_sal'] = 0 * (emp['Basic_Per_Day'] if emp['Basic_Per_Day'] is not None else 0)
        elif emp['iconAM_OT'] == 'check-square' and emp['iconPM_OT'] == 'square':
            emp['OT'] = 2
            emp['OT_sal'] = 0.5 * (emp['Basic_Per_Day'] if emp['Basic_Per_Day'] is not None else 0)
        elif emp['iconAM_OT'] == 'square' and emp['iconPM_OT'] == 'check-square':
            emp['OT'] = 3
            emp['OT_sal'] = 0.5 * (emp['Basic_Per_Day'] if emp['Basic_Per_Day'] is not None else 0)
        elif emp['iconAM_OT'] == 'check-square' and emp['iconPM_OT'] == 'check-square':
            emp['OT'] = 1
            emp['OT_sal'] = 1 * (emp['Basic_Per_Day'] if emp['Basic_Per_Day'] is not None else 0)
        else:
            emp['OT_sal'] = 0

        # Calculate Daily Wage
        emp['Daily_Wage'] = emp['att_sal'] + emp['OT_sal']

        # Replace any None values with 'NULL'
        for key, value in emp.items():
            if value is None:
                emp[key] = 'NULL'

def Att_decoder (data: dict):
    for emp in data:
        if emp['attendance_code'] == 0:
            emp['iconAM'] = 'square'
            emp['iconPM'] = 'square'
            emp['tickColor'] = 'grey'
            emp['crossColor'] = 'red'
        elif emp['attendance_code'] == 2:
            emp['iconAM'] = 'check-square'
            emp['iconPM'] = 'square'
            emp['tickColor'] = 'green'
            emp['crossColor'] = 'grey'
        elif emp['attendance_code'] == 3:
            emp['iconAM'] = 'square'
            emp['iconPM'] = 'check-square'
            emp['tickColor'] = 'green'
            emp['crossColor'] = 'grey'
        elif emp['attendance_code'] == 1:
            emp['iconAM'] = 'check-square'
            emp['iconPM'] = 'check-square'
            emp['tickColor'] = 'green'
            emp['crossColor'] = 'grey'

    for emp in data:
        if emp['OT'] == 0:
            emp['iconAM_OT'] = 'square'
            emp['iconPM_OT'] = 'square'
        elif emp['OT'] == 2:
            emp['iconAM_OT'] = 'check-square'
            emp['iconPM_OT'] = 'square'
        elif emp['OT'] == 3:
            emp['iconAM_OT'] = 'square'
            emp['iconPM_OT'] = 'check-square'
        elif emp['OT'] == 1:
            emp['iconAM_OT'] = 'check-square'
            emp['iconPM_OT'] = 'check-square'

def Txn_decoder (data: dict):
    random_number = str(random.randint(1, 10000))
    data['ref'] = f"Ref_{data['Company_id']}_"+random_number
    if data['Adv_rec'] == 'Advance':
        data['Debit'] = data['amount']
        data['Credit'] = 'NULL'
        data['actual_due'] = data['dues'] + data['amount']
    if data['Adv_rec'] == 'Recovery':
        data['Credit'] = data['amount']
        data['Debit'] = 'NULL'
        data['actual_due'] = data['dues'] - data['amount']

def Txn_decoder_sal (data: dict):
    random_number = str(random.randint(1, 10000))
    data['ref'] = f"Ref_{data['Company_id']}_"+random_number
