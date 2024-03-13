# My Diet Manager

The **My Diet Manager** is a Streamlit web application designed to assist users in managing their diet by leveraging the power of Google's Generative AI technology. This application allows users to input prompts related to food and analyze images to calculate the total calories while providing details for each food item.

## Features

- **Diet Management**: Users can input prompts related to food, such as questions about the healthiness of a particular food item.

- **Image Analysis**: The application supports image upload for further analysis of food items. The AI model calculates the total calories and provides details for each food item within the image.

- **User-Friendly Interface**: The Streamlit-based user interface ensures a smooth and intuitive experience for users.

## Getting Started

Follow these steps to run the My Diet Manager:

1. Clone the repository:

    ```bash
    git clone https://github.com/defyingdemonprogram/QA-with-Multiple-PDF-langchain.git
    cd QA-with-Multiple-PDF-langchain
    cd FOOD_HEALTH
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:

    - Create a `.env` file in the project directory.
    - Add your Google API key to the `.env` file:

        ```env
        GOOGLE_API_KEY=your_api_key_here
        ```

4. Run the application:

    ```bash
    streamlit run app.py
    ```

## Usage

1. Launch the application using the provided Streamlit command.
2. Enter your food-related prompt in the input box.
3. Optionally, upload an image containing food items for analysis.
4. Click the "Tell me the total calories" button to receive AI-generated responses.
5. Explore the details provided by the AI assistant, including the total calories and specific information for each food item.

## Note

Ensure that you have a valid Google API key to enable the integration of Google's Generative AI features.

Feel free to customize and expand the functionalities of this My Diet Manager according to your specific needs.