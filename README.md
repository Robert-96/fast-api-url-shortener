# fast-api-url-shortener

A simple URL shortener demo app build with FastAPI.

## Development Setup

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run

To start the development server, run the following command:

```bash
uvicorn app.main:app --reload
```

Once the server is up and running, open <http://localhost:8000> in your browser. You can also access the Swagger UI documentation at <http://127.0.0.1:8000/docs>.

## License

This project is licensed under the [MIT License](LICENSE).
