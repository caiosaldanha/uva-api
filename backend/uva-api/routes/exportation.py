from fastapi import APIRouter, HTTPException
from services.vitibrasilscraper import VitibrasilScraper

router = APIRouter()

@router.get('/exportation/{year}', summary='Exportation')
async def v1_get_exportation(year):
    try:
        v1_get_exportation_scraper = VitibrasilScraper(year=int(year))
        v1_get_exportation_df = v1_get_exportation_scraper.get_exportation()
        return v1_get_exportation_df
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid value for year: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.post('/exportation/{year}', summary='Exportation')
async def v1_get_exportation(year):
    try:
        v1_get_exportation_scraper = VitibrasilScraper(year=int(year))
        v1_get_exportation_df = v1_get_exportation_scraper.get_exportation()
        return v1_get_exportation_df
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid value for year: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")