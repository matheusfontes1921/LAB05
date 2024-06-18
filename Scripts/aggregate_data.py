import pandas as pd

# Carregar o arquivo CSV original
file_path = './experiment_results.csv'
df = pd.read_csv(file_path)

# Calculando médias
agg_df = df.groupby(['API', 'Complexity']).agg(
    avg_response_time=('Response Time (s)', 'mean'),
    avg_response_size=('Response Size (bytes)', 'mean')
).reset_index()

# Salvar o DataFrame agregado em um arquivo CSV
agg_file_path = './aggregated_experiment_results.csv'
agg_df.to_csv(agg_file_path, index=False)

print("Arquivo agregado salvo em:", agg_file_path)
print(agg_df)
