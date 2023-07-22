import pandas as pd

def convert_csv_to_sql(table_name='property_table', csv_file_name='property_table.csv'):
    if table_name == 'property_table':
        df = pd.read_csv(csv_file_name)
        for row in df.itertuples():
            self.c.execute('''
                        INSERT INTO products (product_id, product_name, price)
                        VALUES (?,?,?)
                        ''',
                        row.product_id, 
                        row.product_name,
                        row.price
                        )
        self.connt.commit()
    else:
        pass
    return 