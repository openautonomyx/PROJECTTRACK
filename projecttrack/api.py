from fastapi import FastAPI

app = FastAPI(title='PROJECTTRACK API')


@app.get('/')
def root():
    return {
        'service': 'PROJECTTRACK',
        'status': 'running'
    }


@app.get('/health')
def health():
    return {
        'ok': True,
        'service': 'PROJECTTRACK'
    }
