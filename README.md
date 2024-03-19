## Real-Time Stock Price Checker

This Python-based application is designed to asynchronously check real-time stock prices from the Alpha Vantage API. It provides a convenient Command Line Interface (CLI) for users to retrieve up-to-date stock information.

### Prerequisites

Before using the application, ensure you have the following installed:

- Python 3.x
- Poetry (optional but recommended for managing dependencies)
- Alpha Vantage API key (sign up for a free API key on the Alpha Vantage website)

### Installation

To install and run the application, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/AliHezarpisheh/async-stock-price-checker.git
   ```

2. Navigate to the project directory:

   ```bash
   cd real-time-stock-price-checker
   ```

3. Install dependencies using Poetry (recommended):

   ```bash
   poetry install
   ```

   Alternatively, you can create a virtual environment and install the requirements using pip:

   ```bash
   python -m venv venv
   source venv/bin/activate (for Unix-based systems)
   venv\Scripts\activate (for Windows)
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project directory and add your Alpha Vantage API key:

   ```plaintext
   ALPHAVANTAGE_API_KEY=your_api_key_here
   ```

### Usage

Once the installation is complete and the API key is set, you can run the application using the following command:

```bash
python run.py
```

Follow the on-screen instructions to interact with the CLI and retrieve real-time stock prices.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

- Thanks to Alpha Vantage for providing the API used in this application.