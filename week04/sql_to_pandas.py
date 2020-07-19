import pandas as pd
import numpy as np

def print_header(statement):
    print(f'\n#### {statement}')

group=[300, 600, 900, 1200, 1500]
data=pd.DataFrame({
    "id": [group[x] for x in np.random.randint(0, len(group), 16)],
    "age": np.random.randint(20, 60, 16),
    "order_id": np.random.randint(1000, 2000, 16)
    })

print_header(f'SELECT * FROM data')
print(data.loc[:,])

print_header(f'SELECT * FROM data LIMIT 10')
print(data.head(10))

print_header(f'SELECT id FROM data')
print(data[['id']])

print_header(f'SELECT COUNT(id) FROM data')
print(data['id'].count())

print_header(f'SELECT * FROM data WHERE id<1000 AND age>30')
print(data[(data['id'] < 1000) & (data['age'] > 30)])

group=[10, 20, 30, 40, 50]
table1=pd.DataFrame({
  "id": [group[x] for x in np.random.randint(0, len(group), 10)],
  "name": [f'n{i}' for i in range(10)],
  "age": np.random.randint(20, 60, 10),
  "order_id": np.random.randint(1000, 2000, 10)
  })
table2=pd.DataFrame({
  "id": [group[x] for x in np.random.randint(0, len(group), 10)],
  "name": [f'n{i}' for i in range(10)],
  "age": np.random.randint(20, 60, 10),
  "order_id": np.random.randint(1000, 2000, 10)
  })

print_header(f'SELECT * FROM table1')
print(table1.loc[:,])

print_header(f'SELECT * FROM table2')
print(table2.loc[:,])

print_header(f'SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id')
print(table1.groupby(['id'])['order_id'].nunique().reset_index(name='distinct_orderid_count'))

print_header(f'SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id')
print(table1.merge(table2, on='id', how='inner', suffixes=('_t1','_t2')))

print_header(f'SELECT * FROM table1 UNION SELECT * FROM table2')
print(pd.concat([table1, table2]).drop_duplicates())

print_header(f'DELETE FROM table1 WHERE id=10')
table1 = table1[table1['id'] != 10].reset_index(drop=True)
print(table1)

print_header(f'ALTER TABLE table1 DROP COLUMN column_name')
table1.drop(['name'], axis=1, inplace=True)
print(table1)
