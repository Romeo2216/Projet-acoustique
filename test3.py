import sqlite3
import numpy as np

# Connexion à SQLite
conn = sqlite3.connect("arrays.db")
cursor = conn.cursor()

# Création d'une table avec une colonne BLOB
cursor.execute("""
CREATE TABLE IF NOT EXISTS Arrays (
    id INTEGER PRIMARY KEY,
    array BLOB
)
""")

# Exemple de tableau numpy 2D
array_2d = np.random.rand(3, 3)

# Conversion du tableau en binaire
array_blob = array_2d.tobytes()

# Insertion dans la base de données
cursor.execute("INSERT INTO Arrays (array) VALUES (?)", (array_blob,))
conn.commit()

# Récupération du tableau
cursor.execute("SELECT array FROM Arrays WHERE id = 1")
retrieved_blob = cursor.fetchone()[0]

# Reconstruction du tableau
retrieved_array = np.frombuffer(retrieved_blob, dtype=array_2d.dtype).reshape(array_2d.shape)

# Vérification
print("Original Array:")
print(array_2d)
print("Retrieved Array:")
print(retrieved_array)
print(f"Are they equal? {np.array_equal(array_2d, retrieved_array)}")

conn.close()
