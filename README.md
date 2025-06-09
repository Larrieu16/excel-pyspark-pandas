# 📝 Projeto de Importação e Análise de Tarefas Legadas com PySpark

Este projeto realiza a importação de dados legados a partir de uma planilha Excel, transformando os dados para o padrão utilizado pela aplicação (com Single Table Design em DynamoDB), e gera uma planilha com resumo de tarefas abandonadas.

## ⚙️ Tecnologias Utilizadas

- Python 3.10+
- Apache Spark (PySpark)
- Pandas (para exportar Excel)
- Boto3 (opcional para integração com DynamoDB)
- OpenPyXL

---

---

## 🧪 Objetivo do Projeto

1. Ler dados legados de tarefas a partir de uma planilha `.xlsx`
2. Transformar e limpar os dados:
   - Filtrar tarefas canceladas
   - Reatribuir a um novo usuário
   - Normalizar datas
   - Gerar chaves `PK` e `SK` para Single Table Design
3. Inserir as tarefas válidas no DynamoDB com dicionários JSON
4. Gerar uma nova planilha com **resumo de tarefas abandonadas** (status cancelled) dos últimos **6 meses**

---

## 🔄 Fluxo do Programa

### 1. `read_excel.py`

- Lê o arquivo `.xlsx` utilizando `SparkSession.read.format("com.crealytics.spark.excel")`
- Retorna um DataFrame com os dados crus da planilha

### 2. `transform_excel.py`

#### a) `transform_dataframe(df)`

- **Filtra**:
  - Tarefas com `status = 3` (cancelled)
  - Usuário original antigo (`f9a533f2c78e4a09f87c9e68e442d3fe`)
  - Apaga dados que não serão utilizados na tabela nova
- **Transforma**:
  - Reatribui todas as tarefas para o novo `user_sub`
  - Gera `item_id` com UUID
  - Formata `createdAt` e `date`
  - Cria `PK` e `SK` com base em datas e IDs
  - Traduz:
    - `Status`: `1 → todo`, `2 → done`, `3 → cancelled`
    - `Tipo da Tarefa`: `Tarefa a Ser Feita → Task`, `Item de Compra → Shopping_Item`

- **Retorno**: DataFrame pronto para inserção no DynamoDB

#### b) `generate_abandoned_summary(df)`

- **Filtra** apenas tarefas com `status = 3` (cancelled)
- Agrupa por mês (`Data de Conclusão`)
- Conta:
  - Total de tarefas abandonadas
  - Total de itens abandonados (`Tipo da Tarefa = Item de Compra`)
- Filtra os últimos **6 meses**
- **Retorno**: DataFrame com resumo para exportação como Excel

---

## 🧑‍💻 Execução

```bash
python main.py (Para geração do JSON)
python main.py --insert-from-json (Insere no DynamoDB com JSON)
python main.py --fetch-from-dynamo (Gera os relatórios através da tabela do DynamoDB)
