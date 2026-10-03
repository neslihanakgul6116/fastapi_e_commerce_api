from fastapi import FastAPI, Depends, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models import Product, Category

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Basit bellek tabanlı sepet listesi
cart_items = []

# --- Ana Sayfa ve Arama (Search) ---
@app.get("/", response_class=HTMLResponse)
def home(request: Request, q: str = None, db: Session = Depends(get_db)):
    # Eğer arama kelimesi (q) varsa, ürün adında veya açıklamasında arama yap
    if q:
        products = db.query(Product).filter(Product.name.ilike(f"%{q}%")).all()
    else:
        products = db.query(Product).all()
    
    return templates.TemplateResponse(request, "index.html", {
        "request": request,
        "products": products,
        "selected_category": None,
        "search_query": q or "",
        "banner": {
            "title": "Seçili Ürünlerde %50'ye Varan Fırsatlar!",
            "subtitle": "Kaçırılmayacak indirimler seni bekliyor, hemen alışverişe başla.",
            "bg_color": "linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%)",
            "image_url": "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=600&auto=format&fit=crop&q=80"
        }
    })

# --- Kategori Sayfaları ---
@app.get("/elektronik", response_class=HTMLResponse)
def elektronik_page(request: Request, db: Session = Depends(get_db)):
    try:
        products = db.query(Product).join(Category).filter(Category.slug == "elektronik").all()
    except Exception:
        products = []
        
    return templates.TemplateResponse(request, "index.html", {
        "request": request,
        "products": products,
        "selected_category": "elektronik",
        "search_query": "",
        "banner": {
            "title": "Teknolojide Büyük İndirim: %50'ye Varan Fırsatlar!",
            "subtitle": "En yeni kulaklıklar, akıllı saatler ve elektronik aksesuarlar.",
            "bg_color": "linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)",
            "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80"
        }
    })

@app.get("/giyim", response_class=HTMLResponse)
def giyim_page(request: Request, db: Session = Depends(get_db)):
    try:
        products = db.query(Product).join(Category).filter(Category.slug == "giyim").all()
    except Exception:
        products = []
        
    return templates.TemplateResponse(request, "index.html", {
        "request": request,
        "products": products,
        "selected_category": "giyim",
        "search_query": "",
        "banner": {
            "title": "Sezonun Trend Modelleri Şimdi Satışta!",
            "subtitle": "Tarzınızı yansıtacak oversize hoodie, etek, gömlek ve kombinler.",
            "bg_color": "linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%)",
            "image_url": "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=600&auto=format&fit=crop&q=80"
        }
    })

@app.get("/ev-yasam", response_class=HTMLResponse)
def ev_yasam_page(request: Request, db: Session = Depends(get_db)):
    try:
        products = db.query(Product).join(Category).filter(Category.slug == "ev-yasam").all()
    except Exception:
        products = []
        
    return templates.TemplateResponse(request, "index.html", {
        "request": request,
        "products": products,
        "selected_category": "ev-yasam",
        "search_query": "",
        "banner": {
            "title": "Evinize Şıklık ve Konfor Katın",
            "subtitle": "Akıllı termoslar, ev dekorasyonu ve yaşam ürünleri.",
            "bg_color": "linear-gradient(135deg, #00b894 0%, #55efc4 100%)",
            "image_url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=600&auto=format&fit=crop&q=80"
        }
    })

@app.get("/aksesuar", response_class=HTMLResponse)
def aksesuar_page(request: Request, db: Session = Depends(get_db)):
    try:
        products = db.query(Product).join(Category).filter(Category.slug == "aksesuar").all()
    except Exception:
        products = []
        
    return templates.TemplateResponse(request, "index.html", {
        "request": request,
        "products": products,
        "selected_category": "aksesuar",
        "search_query": "",
        "banner": {
            "title": "Kombininizi Tamamlayacak Aksesuarlar",
            "subtitle": "Minimalist çantalar, cüzdanlar ve şık detaylar.",
            "bg_color": "linear-gradient(135deg, #f39c12 0%, #e67e22 100%)",
            "image_url": "https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=600&auto=format&fit=crop&q=80"
        }
    })

# --- Ürün Detay Sayfası ---
@app.get("/product/{product_id}", response_class=HTMLResponse)
def product_detail(request: Request, product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return HTMLResponse("Ürün bulunamadı", status_code=404)
        
    return templates.TemplateResponse(request, "product_detail.html", {
        "request": request,
        "product": product
    })

# --- Sepet API Rotaları ---
@app.post("/api/add-to-cart/{product_id}")
def add_to_cart(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return {"success": False, "message": "Ürün bulunamadı"}
    
    cart_items.append({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "image_url": product.image_url
    })
    return {"success": True, "message": f"{product.name} sepete eklendi!", "cart_count": len(cart_items)}

@app.get("/api/cart-count")
def cart_count():
    return {"count": len(cart_items)}

# --- Favoriler ve Sepet Sayfaları ---
@app.get("/favorites", response_class=HTMLResponse)
def favorites_page(request: Request):
    return templates.TemplateResponse(request, "favorites.html", {"request": request})

@app.get("/cart-page", response_class=HTMLResponse)
def cart_page(request: Request):
    formatted_cart = []
    for item in cart_items:
        formatted_cart.append({
            "product": {
                "id": item["id"],
                "name": item["name"],
                "price": item["price"],
                "image_url": item["image_url"]
            },
            "quantity": 1
        })
        
    return templates.TemplateResponse(request, "cart.html", {
        "request": request, 
        "cart_items": formatted_cart
    })

@app.get("/checkout", response_class=HTMLResponse)
def checkout_page(request: Request):
    return templates.TemplateResponse(request, "checkout.html", {
        "request": request,
        "cart_items": cart_items
    })