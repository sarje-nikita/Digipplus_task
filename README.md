# Digipplus_task

## Digipplus Internship Task Submission

### Description:

This code is designed to scrape Google My Business (GMB) data from Google Maps based on a list of cities `city_list.json` and business categories `business_list.json`. The objective is to gather information about businesses in the specified cities and categories and store the data in the `Businesses.xlsx` file.

### Steps to Execute:

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/sarje-nikita/Digipplus_task.git
    cd Digipplus_task
    ```

2. **Create a New Virtual Environment:**

    - **For Windows:**
        ```bash
        python -m venv venv
        ```

    - **For Linux and macOS:**
        ```bash
        python3 -m venv venv
        ```

3. **Activate the Virtual Environment:**

    - **For Windows:**
        ```bash
        .\venv\Scripts\activate
        ```

    - **For Linux and macOS:**
        ```bash
        source venv/bin/activate
        ```

4. **Install Playwright:**
    ```bash
    pip install playwright
    playwright install
    ```

5. **Install Pandas:**
    ```bash
    pip install pandas
    ```

6. **Install Openpyxl:**
    ```bash
    pip install openpyxl
    ```

Now you are all set now run main.py . Happy coding!
