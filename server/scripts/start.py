def run():
    import subprocess
    
    subprocess.run(args="uvicorn src.main:app --host 0.0.0.0 --port 8000 --loop asyncio", shell=True)