import configparser
import pandas as pd


# Read the API key from the configuration file
config = configparser.ConfigParser()
config.read('../config.ini')
openai_api_key = config.get('openai', 'api_key')
cohere_api_key = config.get('cohere', 'api_key')

def embed_cohere(text):
    def embed_cohere(text):
        # Insert code here based on @embed_text_cohere.py
        # ...
        co = cohere.Client(cohere_api_key)
        response = co.embed(texts=[text], model='large', truncate='END')
        return response.embeddings[0]
    

def embed_chunks(chunks, model='cohere'):
    # Initialize variables
    embeddings = []

    # Iterate over the chunks
    for chunk in chunks:
        # Embed the chunk
        if model == 'cohere':
            embeddings.append(embed_cohere(chunk))
        elif model == 'openai':
            embeddings.append(embed_openai(chunk))

    return embeddings

def chunk_text_column(text_column, chunk_token_size):
    # Initialize variables
    chunks = []
    start_row = 0
    end_row = 0
    current_chunk = ""

    # Iterate over the text in the given column
    for text in text_column:
        # Check if the current chunk combined with the text from the current row exceeds the token size
        if len(current_chunk) + len(text) > chunk_token_size:
            # Add the current chunk to the list of chunks
            chunks.append(current_chunk)
            end_row += 1

            # Reset the current chunk and start a new one
            current_chunk = text
            start_row = end_row
        else:
            # Append the text from the current row to the current chunk
            current_chunk += text

    # Add the last chunk to the list of chunks
    chunks.append(current_chunk)
    end_row += 1

    # Create a new DataFrame to store the chunked data
    chunked_df = pd.DataFrame({'chunk': chunks, 'start_row': start_row, 'end_row': end_row})

    return chunked_df


def chunk_embed_transcript(args):
    # Read the CSV file into a pandas DataFrame
    transcript_df = pd.read_csv(args.csv_file)

    # Chunk the transcript
    chunk_df = chunk_text_column(transcript_df['text'], args.chunk_token_size)

    # Embed the chunks
    chunk_df['embedding'] = embed_chunks(chunk_df['chunk'], args.embedding_model)



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Chunk and embed a transcript')
    parser.add_argument('csv_file', type=str, help='the CSV file containing the transcript')
    parser.add_argument('--chunk_token_size', type=int, default=256, help='the maximum number of tokens in a chunk')
    parser.add_argument('--embedding_model', type=str, default='cohere', choices=['cohere', 'openai'], help='the embedding model to use')

    args = parser.parse_args()

    chunk_embed_transcript(args)