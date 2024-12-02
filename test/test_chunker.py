import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
from scripts.preprocessing import process_documents

class TestProcessDocuments(unittest.TestCase):

    @patch('scripts.preprocessing.os.listdir')
    @patch('scripts.preprocessing.open', new_callable=mock_open)
    @patch('scripts.preprocessing.parse_html')
    @patch('scripts.preprocessing.extract_main_content')
    @patch('scripts.preprocessing.clean_text')
    @patch('scripts.preprocessing.fixed_length_chunking')
    @patch('scripts.preprocessing.create_chunk_metadata')
    def test_process_documents(self, mock_create_metadata, mock_fixed_length_chunking, mock_clean_text, 
                               mock_extract_content, mock_parse_html, mock_open, mock_listdir):
        # Setup mock return values
        mock_listdir.return_value = ['test.html']
        mock_parse_html.return_value = MagicMock()
        mock_extract_content.return_value = 'Main content'
        mock_clean_text.side_effect = lambda x: x  # Return the input as is
        mock_fixed_length_chunking.return_value = [{'content': 'Chunk 1', 'heading': 'Heading 1'}]
        mock_create_metadata.return_value = {'document_id': 'test', 'index': 0, 'heading': 'Heading 1'}

        # Call the function
        process_documents('input_dir', 'output_file.jsonl')

        # Check if the file was opened correctly
        mock_open.assert_called_once_with('output_file.jsonl', 'w', encoding='utf-8')

        # Check if the correct data was written to the file
        handle = mock_open()
        handle.write.assert_called_once_with('{"text": "Chunk 1", "document_id": "test", "index": 0, "heading": "Heading 1"}\n')

if __name__ == '__main__':
    unittest.main()
