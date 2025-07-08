import pygsheets

async def add_row_to_table(row):
    gc = pygsheets.authorize(service_file="leadifi-478ae79c5357.json")
    sh = gc.open('leadifi')


    worksheet = sh.sheet1
    records = worksheet.get_all_records()
    new_row = len(records) + 2
    worksheet.update_values(f'A{new_row}', [row])