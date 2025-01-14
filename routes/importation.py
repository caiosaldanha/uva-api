from fastapi import APIRouter, HTTPException
from vitibrasilscraper import VitibrasilScraper

router = APIRouter()

@router.get('/importation/{year}', summary='Importation')
async def v1_get_importation(year):
    try:
        v1_get_importation_scraper = VitibrasilScraper(year=int(year))
        v1_get_importation_df = v1_get_importation_scraper.get_importation()
        return v1_get_importation_df
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid value for year: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")