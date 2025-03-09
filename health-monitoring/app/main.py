import time
import httpx
from fastapi import FastAPI, Response
from prometheus_client import Gauge
from prometheus_client import generate_latest
from prometheus_client.core import CollectorRegistry

registry = CollectorRegistry()

url_up = Gauge('sample_external_url_up', 'External URL availability (1=up, 0=down)', ['url'], registry=registry)
response_time = Gauge('sample_external_url_response_ms', 'External URL response time in milliseconds', ['url'], registry=registry)

URLS = ["https://httpstat.us/503", "https://httpstat.us/200"]


app = FastAPI(title="URL Monitoring Service")
    

async def check_url(url) -> tuple:
    try:
        start_time = time.time()
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
        
        end_time = time.time()
        
        response_ms = (end_time - start_time) * 1000
        
        if response.status_code == 200:
            url_up.labels(url=url).set(1)
        else:
            url_up.labels(url=url).set(0)
            
        response_time.labels(url=url).set(response_ms)
        
        return response.status_code, response_ms
    except Exception:
        url_up.labels(url=url).set(0)
        response_time.labels(url=url).set(0)
        return 0, 0

@app.get("/metrics")
async def metrics() -> Response:
    for url in URLS:
        await check_url(url)
    
    return Response(content=generate_latest(registry), media_type="text/plain")

@app.get("/")
async def home():
    return {"message": "URL Monitoring Service. Visit /metrics for Prometheus metrics."}
