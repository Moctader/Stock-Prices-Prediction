from pathlib import Path
import uvicorn
from fastapi.responses import RedirectResponse
from app.core.registrar import register_app

app = register_app()


@app.get("/metrics")
def metrics():
    return {"message": "Metrics endpoint"}


@app.get("/")
async def home():
    return RedirectResponse(url="/docs")


if __name__ == '__main__':
    try:
        config = uvicorn.Config(
            app=f'{Path(__file__).stem}:app', reload=True, host="0.0.0.0", port=8089)
        server = uvicorn.Server(config)
        server.run()
    except Exception as e:
        raise e
