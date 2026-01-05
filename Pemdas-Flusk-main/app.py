from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "database.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS diabetes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kode_provinsi INTEGER,
            nama_provinsi TEXT,
            kode_kabupaten_kota INTEGER,
            nama_kabupaten_kota TEXT,
            jumlah_penderita_dm INTEGER,
            satuan TEXT,
            tahun INTEGER
        )
    """)
    conn.commit() 
    conn.close()

init_db()

@app.route("/")
def index():
    conn = get_db()
    data = conn.execute("SELECT * FROM diabetes ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", data=data)

@app.route("/tambah", methods=["POST"])
def tambah():
    nama_provinsi = request.form["nama_provinsi"]
    nama_kabupaten_kota = request.form["nama_kabupaten_kota"]
    jumlah_penderita_dm = request.form["jumlah_penderita_dm"]
    tahun = request.form["tahun"]

    # optional
    kode_provinsi = request.form.get("kode_provinsi", 0)
    kode_kabupaten_kota = request.form.get("kode_kabupaten_kota", 0)
    satuan = request.form.get("satuan", "Orang")

    conn = get_db()
    conn.execute("""
        INSERT INTO diabetes
        (kode_provinsi, nama_provinsi, kode_kabupaten_kota,
         nama_kabupaten_kota, jumlah_penderita_dm, satuan, tahun)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        kode_provinsi, nama_provinsi, kode_kabupaten_kota,
        nama_kabupaten_kota, jumlah_penderita_dm, satuan, tahun
    ))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    nama_provinsi = request.form["nama_provinsi"]
    nama_kabupaten_kota = request.form["nama_kabupaten_kota"]
    jumlah_penderita_dm = request.form["jumlah_penderita_dm"]
    tahun = request.form["tahun"]

    # optional
    kode_provinsi = request.form.get("kode_provinsi", 0)
    kode_kabupaten_kota = request.form.get("kode_kabupaten_kota", 0)
    satuan = request.form.get("satuan", "Orang")

    conn = get_db()
    conn.execute("""
        UPDATE diabetes
        SET kode_provinsi=?,
            nama_provinsi=?,
            kode_kabupaten_kota=?,
            nama_kabupaten_kota=?,
            jumlah_penderita_dm=?,
            satuan=?,
            tahun=?
        WHERE id=?
    """, (
        kode_provinsi, nama_provinsi, kode_kabupaten_kota,
        nama_kabupaten_kota, jumlah_penderita_dm, satuan, tahun, id
    ))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/hapus/<int:id>", methods=["POST"])
def hapus(id):
    conn = get_db()
    conn.execute("DELETE FROM diabetes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True)
