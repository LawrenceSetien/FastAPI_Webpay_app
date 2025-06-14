# Transbank Payment Integration

A simple payment application using Transbank's Webpay Plus integration with FastAPI.

## Setup

1. Create and activate a virtual environment:

For Linux/Mac:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy and rename `example.env` to `.env` file in the root directory with your own variables.


4. Run the application:
```bash
uvicorn app.main:app --reload --log-level debug
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development Mode

This application uses Transbank's test environment by default. For testing, you can use the following test cards:

- Redcompra ok: 4511 3466 6003 7060
- Redcompra Error: 5186 0085 4123 3829

- Credentials:
  - RUT: 11.111.111-1
  - Pass: 123

## Deactivating the Virtual Environment

When you're done working on the project, you can deactivate the virtual environment:

```bash
deactivate
``` 
