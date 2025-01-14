from fastapi import APIRouter, HTTPException
from vitibrasilscraper import VitibrasilScraper

router = APIRouter()

@router.get('/processing/{year}', summary='Processing')
async def v1_get_processing(year):
    try:
        v1_get_processing_scraper = VitibrasilScraper(year=int(year))
        v1_get_processing_df = v1_get_processing_scraper.get_processing()
        return v1_get_processing_df
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid value for year: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")