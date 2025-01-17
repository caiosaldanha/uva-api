# imports ===================
# fastapi
from fastapi import FastAPI, HTTPException, APIRouter
from services.vitibrasilscraper import VitibrasilScraper
# routes
from routes.welcome import router as welcome_router
from routes.production import router as production_router
from routes.processing import router as processing_router
from routes.commercialization import router as commercialization_router
from routes.importation import router as importation_router
from routes.exportation import router as exportation_router


# metadata ===================
# description
description = """
This API performs an online data retrieval of Wine, Juice and Derivative production from Brasil. 🍇

## Items

- **Production** - Production of wines, juices, and derivatives from Rio Grande do Sul

- **Processing** - Quantity of grapes processed in Rio Grande do Sul
  - Vinifera, 
  - American and Hybrid grapes
  - Table grapes
  - Unclassified

- **Commercialization** - Commercialization of wines and derivatives in Rio Grande do Sul

- **Importation** - Importation of grape derivatives
  - Table wines
  - Sparkling wines
  - Fresh grapes
  - Raisins
  - Grape juice

- **Exportation** - Exportation of grape derivatives
  - Table wines
  - Sparkling wines
  - Fresh grapes
  - Grape juice


## Users

You will be able to:

* **Retrieve a dataframe** for each item - already with all subitems.
* **Retrieve yearly data** of each item from 1970 to 2023.

## Details
"""
# tags
tags_metadata = [
    {
        'name': 'Welcome',
        'description': 'Information about the API'
    },
    {
        'name': 'Production',
        'description': 'Production of wines, juices, and derivatives from Rio Grande do Sul'
    },
    {
        'name': 'Processing',
        'description': 'Quantity of grapes processed in Rio Grande do Sul'
    },
    {
        'name': 'Commercialization',
        'description': 'Commercialization of wines and derivatives in Rio Grande do Sul'
    },
    {
        'name': 'Importation',
        'description': 'Importation of grape derivatives'
    },
    {
        'name': 'Exportation',
        'description': 'Exportation of grape derivatives'
    }
]

# app ===============================
app = FastAPI(
    title="UVA API",
    description=description,
    summary="by Caio Saldanha",
    version="1.0.0",
    terms_of_service="http://caiosaldanha.com/uvaapi/termsofservice",
    contact={
        "name": "Caio Saldanha",
        "url": "https://caiosaldanha.com",
        "email": "hello@caiosaldanha.com",
    },
    license_info={
        "name": "License - Apache 2.0",
        "identifier": "MIT",
    },
    openapi_tags=tags_metadata,
    root_path="/api",  # Match the Nginx proxy path
    docs_url="/docs",  # Keep the default or customize if needed
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# routes ==========================
app.include_router(welcome_router, tags=['Welcome'])
app.include_router(production_router, prefix="/v1", tags=['Production'])
app.include_router(processing_router, prefix="/v1", tags=['Processing'])
app.include_router(commercialization_router, prefix="/v1", tags=['Commercialization'])
app.include_router(importation_router, prefix="/v1", tags=['Importation'])
app.include_router(exportation_router, prefix="/v1", tags=['Exportation'])