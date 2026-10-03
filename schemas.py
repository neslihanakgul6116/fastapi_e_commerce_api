from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# --- KATEGORİ ŞEMALARI ---
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    class Config:
        from_attributes = True


# --- ÜRÜN ŞEMALARI ---
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0, description="Fiyat sıfırdan büyük olmalıdır")
    stock: int = Field(ge=0, description="Stok negatif olamaz")
    category_id: int
    image_url: Optional[str] = None # <-- YENİ EKLENEN ALAN

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True


# --- SEPET ŞEMALARI ---
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, description="Miktar en az 1 olmalıdır")

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductResponse
    class Config:
        from_attributes = True


# --- FAVORİ ŞEMALARI ---
class FavoriteCreate(BaseModel):
    product_id: int

class FavoriteResponse(BaseModel):
    id: int
    product_id: int
    product: ProductResponse
    class Config:
        from_attributes = True


# --- YORUM ŞEMALARI ---
class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5, description="Puan 1 ile 5 arasında olmalıdır")
    comment: str

class ReviewResponse(ReviewCreate):
    id: int
    product_id: int
    created_at: datetime
    class Config:
        from_attributes = True


# --- KUPON ŞEMALARI ---
class CouponCreate(BaseModel):
    code: str
    discount_percent: float = Field(gt=0, le=100)

class CouponResponse(CouponCreate):
    id: int
    class Config:
        from_attributes = True


# --- ÖDEME VE SİPARİŞ ŞEMALARI ---
class CheckoutRequest(BaseModel):
    card_holder: str = Field(..., description="Kart üzerindeki isim")
    card_number: str = Field(..., min_length=16, max_length=16, description="16 haneli kart numarası")
    expiry_date: str = Field(..., description="SKT (Örn: 08/28)")
    cvv: str = Field(..., min_length=3, max_length=3, description="3 haneli güvenlik kodu")
    coupon_code: Optional[str] = None # İsteğe bağlı indirim kuponu

class OrderResponse(BaseModel):
    id: int
    total_amount: float
    status: str
    created_at: datetime
    class Config:
        from_attributes = True