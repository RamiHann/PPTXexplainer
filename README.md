```markdown
# GPT-Explainer Project

## Overview

The GPT-Explainer project is designed to explain PowerPoint presentations using the GPT-3.5 AI model. The project includes functionality for uploading presentations, processing them asynchronously, and retrieving explanations. The system uses an SQLite database to manage users and uploads, ensuring efficient data handling and maintainability.

## Requirements

### Prerequisites

- Python 3.7+
- `pip` (Python package installer)

### Python Packages

Install the required packages using `pip`:
```sh
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root of your project with the following content:
```plaintext
OPENAI_API_KEY=your_openai_api_key_here
```

## Setup

### Database Setup

Initialize the SQLite database by running the following command:
```sh
python database.py
```

This will create the necessary tables (`Users` and `Uploads`) in the database.

## Running the Application

### Start the Flask Server

To start the Flask server, run:
```sh
python app.py
```

### Run the Explainer

To start processing new uploads, run:
```sh
python explainer.py
```

## Usage

### Python Client

The Python client (`client.py`) allows you to upload files, check status, and retrieve upload history.

#### Upload a File
To upload a file with an optional email:
```sh
python client.py upload path/to/your/presentation.pptx your-email@example.com
```

#### Check Status by UID
To check the status of an upload by UID:
```sh
python client.py status <uid>
```

#### Get Upload History by Email
To retrieve the upload history for a given email:
```sh
python client.py history your-email@example.com
```

## Project Structure

```plaintext
.
├── app.py                # Flask server for handling uploads and status checks
├── client.py             # Python client for interacting with the server
├── database.py           # Database setup and ORM definitions
├── explainer.py          # Script for processing uploaded presentations
├── gpt_explainer.py      # Module for interacting with OpenAI GPT-3.5
├── extract_txt.py        # Module for extracting text from presentations
├── to_json.py            # Module for saving explanations to JSON
├── requirements.txt      # Python package dependencies
├── .env                  # Environment variables (not included in version control)
└── README.md             # This README file
```

## Notes

- Ensure you have a valid OpenAI API key in your `.env` file.
- Always run `setup_database` before starting the Flask server to ensure the database is initialized.
- Check the logs in the `logs` folder for detailed information on processing and errors.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [OpenAI](https://www.openai.com/) for providing the GPT-3.5 model.
- [SQLAlchemy](https://www.sqlalchemy.org/) for the ORM.
- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [python-pptx](https://python-pptx.readthedocs.io/) for parsing PowerPoint files.

## Good Luck!

![Good Luck](https://i.imgflip.com/1pz4wb.jpg)
```

