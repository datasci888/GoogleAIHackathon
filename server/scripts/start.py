def run():
    import subprocess

    subprocess.run(args="python -m streamlit run ./src/app.py --server.port=8501 --server.address=0.0.0.0", shell=True)