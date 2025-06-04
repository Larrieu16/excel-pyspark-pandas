from read_excel import read_excel_file
from transform_excel import transform_dataframe
import os
import sys 

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

csv_path = "C:\\Users\\Larri\\Downloads\\amostragem.csv"
output_csv = "C:\\Users\\Larri\\Downloads\\amostragem_transformada_dynamo.csv"

df_original = read_excel_file(csv_path)

df_transformado = transform_dataframe(df_original)

print("Visualização dos dados transformados:")
df_transformado.show(truncate=False)
df_transformado.printSchema()

try:
    pandas_df = df_transformado.toPandas()
    pandas_df.to_csv(output_csv, index=False, encoding='utf-8')
    
    print(f"\nArquivo CSV salvo com sucesso em: {output_csv}")
    print(f"Número de registros exportados: {len(pandas_df)}")
    
except Exception as e:
    print(f"\nErro ao exportar o arquivo CSV: {str(e)}")