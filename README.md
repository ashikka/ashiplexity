# Ashiplexity - Perplexity Clone

A Streamlit-based chat application that mimics Perplexity's interface and functionality using the Perplexity API with document-based Q&A.

## Features

- Clean, modern UI similar to Perplexity
- Document-based Q&A using local files
- Perplexity API integration
- Environment variable configuration
- Chat interface with message history
- Quick prompt buttons

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

1. Get your Perplexity API key from [Perplexity API Settings](https://www.perplexity.ai/settings/api)
2. Edit the `.env` file and replace `your_api_key_here` with your actual API key:

```env
PERPLEXITY_API_KEY=your_actual_api_key_here
```

### 3. Add Documents

Place your documents in the `documents/` folder. The app will automatically load all `.txt` files from this folder.

Example structure:

```
documents/
├── about_ashikka.txt
├── resume.txt
└── projects.txt
```

### 4. Run the Application

```bash
streamlit run main.py
```

The app will open in your default browser at `http://localhost:8501`

## Usage

1. **API Key**: The app automatically loads your API key from the `.env` file
2. **Documents**: All documents in the `documents/` folder are automatically loaded
3. **Ask Questions**: Type questions about the content in your documents
4. **Quick Prompts**: Use the predefined prompt buttons for common questions
5. **Chat History**: All conversations are preserved in the session

## Project Structure

```
ashiplexity/
├── main.py              # Main Streamlit application
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── .gitignore          # Git ignore rules
├── README.md           # This file
└── documents/          # Document folder
    └── about_ashikka.txt
```

## How It Works

1. **Document Loading**: The app loads all `.txt` files from the `documents/` folder
2. **Context Building**: When you ask a question, the app includes all document content as context
3. **API Integration**: Questions are sent to Perplexity API with document context
4. **Response Display**: AI responses are displayed in chat bubbles

## Troubleshooting

- **API Key Issues**: Make sure your `.env` file contains the correct API key
- **Document Loading**: Ensure documents are in the `documents/` folder and are `.txt` files
- **Import Errors**: Run `pip install -r requirements.txt` to install all dependencies
- **Port Issues**: If port 8501 is busy, Streamlit will automatically use the next available port

## Development

To modify the app:

1. Edit `main.py` to change functionality
2. Add documents to the `documents/` folder
3. Update `requirements.txt` if adding new dependencies
4. Restart the app with `streamlit run main.py`

## API Configuration

The app uses the Perplexity API with the `llama-2-70b-chat` model. You can modify the model and parameters in the `ask_perplexity_with_context` function in `main.py`.
