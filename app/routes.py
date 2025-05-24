from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import numpy as np
import pandas as pd
from app import mysql
from app.fcm import fuzzy_cmeans
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash
import functools

main = Blueprint('main', __name__)

# Decorator untuk cek login
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('main.login'))
        return view(**kwargs)
    return wrapped_view

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and check_password_hash(user['password'], password):
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('main.home'))
            
        flash('Username atau password salah')
    
    return render_template('auth/login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        error = None
        
        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        if cursor.fetchone() is not None:
            error = 'Username {} sudah terdaftar.'.format(username)
        
        if error is None:
            cursor.execute(
                'INSERT INTO users (username, password) VALUES (%s, %s)',
                (username, generate_password_hash(password))
            )
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('main.login'))
        
        flash(error)
        cursor.close()
    
    return render_template('auth/register.html')

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

@main.route('/')
@login_required
def home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Hitung jumlah daerah
    cursor.execute('SELECT COUNT(*) as total_daerah FROM data_penyakit')
    total_daerah = cursor.fetchone()['total_daerah']
    
    # Ambil data untuk grafik
    cursor.execute('''
        SELECT 
            p.puskesmas_kecamatan,
            p.stunting,
            p.wasting,
            p.underweight
        FROM data_penyakit p
        ORDER BY p.stunting + p.wasting + p.underweight DESC
        LIMIT 10
    ''')
    top_data = cursor.fetchall()
    
    # Hitung total kasus
    cursor.execute('''
        SELECT 
            SUM(stunting) as total_stunting,
            SUM(wasting) as total_wasting,
            SUM(underweight) as total_underweight
        FROM data_penyakit
    ''')
    totals = cursor.fetchone()
    
    cursor.close()
    
    chart_data = {
        'labels': [d['puskesmas_kecamatan'] for d in top_data],
        'stunting': [d['stunting'] for d in top_data],
        'wasting': [d['wasting'] for d in top_data],
        'underweight': [d['underweight'] for d in top_data]
    }
    
    return render_template('home.html',
                         total_daerah=total_daerah,
                         totals=totals,
                         chart_data=chart_data)

@main.route('/data-awal')
@login_required
def data_awal():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM data_penyakit')
    data = cursor.fetchall()
    cursor.close()
    return render_template('data_awal.html', data=data)

@main.route('/data-klaster', methods=['GET'])
@login_required
def data_klaster():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM data_penyakit')
    data = cursor.fetchall()
    cursor.close()
    
    df = pd.DataFrame(data)
    features = df[[
        'sasaran_balita_eppgbm', 
        'balita_entry_2023',
        'persentase', 
        'stunting', 
        'wasting', 
        'underweight'
    ]].values
    
    U_final, centers_final = fuzzy_cmeans(features)
    cluster_labels = np.argmax(U_final, axis=1)
    
    tingkat_kerawanan = {
        0: "Rendah",
        1: "Sedang",
        2: "Tinggi"
    }
    
    clustering_results = []
    for i, row in enumerate(data):
        result = dict(row)
        result['cluster'] = int(cluster_labels[i]) + 1
        result['tingkat_kerawanan'] = tingkat_kerawanan[cluster_labels[i]]
        result['membership_values'] = U_final[i]
        clustering_results.append(result)
    
    cluster_counts = {}
    for label in tingkat_kerawanan.values():
        count = sum(1 for r in clustering_results if r['tingkat_kerawanan'] == label)
        cluster_counts[label] = count
    
    return render_template(
        'data_klaster.html',
        data=clustering_results,
        centers=centers_final,
        cluster_counts=cluster_counts
    )

@main.route('/tambah-data', methods=['GET', 'POST'])
@login_required
def tambah_data():
    if request.method == 'POST':
        puskesmas = request.form['puskesmas']
        sasaran = request.form['sasaran']
        balita_entry = request.form['balita_entry']
        persentase = request.form['persentase']
        stunting = request.form['stunting']
        wasting = request.form['wasting']
        underweight = request.form['underweight']
        
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO data_penyakit 
            (puskesmas_kecamatan, sasaran_balita_eppgbm, balita_entry_2023, 
             persentase, stunting, wasting, underweight)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (puskesmas, sasaran, balita_entry, persentase, stunting, wasting, underweight))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('main.data_klaster'))
    return render_template('tambah_data.html')

@main.route('/edit-data/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_data(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST':
        puskesmas = request.form['puskesmas']
        sasaran = request.form['sasaran']
        balita_entry = request.form['balita_entry']
        persentase = request.form['persentase']
        stunting = request.form['stunting']
        wasting = request.form['wasting']
        underweight = request.form['underweight']
        
        cursor.execute('''
            UPDATE data_penyakit 
            SET puskesmas_kecamatan = %s, 
                sasaran_balita_eppgbm = %s,
                balita_entry_2023 = %s,
                persentase = %s,
                stunting = %s,
                wasting = %s,
                underweight = %s
            WHERE id = %s
        ''', (puskesmas, sasaran, balita_entry, persentase, stunting, wasting, underweight, id))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('main.data_klaster'))
    
    cursor.execute('SELECT * FROM data_penyakit WHERE id = %s', (id,))
    data = cursor.fetchone()
    cursor.close()
    
    return render_template('edit_data.html', data=data)

@main.route('/hapus-data/<int:id>')
@login_required
def hapus_data(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM data_penyakit WHERE id = %s', (id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('main.data_klaster'))

@main.route('/validasi-klaster')
@login_required
def validasi_klaster():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM data_penyakit')
    data = cursor.fetchall()
    cursor.close()
    
    df = pd.DataFrame(data)
    features = df[[
        'sasaran_balita_eppgbm', 
        'balita_entry_2023',
        'persentase', 
        'stunting', 
        'wasting', 
        'underweight'
    ]].values
    
    # Menjalankan FCM
    U_final, centers = fuzzy_cmeans(features)
    cluster_labels = np.argmax(U_final, axis=1)
    
    # Menghitung validasi indeks
    silhouette_avg = calculate_silhouette(features, cluster_labels)
    partition_coefficient = calculate_partition_coefficient(U_final)
    partition_entropy = calculate_partition_entropy(U_final)
    
    # Membuat data untuk grafik
    validation_data = {
        'indeks': ['Silhouette', 'Partition Coefficient', 'Partition Entropy'],
        'nilai': [silhouette_avg, partition_coefficient, partition_entropy]
    }
    
    return render_template(
        'validasi_klaster.html',
        validation_data=validation_data
    )

def calculate_silhouette(data, labels):
    from sklearn.metrics import silhouette_score
    return silhouette_score(data, labels)

def calculate_partition_coefficient(U):
    return np.sum(U ** 2) / U.shape[0]

def calculate_partition_entropy(U):
    return -np.sum(U * np.log(U + 1e-10)) / U.shape[0]

@main.route('/summary-klaster')
@login_required
def summary_klaster():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM data_penyakit')
    data = cursor.fetchall()
    cursor.close()
    
    df = pd.DataFrame(data)
    features = df[[
        'sasaran_balita_eppgbm', 
        'balita_entry_2023',
        'persentase', 
        'stunting', 
        'wasting', 
        'underweight'
    ]].values
    
    # Menjalankan FCM
    U_final, centers = fuzzy_cmeans(features)
    cluster_labels = np.argmax(U_final, axis=1)
    
    # Menambahkan label cluster ke DataFrame
    df['cluster'] = cluster_labels
    
    # Menghitung rata-rata untuk setiap cluster
    summary = df.groupby('cluster').agg({
        'sasaran_balita_eppgbm': 'mean',
        'balita_entry_2023': 'mean',
        'persentase': 'mean',
        'stunting': 'mean',
        'wasting': 'mean',
        'underweight': 'mean'
    }).round(2)
    
    # Menghitung jumlah daerah per cluster
    cluster_counts = df['cluster'].value_counts().sort_index()
    
    # Mapping tingkat kerawanan
    tingkat_kerawanan = {
        0: "Rendah",
        1: "Sedang",
        2: "Tinggi"
    }
    
    # Menyiapkan data untuk radar chart
    chart_data = {
        'features': ['Sasaran Balita', 'Balita Entry', 'Persentase', 'Stunting', 'Wasting', 'Underweight'],
        'cluster_0': summary.iloc[0].tolist(),
        'cluster_1': summary.iloc[1].tolist(),
        'cluster_2': summary.iloc[2].tolist()
    }
    
    return render_template(
        'summary_klaster.html',
        summary=summary,
        cluster_counts=cluster_counts,
        tingkat_kerawanan=tingkat_kerawanan,
        chart_data=chart_data
    )