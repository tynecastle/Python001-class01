Pandas的使用

1. 数据集
通过sklearn中的datasets库可以导入很多经典数据集，包括：
- datasets.load_iris()  鸢尾花数据集
- datasets.load_boston()  Boston房屋价格数据集（回归分析）
- datasets.load_digits()  手写体数据集（分类）

2. 读取文件的技巧
如果要读取的文件和当前python脚本在同一路径下，可以使用如下方法获取脚本所在的绝对路径：
pwd = os.path.dirname(os.path.realpath(__file__))
然后再将获取的路径与要读取的文件名拼接在一起：
book = os.path.join(pwd, 'book_utf8.csv')

3. Pandas的基本使用
- 读取csv格式的文件并将全部内容放入一个DataFrame对象：
  df = pd.read_csv(book)
- 对象df中会默认把读到的第一行数据当做表头，不管它是不是真正的表头
- 筛选标题为"还行"这一列：
  df['还行']
- 以切片方式进行筛选，显示前3行（行号为0到2）：
  df[0:3]
- 添加表头：
  df.columns = ['star', 'vote', 'shorts']
- 显示特定的行、列：
  df.loc[1:3, ['star']]  # 行号为1到3
- 删除缺失数据的行：
  df.dropna()
- 数据聚合，统计标题为“star”这一列每个值的出现次数：
  df.groupby('star').sum()
- Python和Excel结合，实际上就是将Python的内置函数与Pandas结合
  star_to_number = {
      '力荐' : 5,
      '推荐' : 4,
      '还行' : 3,
      '较差' : 2,
      '很差' : 1
  }
  df['new_star'] = df['star'].map(star_to_number)

4. Pandas的两大基本数据结构
Series和DataFrame是Pandas的两大基本数据结构，它们都是基于numpy做的封装

5. Series
- Series可以看成是只有一个列维度的数据结构
- Series会给数据自动加上索引，这些索引也可以被修改
- 两个基本属性：index和values
- 通过字典创建带索引的Series：
  s1 = pd.Series({'a':11, 'b':22, 'c':33})
- 通过关键字创建带索引的Series：
  s2 = pd.Series([11, 22, 33], index = ['a', 'b', 'c'])
- 将Series对象转换为Python的列表：
  s1.values.tolist()
- 使用index会提升查询性能
  - 如果index唯一，pandas会使用哈希表优化，查询性能为O(1)
  - 如果index有序不唯一，pandas会使用二分查找算法，查询性能为O(logN)
  - 如果index完全随机，每次查询都要扫全表，查询性能为O(N)
- 使用Pandas的map函数对数据做批量处理：
  emails = pd.Series(['abc at amazom.com', 'admin1@163.com', 'mat@m.at', 'ab@abc.com'])
  pattern = '[A-Za-z0-9.\_]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,5}'
  mask = emails.map(lambda x: bool(re.match(pattern, x)))

6. DataFrame
- DataFrame具有行和列两个维度，类似Excel表格
- 可以自定义行索引和列索引
  df = pd.DataFrame([
      ['a', 'b', 'c'], 
      ['d', 'e', 'f']
    ],
    columns = ['one', 'two', 'three'],
    index = ['first', 'second']
  )

7. Pandas数据导入
- 导入Excel文件，需要注意读取Excel文件依赖底层的xlrd库，需要事先安装：
  pip install xlrd
  excel1 = pd.read_excel(r'1.xlsx')
  pd.read_excel(r'1.xlsx', sheet_name=0)
- 导入csv文件
  pd.read_csv(r'1.csv', sep=' ', nrows=10, encoding='utf-8')
- 导入文本文件
  pd.read_table(r'1.txt', sep = ' ')
- 导入MySQL表
  import pymysql
  sql = 'SELECT *  FROM mytable'
  conn = pymysql.connect('ip', 'name', 'pass', 'dbname', 'charset=utf8')
  df = pd.read_sql(sql, conn)

8. 查看Pandas数据的全貌信息
- 查看前几行
  excel1.head(3)
- 查看行列数量
  excel1.shape
- 查看详细信息
  excel1.info()
  <class 'pandas.core.frame.DataFrame'>
  RangeIndex: 3 entries, 0 to 2
  Data columns (total 4 columns):
   #   Column  Non-Null Count  Dtype  
  ---  ------  --------------  -----  
   0   num1    3 non-null      int64  
   1   num2    2 non-null      float64
   2   num3    3 non-null      int64  
   3   num4    3 non-null      int64  
  dtypes: float64(1), int64(3)
  memory usage: 224.0 bytes
  None
- 查看统计信息
  excel1.describe()
               num1        num2        num3        num4
  count    3.000000    2.000000    3.000000    3.000000
  mean    48.333333  113.000000  131.000000  172.333333
  std     56.580326  154.149278  176.714459  237.112491
  min      1.000000    4.000000    5.000000    7.000000
  25%     17.000000   58.500000   30.000000   36.500000
  50%     33.000000  113.000000   55.000000   66.000000
  75%     72.000000  167.500000  194.000000  255.000000
  max    111.000000  222.000000  333.000000  444.000000

9. 数据预处理
- 缺失值
  - Series对象中的缺失值是numpy.nan，而DataFrame对象中是None
  - 检查是否存在缺失值，Series对象使用hasnans属性，而DataFrame对象使用isnull()方法
  - 使用df.isnull().sum()可以统计DataFrame对象每一行有多少个缺失值
  - 缺失值填充有多种方法，要注意对原数据不是in place的修改，需要赋值给新的对象才能保留填充后的结果
  - 可以将缺失值填充为平均值：
    x.fillna(value=x.mean())
  - 可以前向填充缺失值：
    df.ffill()  # 使用前一行的值填充
    df.ffill(axis=1)  # 使用前一列的值填充
  - 可以将缺失值填充为默认值：
    x.fillna('无')
  - 一般情况下不能随意填充缺失值，尤其是当缺失值的意义很重要时（如人的性别），如果无法填充就应删除整条记录：
    x.dropna()
- 重复值
  - 删除重复值：df.drop_duplicates()

10. 数据调整
- 行列选择，注意要把被筛选的行或列的名称放在列表里，而不是元组
  df[ ['A', 'C'] ]  # 根据列的名称筛选
  df.iloc[:, [0, 2]]  # :表示所有行，筛选第1列和第3列
  df.loc[ [0, 2] ]  # 筛选第1行和第3行
  df.loc[ 0:2 ]  # 筛选从第1行到第3行
  df[ ( df['A'] < 5 ) & ( df['C'] < 4 ) ]  # 用比较条件进行筛选
- 数值替换，也要注意对原数据不是in place的修改，需要赋值给新的对象才能保留填充后的结果
  df['C'].replace(4, 40)
  df.replace(np.NaN, 0)
  df.replace([4, 5, 8], 1000)
- 数值排序
  df.sort_values( by=['A'], ascending=False)  # 按照指定列降序排列
  df.sort_values( by=['A','C'], ascending=[True,False])  # 多列排序
- 数值删除
  df.drop('A', axis=1)  # 删除列
  df.drop(3, axis=0)  # 删除行
  df[ df['A'] < 4 ]  # 删除满足条件的若干行
- 行列互换（矩阵转置）
  df.T
  df.T.T
- 索引重塑：可以做数据透视表
  - df.stack()
  - df.unstack()
  - df.stack().reset_index()

11. 数值运算
- 基本运算
  - 某一列所有数值加/减/乘/除某一个常数：
    df['A'] + 5
  - 列与列之间加减乘除：
    df['A'] + df['C']
  - 列与列之间比较数值：
    df['A'] > df['C']
- 汇总
  - 非空值计数：df.count()
  - 列求和：df.sum()，df['A'].sum()
  - 求均值：df.mean()
  - 求最大/最小值：df.max()，df.min()
  - 求中位数：df.median()
  - 求众数：df.mode()
  - 求方差：df.var()
  - 求标准差：df.std()
- 数据分组
  - df.groupby('field1').count()
  - df.groupby('field1').sum()
  - df.groupby('field1').mean()
  - df.groupby('field1').mean().to_dict()
  - df.groupby('field1').aggregate({'field1':'count', 'field2':'sum'})
  - df.groupby('field1').transform('mean') # 把处理后的数值赋给每一个元素，而非聚合

12. 多表操作
- 多表拼接
  - 当数据源来自多种文件格式时，建议先集中导入pandas，然后再进行多表拼接，而不是先转换成统一格式再导入pandas。
  - 因为进行格式转换时还会遇到字符集、分隔符不一致的问题，会导致事倍功半。
  - 一对一（两个表有一个公共列）：pd.merge(data1, data2)
  - 多对一（两个表有多个公共列，基于其中一个进行拼接）：pd.merge(data3, data2, on='group')
  - 多对多（基于两个表的多个公共列进行拼接）：pd.merge(data3, data2)
- 连接键类型，解决连接的两个表没有公共列的问题
  - pd.merge(data3, data2, left_on='a', right_on='b')
  - pd.merge(data3, data2, left_index='a', right_index='b')
- 连接方式
  - 内连接（默认方式）：pd.merge(data3, data2, on='group', how='inner')
  - 左连接：pd.merge(data3, data2, on='group', how='left')
  - 右连接：pd.merge(data3, data2, on='group', how='right')
  - 外连接：pd.merge(data3, data2, on='group', how='outer')
  - 纵向拼接：pd.concat([data1, data2])

13. 数据导出
- 导出类型
  - 导出为xlsx文件：
    df.to_excel(excel_writer=r'file.xlsx')
  - 设置Sheet名称：
    df.to_excel(excel_writer=r'file.xlsx', sheet_name='sheet1')
  - 设置索引/去掉索引：
    df.to_excel(excel_writer=r'file.xlsx', sheet_name='sheet1', index=False)
  - 设置要导出的列：
    df.to_excel(excel_writer=r'file.xlsx', sheet_name='sheet1', index=False, columns=['col1','col2'])
  - 设置编码格式：
    enconding = 'utf-8'
  - 缺失值处理：
    na_rep = 0
  - 无穷值处理：
    inf_rep = 0
  - 导出为pkl文件（速度为excel文件的7倍，但是只兼容pandas）：
    df.to_pickle('file.pkl')
- 可视化
  import matplotlib.pyplot as plt
  - 绘制简单地图表：
    plt.plot(df.index, df['A'],)
  - 自定义图表的样式：
    plt.plot(df.index, df['A'], color='#FFAA00', linestyle='--', linewidth=3, marker='D')
  - 绘制散点图：
    plt.scatter(df.index, df['A'])
  - 使用seaborn库美化plt
