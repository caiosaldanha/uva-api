from fastapi import APIRouter, HTTPException
from vitibrasilscraper import VitibrasilScraper

router = APIRouter()

@router.get('/commercialization/{year}', summary='Commercialization')
async def v1_get_commercialization(year):
    try:
        v1_get_commercialization_scraper = VitibrasilScraper(year=int(year))
        v1_get_commercialization_df = v1_get_commercialization_scraper.get_commercialization()
        return v1_get_commercialization_df
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid value for year: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")