# StoreAPI
This project is a FastAPI application for managing products. It provides endpoints for creating, retrieving, updating, and deleting products. Besides FastAPI, it was built using SQLAlchemy, Pydantic, Docker, and MongoDB, using TDD with Pytest.

## Requirements
- Python 3.12
- Docker
- Poetry

## Installation
1. Clone this repository:
```bash
git clone https://github.com/JoaoBarroso4/StoreAPI.git
```
2. Navigate to the project's root directory.
3. Install the required dependencies
```bash
poetry install
```
4. Create a `.env` file in the root directory and add the following environment variables:
```bash
DATABASE_URL=<your_db_url>
```
5. Run docker-compose to start the MongoDB container
```bash
docker-compose up -d
```
6. Run the application
```bash
poetry run uvicorn store.main:app --reload
```
The server will start running at `http://localhost:8000`. Docs at `http://localhost:8000/docs`.

## Endpoints
- `POST /products/`: Create a new product.
- `GET /products/{product_id}`: Retrieve a product by its ID.
- `GET /products/`: Retrieve all products.
- `PATCH /products/{product_id}`: Update a product by its ID.
- `DELETE /products/{product_id}`: Delete a product by its ID.

## Testing

To run the tests, use the following command:
```bash
poetry run pytest
```
