# GST-bot

GST-bot is a Streamlit-based chatbot designed to resolve queries related to the Goods and Services Tax (GST) in India. It utilizes PDF documents to extract information and provides conversational interaction for users to ask questions. Powered by the RAG (Retrieval-Augmented Generation) framework, GST-bot delivers effective question answering by combining retrieval-based methods with generative capabilities.

## Getting Started

To run GST-bot locally, follow these steps:

1. Clone this repository to your local machine.

2. Install the required Python packages by running:

3. Make sure you have the necessary PDF documents related to GST available. You can either upload them using the provided interface or specify the file paths directly.

4. Run the Streamlit app by executing the following command:

5. Once the app is running, you can ask your GST-related queries in the text input field provided.

6. You would need to update the .env file with your own OpenAI API key. 

## Features

- **Upload Documents**: Users can upload PDF documents containing GST-related information.
- **Use Existing**: Users can choose to use already uploaded PDF documents related to GST.
- **Interactive Chat Interface**: Users can ask questions, and the chatbot responds with relevant information extracted from the uploaded documents.
- **Query Resolution**: GST-bot utilizes PDF parsing, text chunking, and embeddings to efficiently retrieve information and provide accurate responses.

## Code Structure

- `chatbot.py`: Main application file containing the Streamlit UI and backend logic.
- `README.md`: Documentation file providing information about the project.
- `pdfs_docs/`: Directory containing GST related PDF documents i.e. the existing knowledge base of the chatbot.

## Dependencies

- Streamlit: For building the user interface.
- PyPDF2: For extracting text from PDF documents.
- langchain: A custom library providing functionalities for text processing, embeddings, and conversation chains.
- dotenv: For loading environment variables (not used directly in this code snippet).
- OpenAI: Large Language Model used for Question Answering


## Contributors

- Kaustubh Rastogi ([My GitHub Profile](https://github.com/rastogi17))

