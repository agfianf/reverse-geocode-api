from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.config import settings
from app.middlewares.error_response import handle_error_response
from app.repositories.reverse_geo import ReverseGeocodeRepositories
from app.routers.reverse_geo import router as reverse_geo_router
from app.services.reverse_geo import ReverseGeocodeService


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    print("Initializing resources...")
    reverse_geo_repo = ReverseGeocodeRepositories()
    reverse_geocode_service = ReverseGeocodeService(repo=reverse_geo_repo)
    yield {
        "reverse_geocode_service": reverse_geocode_service,
    }
    print("Cleaning up resources...")
    # cleanup


app = FastAPI(
    title=settings.APP_NAME,
    version=f"{settings.APP_VERSION}",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def root():  # noqa: ANN201
    return RedirectResponse("/docs")


@app.get("/health")
async def health():
    return {"status": "ok"}


app.add_exception_handler(HTTPException, handle_error_response)
app.add_exception_handler(RequestValidationError, handle_error_response)

app.include_router(reverse_geo_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG,
    )
