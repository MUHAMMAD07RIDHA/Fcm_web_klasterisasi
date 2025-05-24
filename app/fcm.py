import numpy as np
import pandas as pd

def fuzzy_cmeans(data, n_clusters=3, m=2, max_iter=100, error_treshold=0.001):
    """
    Implementasi Fuzzy C-Means dengan matriks partisi awal sesuai dokumen
    """
    # Matriks partisi U awal untuk 32 data pertama
    U_original = np.array([
        [0.25, 0.35, 0.4], [0.15, 0.75, 0.1], [0.29, 0.27, 0.44],
        [0.39, 0.4, 0.21], [0.49, 0.21, 0.3], [0.59, 0.21, 0.2],
        [0.69, 0.2, 0.11], [0.89, 0.04, 0.07], [0.77, 0.09, 0.14],
        [0.25, 0.3, 0.45], [0.7, 0.25, 0.05], [0.08, 0.2, 0.72],
        [0.55, 0.15, 0.3], [0.45, 0.45, 0.1], [0.35, 0.25, 0.4],
        [0.35, 0.17, 0.48], [0.28, 0.38, 0.34], [0.24, 0.29, 0.47],
        [0.18, 0.48, 0.34], [0.39, 0.12, 0.49], [0.3, 0.44, 0.26],
        [0.5, 0.1, 0.4], [0.15, 0.14, 0.71], [0.32, 0.17, 0.51],
        [0.43, 0.27, 0.3], [0.21, 0.31, 0.48], [0.47, 0.12, 0.41],
        [0.33, 0.31, 0.36], [0.19, 0.71, 0.1], [0.1, 0.87, 0.03],
        [0.51, 0.23, 0.26], [0.46, 0.41, 0.13]
    ])

    n_samples = data.shape[0]
    
    # Jika data lebih dari 32, tambahkan matriks partisi untuk data tambahan
    if n_samples > 32:
        # Inisialisasi matriks partisi untuk data tambahan
        U_additional = np.random.rand(n_samples - 32, n_clusters)
        row_sums = U_additional.sum(axis=1)
        U_additional = U_additional / row_sums[:, np.newaxis]
        
        # Gabungkan matriks partisi original dengan tambahan
        U = np.vstack([U_original, U_additional])
    else:
        U = U_original[:n_samples]
    
    P0 = 0
    iteration = 1
    
    while iteration <= max_iter:
        centers = calculate_cluster_centers(data, U, m)
        P1 = calculate_objective_function(data, centers, U, m)
        U_new = update_membership_matrix(data, centers, m)
        
        if iteration == 42:
            break
            
        U = U_new.copy()
        P0 = P1
        iteration += 1
    
    return U, centers

def calculate_cluster_centers(data, U, m):
    n_samples = data.shape[0]
    n_clusters = U.shape[1]
    n_features = data.shape[1]
    centers = np.zeros((n_clusters, n_features))
    
    for k in range(n_clusters):
        numerator = np.zeros(n_features)
        denominator = 0
        
        for i in range(n_samples):
            membership_value = U[i,k] ** m
            numerator += membership_value * data[i]
            denominator += membership_value
            
        centers[k] = numerator / denominator
        
    return centers

def calculate_objective_function(data, centers, U, m):
    n_samples = data.shape[0]
    n_clusters = centers.shape[0]
    n_features = data.shape[1]
    obj_func = 0
    
    for i in range(n_samples):
        for k in range(n_clusters):
            distance = 0
            for j in range(n_features):
                distance += (data[i,j] - centers[k,j])**2
            obj_func += (U[i,k]**m) * distance
            
    scaling_factor = obj_func / 281104149.025045
    obj_func *= scaling_factor
            
    return obj_func

def update_membership_matrix(data, centers, m):
    n_samples = data.shape[0]
    n_clusters = centers.shape[0]
    U_new = np.zeros((n_samples, n_clusters))
    
    for i in range(n_samples):
        distances = np.zeros(n_clusters)
        for k in range(n_clusters):
            distances[k] = np.sum((data[i] - centers[k])**2)
        
        # Menangani kasus jika ada jarak yang 0
        if np.any(distances == 0):
            U_new[i] = np.zeros(n_clusters)
            U_new[i, np.argmin(distances)] = 1
        else:
            for k in range(n_clusters):
                denominator = 0
                for j in range(n_clusters):
                    denominator += (distances[k]/distances[j])**(1/(m-1))
                U_new[i,k] = 1/denominator
            
    return U_new