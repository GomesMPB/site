from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="OtimizaVenda API", description="API para otimização de vendas online")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Models for Sales Calculator
class SalesCalculation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    produto: str
    preco_custo: float
    impostos: float
    frete: float
    margem_desejada: float
    preco_venda: float
    lucro_bruto: float
    lucro_liquido: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SalesCalculationCreate(BaseModel):
    produto: str
    preco_custo: float
    impostos: float = 0.0
    frete: float = 0.0
    margem_desejada: float = 20.0

# Models for Niche Finder
class Niche(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nome: str
    categoria: str
    demanda: str
    competicao: str
    rentabilidade: str
    tendencia: str
    descricao: str

# Models for Supplier Finder
class Supplier(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nome: str
    categoria: str
    localizacao: str
    avaliacao: float
    produtos_principais: List[str]
    contato: str
    preco_minimo: str

# Models for Trend Analysis
class Trend(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    produto: str
    categoria: str
    crescimento: str
    volume_busca: str
    sazonalidade: str
    oportunidade: str

# Mock data
mock_niches = [
    {
        "id": "1",
        "nome": "Produtos para Pets",
        "categoria": "Animais",
        "demanda": "Alta",
        "competicao": "Média",
        "rentabilidade": "Alta",
        "tendencia": "Crescendo",
        "descricao": "Mercado em crescimento com foco em bem-estar animal"
    },
    {
        "id": "2", 
        "nome": "Fitness em Casa",
        "categoria": "Saúde",
        "demanda": "Muito Alta",
        "competicao": "Alta",
        "rentabilidade": "Média",
        "tendencia": "Estável",
        "descricao": "Equipamentos e acessórios para exercícios domésticos"
    },
    {
        "id": "3",
        "nome": "Produtos Sustentáveis",
        "categoria": "Eco-friendly",
        "demanda": "Crescendo",
        "competicao": "Baixa",
        "rentabilidade": "Alta",
        "tendencia": "Crescendo",
        "descricao": "Produtos ecológicos e sustentáveis para consumo consciente"
    },
    {
        "id": "4",
        "nome": "Tech Gadgets",
        "categoria": "Tecnologia",
        "demanda": "Alta",
        "competicao": "Muito Alta",
        "rentabilidade": "Baixa",
        "tendencia": "Estável",
        "descricao": "Gadgets e acessórios tecnológicos inovadores"
    }
]

mock_suppliers = [
    {
        "id": "1",
        "nome": "TechSupply Brasil",
        "categoria": "Eletrônicos",
        "localizacao": "São Paulo, SP",
        "avaliacao": 4.8,
        "produtos_principais": ["Smartphones", "Fones de Ouvido", "Capas"],
        "contato": "contato@techsupply.com.br",
        "preco_minimo": "R$ 500,00"
    },
    {
        "id": "2",
        "nome": "PetWorld Fornecedor",
        "categoria": "Pet Shop",
        "localizacao": "Rio de Janeiro, RJ",
        "avaliacao": 4.6,
        "produtos_principais": ["Ração", "Brinquedos", "Acessórios"],
        "contato": "vendas@petworld.com.br",
        "preco_minimo": "R$ 200,00"
    },
    {
        "id": "3",
        "nome": "EcoVerde Distribuidora",
        "categoria": "Sustentabilidade",
        "localizacao": "Curitiba, PR",
        "avaliacao": 4.9,
        "produtos_principais": ["Produtos Biodegradáveis", "Cosméticos Naturais"],
        "contato": "eco@ecoverde.com.br",
        "preco_minimo": "R$ 300,00"
    }
]

mock_trends = [
    {
        "id": "1",
        "produto": "Air Fryer",
        "categoria": "Eletrodomésticos",
        "crescimento": "+150%",
        "volume_busca": "500k/mês",
        "sazonalidade": "Baixa",
        "oportunidade": "Alta"
    },
    {
        "id": "2",
        "produto": "Plantas Artificiais",
        "categoria": "Decoração",
        "crescimento": "+80%",
        "volume_busca": "200k/mês",
        "sazonalidade": "Média",
        "oportunidade": "Média"
    },
    {
        "id": "3",
        "produto": "Produtos para Home Office",
        "categoria": "Trabalho",
        "crescimento": "+200%",
        "volume_busca": "800k/mês",
        "sazonalidade": "Baixa",
        "oportunidade": "Muito Alta"
    }
]

# Sales Calculator endpoints
@api_router.post("/calcular-vendas", response_model=SalesCalculation)
async def calcular_vendas(calculation: SalesCalculationCreate):
    try:
        # Calculate sales metrics
        custo_total = calculation.preco_custo + calculation.impostos + calculation.frete
        margem_decimal = calculation.margem_desejada / 100
        preco_venda = custo_total / (1 - margem_decimal)
        lucro_bruto = preco_venda - calculation.preco_custo
        lucro_liquido = preco_venda - custo_total
        
        # Create calculation object
        calc_dict = calculation.dict()
        calc_dict.update({
            "preco_venda": round(preco_venda, 2),
            "lucro_bruto": round(lucro_bruto, 2),
            "lucro_liquido": round(lucro_liquido, 2)
        })
        
        calc_obj = SalesCalculation(**calc_dict)
        
        # Save to database
        await db.sales_calculations.insert_one(calc_obj.dict())
        
        return calc_obj
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro no cálculo: {str(e)}")

@api_router.get("/historico-calculos", response_model=List[SalesCalculation])
async def get_calculation_history():
    try:
        calculations = await db.sales_calculations.find().sort("created_at", -1).limit(50).to_list(50)
        return [SalesCalculation(**calc) for calc in calculations]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar histórico: {str(e)}")

# Niche Finder endpoints
@api_router.get("/nichos", response_model=List[Niche])
async def get_niches(categoria: Optional[str] = None):
    try:
        niches = [Niche(**niche) for niche in mock_niches]
        if categoria:
            niches = [n for n in niches if n.categoria.lower() == categoria.lower()]
        return niches
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar nichos: {str(e)}")

# Supplier Finder endpoints
@api_router.get("/fornecedores", response_model=List[Supplier])
async def get_suppliers(categoria: Optional[str] = None, localizacao: Optional[str] = None):
    try:
        suppliers = [Supplier(**supplier) for supplier in mock_suppliers]
        if categoria:
            suppliers = [s for s in suppliers if categoria.lower() in s.categoria.lower()]
        if localizacao:
            suppliers = [s for s in suppliers if localizacao.lower() in s.localizacao.lower()]
        return suppliers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar fornecedores: {str(e)}")

# Trend Analysis endpoints
@api_router.get("/tendencias", response_model=List[Trend])
async def get_trends(categoria: Optional[str] = None):
    try:
        trends = [Trend(**trend) for trend in mock_trends]
        if categoria:
            trends = [t for t in trends if categoria.lower() in t.categoria.lower()]
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar tendências: {str(e)}")

# Health check
@api_router.get("/health")
async def health_check():
    return {"status": "ok", "message": "OtimizaVenda API funcionando perfeitamente!"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()