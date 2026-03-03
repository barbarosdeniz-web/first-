import sqlite3
import pandas as pd
from datetime import datetime
# 1. Veritabanı bağlantısı oluşturma (Dosya yoksa otomatik yaratılır)
conn = sqlite3.connect('sirket_veritabani.db')
cursor = conn.cursor()

# 2. Tablo oluşturma sorgusu
# İncelik: Gerçek hayatta her tablonun eşsiz bir kimliği (Primary Key) olmalıdır.
# Ayrıca verilerin doğru formatta girilmesini zorlamak için 'NOT NULL' kısıtlamaları ekleriz.
create_table_query = """
CREATE TABLE IF NOT EXISTS satislar (
    islem_id INTEGER PRIMARY KEY AUTOINCREMENT,
    urun_adi TEXT NOT NULL,
    kategori TEXT,
    satis_miktari INTEGER NOT NULL,
    birim_fiyat REAL NOT NULL,
    satis_tarihi DATE NOT NULL
);
"""
cursor.execute(create_table_query)
conn.commit()


# Örnek bir ham veri seti oluşturalım (Bunu sisteminize gelen bir CSV gibi düşünün)
ham_veri = [
    {"urun_adi": "Laptop", "kategori": "Elektronik", "satis_miktari": 2, "birim_fiyat": 15000.50, "tarih": "2023-10-01"},
    {"urun_adi": "Masa", "kategori": "Mobilya", "satis_miktari": 1, "birim_fiyat": 2500.00, "tarih": "2023-10-01"},
    {"urun_adi": "Klavye", "kategori": "Elektronik", "satis_miktari": -5, "birim_fiyat": 500.00, "tarih": "2023-10-02"}, # HATA: Negatif miktar
    {"urun_adi": "Telefon", "kategori": None, "satis_miktari": 3, "birim_fiyat": 20000.00, "tarih": "2023-10-03"}, # HATA: Eksik kategori
]

df = pd.DataFrame(ham_veri)

# -- VERİ TEMİZLEME (TRANSFORM) ADIMLARI --

# 1. İncelik: Anlamsız verileri filtreleme (Negatif satış olamaz)
df = df[df['satis_miktari'] > 0]

# 2. İncelik: Eksik (NULL/NaN) verileri doldurma
df['kategori'] = df['kategori'].fillna("Belirtilmemiş")

# 3. İncelik: Veri tiplerini standardize etme
df['tarih'] = pd.to_datetime(df['tarih']).dt.date

print("Temizlenmiş Veri:")
print(df)
# Veriyi veritabanına eklemek için liste formatına çeviriyoruz
kayitlar = df.values.tolist()

# Mesleki İncelik: SQL Injection koruması ve Performans
# Asla string birleştirme (f-string vb.) ile SQL sorgusu yazılmaz. Güvenlik açığı yaratır.
# Bunun yerine '?' parametreleri kullanılır. Ayrıca binlerce satır veriyi tek tek eklemek yerine
# 'executemany' ile toplu (batch) ekleme yapmak performansı inanılmaz derecede artırır.
insert_query = """
INSERT INTO satislar (urun_adi, kategori, satis_miktari, birim_fiyat, satis_tarihi)
VALUES (?, ?, ?, ?, ?)
"""

try:
    cursor.executemany(insert_query, kayitlar)
    conn.commit()
    print(f"{cursor.rowcount} adet kayıt başarıyla veritabanına eklendi.")
except sqlite3.Error as e:
    conn.rollback() # Hata olursa işlemleri iptal et
    print(f"Veritabanı hatası oluştu: {e}")

# SQL ile veri analizi
# İncelik: Toplama/Çarpma gibi işlemleri Python (Pandas) yerine doğrudan SQL'de yapmak 
# (Eğer veritabanı çok büyükse) çok daha performanslıdır. Buna "Pushdown Computation" denir.

analiz_sorgusu = """
SELECT 
    kategori, 
    SUM(satis_miktari) as toplam_satilan_urun,
    SUM(satis_miktari * birim_fiyat) as toplam_ciro
FROM 
    satislar
GROUP BY 
    kategori
ORDER BY 
    toplam_ciro DESC;
"""

cursor.execute(analiz_sorgusu)
rapor = cursor.fetchall()

print("\n--- KATEGORİ BAZLI CİRO RAPORU ---")
for satir in rapor:
    kategori = satir[0]
    miktar = satir[1]
    ciro = satir[2]
    print(f"Kategori: {kategori} | Satılan Ürün: {miktar} | Toplam Ciro: {ciro:,.2f} TL")

# İşi bitince bağlantıları kapatmayı unutmuyoruz (Kaynak yönetimi)
cursor.close()
conn.close()