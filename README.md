# Stock Inspect

## Introduction

Stock Inspect is a Streamlit web application designed for stock analysis. It uses the Language Model (Gemini-pro from google)  to provide insights based on user-provided stock names from NSE. 

## Installation

1. Clone the repository:

    ```bash
    git clone git@github.com:kailashsp/Stock_Inspect.git
    cd Stock_Inspect
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Setup env file
    1. Create a `.env` file in the root directory of the project.

    2. Add the following line to your `.env` file, replacing `YOUR_GOOGLE_API_KEY` with your actual Google API key:

        ```env
        GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
        ```


## Usage

1. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

2. The web application will open in your default browser.

3. Enter a stock symbol in the search box to analyze the stock.

## Components

### Libraries/Frameworks Used

- Pandas: Data manipulation and analysis.
- JSON: Data interchange format.
- Streamlit: Web application framework.
- Streamlit Searchbox: Extension for a searchable dropdown.

### Files

- `app.py`: Main Streamlit application.
- `document_preprocessor.py`: Module for generating stock fundamentals.
- `llm.py`: Module for the Language Model (LLM).
- `prompt.py`: Module containing the stock analysis prompt.
- `MCAP31122023.xlsx`: Excel file containing stock data.

## Configuration

- `streamlit_config.toml`: Configuration file for Streamlit settings.


## Acknowledgments

- Stock data provided by [Finology](https://finology.in/).


## License

This project is licensed under the [MIT License](LICENSE).
