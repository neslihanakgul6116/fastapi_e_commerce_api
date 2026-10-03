from database import SessionLocal, engine, Base
from models import Category, Product

# Tabloları oluştur
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Eski verileri temizle
try:
    db.query(Product).delete()
    db.query(Category).delete()
    db.commit()
except Exception:
    db.rollback()

# Kategorileri Ekle
cat_elektronik = Category(name="Elektronik", slug="elektronik")
cat_giyim = Category(name="Giyim & Moda", slug="giyim")
cat_ev = Category(name="Ev & Yaşam", slug="ev-yasam")
cat_aksesuar = Category(name="Aksesuar", slug="aksesuar")

db.add_all([cat_elektronik, cat_giyim, cat_ev, cat_aksesuar])
db.commit()

# Örnek Ürünleri Ekle
products = [
    Product(
        name="Kablosuz Bluetooth Kulaklık", 
        description="Yüksek ses kalitesi ve uzun pil ömrü.", 
        price=1299.90, 
        stock=15, 
        image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60", 
        category=cat_elektronik
    ),
    Product(
        name="Akıllı Saat ve Spor Bileklik", 
        description="Nabız ölçer, adım sayar ve bildirim desteği.", 
        price=2499.00, 
        stock=10, 
        image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=60", 
        category=cat_elektronik
    ),
    Product(
        name="Oversize Siyah Hoodie", 
        description="İç kısmı şardonlu, %100 pamuklu rahat kesim.", 
        price=799.90, 
        stock=25, 
        image_url="https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500&auto=format&fit=crop&q=60", 
        category=cat_giyim
    ),
    Product(
        name="Klasik Bomber Ceket", 
        description="Sezonun trend dış giyim ürünü.", 
        price=1599.00, 
        stock=8, 
        image_url="https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&auto=format&fit=crop&q=60", 
        category=cat_giyim
    ),
    Product(
        name="Çelik Termos Bardak 500ml", 
        description="12 saat sıcak ve soğuk tutma özellikleri.", 
        price=450.00, 
        stock=30, 
        image_url="https://images.unsplash.com/photo-1513694203232-719a280e022f?w=500&auto=format&fit=crop&q=60", 
        category=cat_ev
    ),
    Product(
        name="Deri Minimalist El Çantası", 
        description="Şık tasarım, günlük kullanıma uygun.", 
        price=899.90, 
        stock=12, 
        image_url="https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=500&auto=format&fit=crop&q=60", 
        category=cat_aksesuar
    )
]

db.add_all(products)
db.commit()
db.close()

print("Veritabanı sıfırdan kuruldu ve ürünler eklendi!")