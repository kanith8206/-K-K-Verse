from pydantic import BaseModel
from typing import Optional, Literal

class UserProfile(BaseModel):
    id: str
    name: str
    email: str
    role: str
    avatar: str
    department: str

class Customer(BaseModel):
    id: str
    name: str
    email: str
    segment: Literal['Enterprise', 'Mid-Market', 'SMB']
    clv: float
    retentionScore: float  # 0-100
    loyaltyTier: Literal['Platinum', 'Gold', 'Silver', 'Bronze']
    region: Literal['North America', 'Europe', 'APAC', 'LATAM']
    tenureMonths: int
    monthlySpend: float
    lastActive: str
    churnProbability: Optional[float] = None
    activityTrend: Literal['Upward', 'Stable', 'Declining']

class Product(BaseModel):
    id: str
    name: str
    category: Literal['Software License', 'Cloud Storage', 'Consulting', 'Hardware', 'Support']
    price: float
    cost: float
    stock: int
    minStockThreshold: int
    warehouseLocation: str
    status: Literal['In Stock', 'Low Stock', 'Out of Stock']

class Sale(BaseModel):
    id: str
    customerId: str
    customerName: str
    productId: str
    productName: str
    quantity: int
    totalRevenue: float
    totalCost: float
    profit: float
    saleDate: str  # YYYY-MM-DD
    region: Literal['North America', 'Europe', 'APAC', 'LATAM']
    salesRep: str

class InventoryItem(Product):
    movementVelocity: Literal['Fast', 'Medium', 'Slow']
    lastReplenished: str

class BusinessKPIs(BaseModel):
    totalRevenue: float
    totalProfit: float
    profitMargin: float
    totalCustomers: int
    activeProductsCount: int
    churnRiskCount: int
