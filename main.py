# flask kütüphanesinden Flask sınıfını getir
from flask import Flask, render_template, request, redirect, session

import sqlite3

# bir tanke Flask nesnesi oluştur
# app isimli değişkende sakla
app = Flask(__name__)
app.secret_key = "A13Fe"



@app.route("/")   # Ana sayfa açıldığında ne yapayım?
def hello_world():
    if "ad" in session :
        return render_template("index.html")
    else:
        return render_template("login.html")
    
@app.route("/cikis")  
def cikis():
    session["ad"] = None
    session["sifre"] = None
    return redirect("/login")


@app.route("/kaydol")   # 
def kaydol():
    return render_template('kaydol.html')

@app.route("/kayitbilgileri", methods=["POST"])   # 
def kayit():
    isim = request.form["isim"]
    email = request.form["email"]
    sifre = request.form["sifre"]

    baglanti = sqlite3.connect("veriler.db")
    sorgu = f"SELECT * FROM kullanicilar WHERE ad='{isim}' "
    imlec = baglanti.cursor()
    imlec.execute(sorgu)
    # sorgu sonucu gelen kayitlar
    kayitlar = imlec.fetchall()
    if len(kayitlar) == 0: 
        sorgu = f"INSERT INTO kullanicilar VALUES('{isim}', '{email}', '{sifre}')"
        imlec.execute(sorgu)
        baglanti.commit()
        return render_template("index.html")
    else:
        return render_template("kaydol.html", hata="Bu kullanıcı zaten kayıtlı")

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/loginbilgileri", methods=["POST"])   # 
def login_kontrol():
    isim = request.form["isim"]
    sifre = request.form["sifre"]

    baglanti = sqlite3.connect("veriler.db")
    sorgu = f"SELECT * FROM kullanicilar WHERE ad='{isim}' AND sifre='{sifre}' "
    imlec = baglanti.cursor()
    imlec.execute(sorgu)
    # sorgu sonucu gelen kayitlar
    kayitlar = imlec.fetchall()
    baglanti.close()
    if len(kayitlar) == 0: 
        return render_template("login.html", hata="Kullanıcı bilgileri hatalı")
    else:
        session["ad"] = isim
        session["sifre"] = sifre
        return redirect("/")
    

@app.route("/urunler")   # 
def urunler():
    if "ad" in session and session["ad"]:
        baglanti = sqlite3.connect("veriler.db")
        sorgu = "SELECT * FROM urunler"
        imlec = baglanti.cursor()
        imlec.execute(sorgu)
        # sorgu sonucu gelen kayitlar
        kayitlar = imlec.fetchall()
        baglanti.close()
        return render_template("urunler.html", urunler=kayitlar)
    else:
        return redirect("/login")

#@app.route("/urunler/sil/<id>")   # 
#def urun_sil(id):
#    if "ad" in session and session["ad"]:    
#        baglanti = sqlite3.connect("veriler.db")
#        sorgu = f"DELETE FROM urunler WHERE id={int(id)}"
#        imlec = baglanti.cursor()
#        imlec.execute(sorgu)
#        
#        baglanti.close()
#        return redirect("/urunler")  
#    else:
#        return redirect("/login")

@app.route("/urunler/sil/<int:id>")   # int:id ekledik
def urun_sil(id):
    if "ad" in session and session["ad"]:    
        baglanti = sqlite3.connect("veriler.db")
        sorgu = f"DELETE FROM urunler WHERE id={id}"  # int(id) yerine direkt id kullanıyoruz
        imlec = baglanti.cursor()
        imlec.execute(sorgu)
        
        baglanti.commit()
        baglanti.close()
        return redirect("/urunler")  
    else:
        return redirect("/login")


@app.route("/urunler/guncelle/<int:id>")   # 
def urun_guncelle(id):
    if "ad" in session and session["ad"]:    
        baglanti = sqlite3.connect("veriler.db")
        sorgu = f"SELECT * FROM urunler WHERE id={id}"
        imlec = baglanti.cursor()
        imlec.execute(sorgu)
        # sorgu sonucu gelen kayitlar
        kayit = imlec.fetchone()
        baglanti.close()
        return render_template("urun_guncelle.html", urun=kayit)
    else:
        return redirect("/login")


@app.route("/urunler/guncelle", methods=["POST"])   # 
def urun_kaydet():
    if "ad" in session and session["ad"]:        
        id = request.form["id"]
        isbn = request.form["isbn"]
        isim = request.form["isim"]
        yazar = request.form["yazar"]
        fiyat = request.form["fiyat"]
        tur=request.form["tur"]
        resim = request.files["resim"]
        resim.save(f"static/resimler/{resim.filename}")
        baglanti = sqlite3.connect("veriler.db")
        sorgu = f"UPDATE urunler SET isbn='{isbn}', isim='{isim}', yazar='{yazar}',fiyat={float(fiyat)},tur='{tur}',resim='{resim.filename}'wHERE id={int(id)}"
        imlec = baglanti.cursor()
        imlec.execute(sorgu)
        # sorgu sonucu gelen kayitlar
        kayit = imlec.fetchone()
        baglanti.commit()
        baglanti.close()    
        return redirect("/urunler") 
    else:
        return redirect("/login")   

from flask import flash    
@app.route("/urunler/ekle", methods=["GET", "POST"])
def urun_ekle():
    if "ad" in session and session["ad"]:
        if request.method == "POST":
            isbn = request.form["isbn"]
            isim = request.form["isim"]
            yazar = request.form["yazar"]
            fiyat = request.form["fiyat"]
            tur = request.form["tur"]
            resim = request.files["resim"]

            baglanti = sqlite3.connect("veriler.db")
            sorgu = f"SELECT * FROM urunler WHERE isbn='{isbn}'"
            imlec = baglanti.cursor()
            imlec.execute(sorgu)
            kayitlar = imlec.fetchall()

            if kayitlar:
                flash("Bu ISBN numarasıyla ilişkilendirilmiş başka bir kitap zaten mevcut!", "hata")
            else:
                resim.save(f"static/resimler/{resim.filename}")
                sorgu = f"INSERT INTO urunler (isbn, isim, yazar, fiyat, tur, resim) VALUES ('{isbn}', '{isim}', '{yazar}', {float(fiyat)}, '{tur}', '{resim.filename}')"
                imlec.execute(sorgu)
                baglanti.commit()
                baglanti.close()
                return redirect("/urunler")

        return render_template("urun_ekle.html")
    else:
        return redirect("/login")
    

@app.route("/search", methods=["POST"])
def kitap_arama():
    if "ad" in session and session["ad"]:
        kitap_arama = request.form["kitap_arama"]
        baglanti = sqlite3.connect("veriler.db")
        sorgu = f"SELECT * FROM urunler WHERE isim LIKE '%{kitap_arama}%'"
        imlec = baglanti.cursor()
        imlec.execute(sorgu)
        kayitlar = imlec.fetchall()
        baglanti.close()
        return render_template("urunler.html", urunler=kayitlar)
    else:
        return redirect("/login")

app.run(debug=False)