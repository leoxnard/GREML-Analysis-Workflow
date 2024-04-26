import anndata
import pandas as pd
from sklearn.metrics import pairwise_distances
import os

genome_input = snakemake.input['genome_input']
grm_output = snakemake.output['grm_output']
distance_method = snakemake.params['distance_method']

distance_methods = [
    'pearson',
    'spearman',
    'correlation',
    'cosine',
    'euclidean',
    'cityblock',
    'euclidean',
    'l1',
    'l2',
    'manhattan',
    'canberra',
    'chebyshev',
    'hamming',
    'mahalanobis',
    'minkowski',
    'seuclidean',
    'sqeuclidean'
]

if distance_method not in distance_methods:
    raise ValueError(f"Distance method {distance_method} not supported. Please choose one of {distance_methods}.")

print("Loading data...")
adata = anndata.read_h5ad(genome_input, backed='r')

adata_df = adata.to_df()
print(f"Data has {adata.shape[0]} samples and {adata.shape[1]} features with first 5 rows and columns:")
print(adata_df.iloc[:5, :5])

print(f"Calculating distance matrix...")
if distance_method == 'pearson' or distance_method == 'spearman':
    adata_df = adata_df.T
    distance_df = adata_df.corr(method=distance_method)
    distance_matrix = distance_df.values
else:
    distance_matrix = pairwise_distances(adata_df, metric=distance_method, n_jobs=-1)

print(f"Distance matrix has shape {distance_matrix.shape} with first 5 rows and columns:")
print(distance_matrix[:5, :5])

print("Creating flat distance matrix table...")
n = distance_matrix.shape[0]
distance_matrix_list = [(i+1, j+1, adata.shape[0], distance_matrix[i, j]) for i in range(n) for j in range(i+1)]
distance_matrix_df_flat = pd.DataFrame(distance_matrix_list, columns=['patient1', 'patient2', 'non-missing SNPs', 'distance'])
print(f"Distance matrix table has length {len(distance_matrix_df_flat['distance'])} with first 5 elements:")
print(distance_matrix_df_flat.head(5))

print("Saving distance matrix grm...")
distance_matrix_df_flat.to_csv(grm_output, index=False, header=False, sep='\t')
print("Compressing distance matrix table...")
os.system(f"pigz -p8 {grm_output}")
print("Done!")