from typing import Optional

from fastapi import FastAPI, Query, Path, File, UploadFile, Depends, HTTPException, status
from pydantic import BaseModel

from .monitor_manager import MonitorManager
from .health_monitor import HealthMonitor


app = FastAPI()
mm = MonitorManager()


@app.post('/api/register/{monitor_name}')
async def register_monitor(
    monitor_name: str = Path(min_length=2, max_length=20)
):
    mm.register(
        HealthMonitor(),
        monitor_name
    )
    return {'monitor_name': monitor_name, 'message': 'Successfuly registred.'}


@app.put('/api/update/{monitor_name}')
async def update_monitor(
    monitor_name: str = Path(min_length=2, max_length=20)
):
    mm.update(monitor_name)


@app.delete('/api/unregister/{monitor_name}')
async def unregister_monitor(
    monitor_name: str = Path(min_length=2, max_length=20)
):
    mm.unregister(monitor_name)
    return {'monitor_name': monitor_name, 'message': 'Successfuly unregistred.'}
