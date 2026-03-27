# FastAPI Notes & Action Items Application

A FastAPI-based web application for managing notes and extracting action items. The application uses SQLite for data persistence and provides both rule-based and LLM-powered action item extraction using Ollama.

## Project Overview

This application allows users to:
- Create and store notes in a SQLite database
- Retrieve all notes with timestamps
- Extract action items from notes using two methods:
  - **Rule-based extraction**: Pattern matching for bullet points, keywords, and imperative sentences
  - **LLM extraction**: Uses Llama 3.1 8B model via Ollama for intelligent action item extraction

The project follows a clean architecture with:
- **Backend**: FastAPI with modular routers
- **Database**: SQLite with connection pooling
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Testing**: Pytest test suite
- **Services**: Extraction logic with both heuristic and LLM approaches

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── db.py                # Database connection management
│   ├── schemas.py           # Pydantic models
│   ├── routers/
│   │   ├── notes.py         # Notes endpoints
│   │   └── action_items.py  # Action items endpoints
│   └── services/
│       └── extract.py       # Action item extraction logic
├── frontend/
│   └── index.html           # Frontend UI
├── tests/
│   └── test_extract.py      # Test suite
├── data/                    # SQLite database directory
└── README.md
```

## Prerequisites

- **Python**: 3.8 or higher
- **Conda**: Miniconda or Anaconda
- **Ollama**: (Optional) Required only for LLM-based extraction

## Setup Instructions

### 1. Create Conda Environment

```bash
# Create a new conda environment
conda create -n fastapi-notes python=3.11 -y

# Activate the environment
conda activate fastapi-notes
```

### 2. Install Dependencies

```bash
# Install FastAPI and related packages
pip install fastapi uvicorn python-dotenv

# Install Ollama client (for LLM extraction)
pip install ollama

# Install testing dependencies
pip install pytest httpx
```

### 3. Set Up Ollama (Optional - for LLM extraction)

If you want to use LLM-based action item extraction:

```bash
# Install Ollama from https://ollama.ai

# Pull the Llama 3.1 model
ollama pull llama3.1:8b

# Verify Ollama is running
ollama list
```

### 4. Environment Configuration

Create a `.env` file in the project root (optional - for future configurations):

```bash
# Add any environment variables here
# DATABASE_PATH=./data/notes.db
```

### 5. Initialize Database

The database will be automatically created when you first run the application. The SQLite database file will be stored in the `data/` directory.

## Running the Application

### Start the FastAPI Server

```bash
# Make sure you're in the project root directory
# Activate your conda environment
conda activate fastapi-notes

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`

### Access the Application

- **Frontend UI**: Open `http://localhost:8000` in your browser
- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative API Docs**: `http://localhost:8000/redoc` (ReDoc)

## API Endpoints

### Notes Endpoints

#### 1. Create Note
- **POST** `/notes`
- **Description**: Create a new note
- **Request Body**:
  ```json
  {
    "content": "Your note content here"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "content": "Your note content here",
    "created_at": "2024-01-15T10:30:00"
  }
  ```

#### 2. Get All Notes
- **GET** `/notes`
- **Description**: Retrieve all notes ordered by creation date (newest first)
- **Response**:
  ```json
  [
    {
      "id": 1,
      "content": "Note content",
      "created_at": "2024-01-15T10:30:00"
    }
  ]
  ```

### Action Items Endpoints

#### 3. Extract Action Items (Rule-based)
- **POST** `/action-items/extract`
- **Description**: Extract action items using pattern-matching rules
- **Request Body**:
  ```json
  {
    "text": "- Buy groceries\n- Schedule meeting\nTODO: Review code"
  }
  ```
- **Response**:
  ```json
  {
    "action_items": [
      "Buy groceries",
      "Schedule meeting",
      "Review code"
    ]
  }
  ```

#### 4. Extract Action Items (LLM)
- **POST** `/action-items/extract-llm`
- **Description**: Extract action items using Llama 3.1 via Ollama
- **Request Body**:
  ```json
  {
    "text": "We need to finalize the design and implement the new feature."
  }
  ```
- **Response**:
  ```json
  {
    "action_items": [
      "Finalize the design",
      "Implement the new feature"
    ]
  }
  ```
- **Note**: Requires Ollama with llama3.1:8b model

## Action Item Extraction Logic

### Rule-based Extraction ([`extract_action_items`](app/services/extract.py))

Identifies action items by:
- Bullet points (-, *, •, numbered lists)
- Keywords: "TODO:", "Action:", "Next:"
- Checkbox markers: "[ ]", "[todo]"
- Imperative verbs: add, create, implement, fix, update, etc.

### LLM Extraction ([`extract_action_items_llm`](app/services/extract.py))

Uses Llama 3.1 8B model to:
- Understand context and intent
- Extract implicit action items
- Handle complex sentence structures
- Return structured JSON output

## Running Tests

### Run All Tests

```bash
# Activate conda environment
conda activate fastapi-notes

# Run pytest
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=app --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/test_extract.py -v
```

### Test Structure

The test suite ([`tests/test_extract.py`](tests/test_extract.py)) covers:
- Rule-based action item extraction
- Edge cases and empty inputs
- Deduplication logic
- Imperative sentence detection
- LLM extraction (if Ollama is available)

## Frontend Features

The [`frontend/index.html`](frontend/index.html) provides:
- **Create Note**: Form to submit new notes
- **List Notes**: Button to fetch and display all notes
- **Extract Action Items**: Interface to extract action items from text
- **Method Selection**: Toggle between rule-based and LLM extraction

## Database Schema

### Notes Table
```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Troubleshooting

### Database Issues
```bash
# If database gets corrupted, delete and restart
rm data/notes.db
# Restart the server to recreate
```

### Ollama Connection Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama service
ollama serve
```

### Port Already in Use
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
```

## Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document functions with docstrings

### Adding New Endpoints
1. Create/modify routers in [`app/routers/`](app/routers/)
2. Update [`app/main.py`](app/main.py) to include the router
3. Add corresponding tests in [`tests/`](tests/)

## Future Enhancements

- User authentication
- Note editing and deletion
- Tagging system
- Export functionality
- Search and filtering
- Task status tracking

## License

This project is for educational purposes as part of Modern Software Development assignments.

## Contact

For issues or questions, please refer to the course materials or contact the instructor.
```