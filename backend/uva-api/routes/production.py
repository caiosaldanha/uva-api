from fastapi import APIRouter, HTTPException
from services.vitibrasilscraper import VitibrasilScraper

router = APIRouter()

@router.get('/production/{year}', summary='Production')
async def v1_get_production(year):
    try:
        v1_get_production_scraper = VitibrasilScraper(year=int(year))
        v1_get_production_df = v1_get_production_scraper.get_production()
        return v1_get_production_df
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid value for year: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.post('/production/{year}', summary='Production')
async def v1_get_production(year):
    try:
        v1_get_production_scraper = VitibrasilScraper(year=int(year))
        v1_get_production_df = v1_get_production_scraper.get_production()
        return v1_get_production_df
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid value for year: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")