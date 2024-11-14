# DataMine Streamlit App

**Description**:  
The **DataMine Streamlit App** allows users to select a county in Indiana and displays the map of the county, housing
market metrics specific to that area, and a time plot of the metrics. It’s an interactive and visual tool for exploring
housing data by county.

---

## Features

- Choose a county in Indiana to view housing market data.
- Interactive map visualization of the selected county.
- Display key metrics of the housing market (e.g., median house price, number of sales, etc.).
- Time plot showing trends in the housing metrics.

---

## Demo

![preview](/assets/preview.png)

---

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/JonathanJT109/data_mine_streamlit.git
    ```

2. **Navigate to the project folder**:
    ```bash
    cd data_mine_streamlit
    ```

3. **Create a Python environment**:
    - Run the following command to create a virtual environment:
      ```bash
      python -m venv venv
      ```

4. **Activate the virtual environment**:

    - **For Windows**:
      ```bash
      .\venv\Scripts\activate
      ```

    - **For Linux/macOS**:
      ```bash
      source venv/bin/activate
      ```

5. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

6. **Run the app**:
    ```bash
    streamlit run main.py
    ```

After running this command, open the provided URL (usually `http://localhost:8501`) in your browser to access the app.

---

## Technologies Used

- **Streamlit**: Used to create the interactive web app.
- **Pandas**: Used for data manipulation and analysis.
- **NumPy**: Used for numerical operations and handling large datasets.

---

## Folder Structure

```
/data_mine
  /venv              # Virtual environment folder
  /requirements.txt  # File listing Python dependencies
  main.py            # Main script to run the Streamlit app
  /server            # Server Requests
```

---

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to your branch (`git push origin feature-name`).
5. Submit a pull request with a detailed description of your changes.

Please ensure that your code follows Python style guidelines and that any new functionality is well-tested.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

TODO