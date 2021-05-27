from os import path
from . import TestBase
from ml_text_assistant.assistant import Assistant
from ml_text_assistant.exploration import Explorer
import tempfile
import unittest
from unittest.mock import patch, Mock


class AssistantPDFTestCase(TestBase):

    def setUp(self):
        self.extractor_mock = Mock()
        self.extractor_mock.configure_mock(**{'text.return_value': 'my text'})
        self.assistant = Assistant(
            extractor=self.extractor_mock,
            preparator=Mock()
        )
        self.input_dir_path = self.get_resources('pdf')
        self.input_file_path = self.get_resource('pdf/3382494.3422167-cropped.pdf')

    @unittest.expectedFailure
    def test_output_path_should_be_a_directory(self):
        with tempfile.TemporaryFile() as output_as_file:
            self.assistant.pdf_to_text(
                self.input_file_path,
                output_as_file
            )

    @unittest.expectedFailure
    def test_input_path_should_exist(self):
        with tempfile.TemporaryDirectory() as output_as_dir:
            self.assistant.pdf_to_text(
                self.input_dir_path + 'any_inexistent_path',
                output_as_dir
            )

    def test_extract_text_from_file_to_inexistent_output(self):
        with tempfile.TemporaryDirectory() as output_as_dir:
            output = output_as_dir + '/any_inexistent_path/'
            self.assistant.pdf_to_text(
                self.input_file_path,
                output
            )
            self.assertFilesIn(['3382494.3422167-cropped.txt'], output)

    def test_extract_text_from_dir_to_existent_output(self):
        with tempfile.TemporaryDirectory() as output_as_dir:
            output = output_as_dir
            self.assistant.pdf_to_text(
                self.input_dir_path,
                output
            )
            expected_files = [
                '3382494.3422167-cropped.txt',
                '3382494.3422167.txt'
            ]
            self.assertFilesIn(expected_files, output)


class AssistantTextTestCase(TestBase):

    def setUp(self):
        self.preparator_mock = Mock()
        self.preparator_mock.configure_mock(**{'prepare.return_value': ['my', 'text']})
        self.assistant = Assistant(
            extractor=Mock(),
            preparator=self.preparator_mock
        )
        self.input_dir_path = self.get_resources('text')
        self.input_file_path = self.get_resource('text/3382494.3422167-cropped.txt')

    @unittest.expectedFailure
    def test_output_path_should_be_a_directory(self):
        with tempfile.TemporaryFile() as output_as_file:
            self.assistant.text_to_csv(
                self.input_file_path,
                output_as_file
            )

    @unittest.expectedFailure
    def test_input_path_should_exist(self):
        with tempfile.TemporaryDirectory() as output_as_dir:
            self.assistant.text_to_csv(
                self.input_dir_path + 'any_inexistent_path',
                output_as_dir
            )

    def test_create_dataset_into_inexistent_output(self):
        with tempfile.TemporaryDirectory() as output_as_dir:
            output = output_as_dir + '/any_inexistent_path/'
            self.assistant.text_to_csv(
                self.input_file_path,
                output
            )
            self.assertFilesIn(['dataset.csv'], output)

    def test_create_dataset_into_existent_output(self):
        with tempfile.TemporaryDirectory() as output_as_dir:
            output = output_as_dir
            self.assistant.text_to_csv(
                self.input_dir_path,
                output
            )
            expected_files = ['dataset.csv']
            self.assertFilesIn(expected_files, output)


class AssistantTestCase(TestBase):

    @patch.object(Explorer, "__init__", return_value=None)
    def test_create_explorer_for_provided_tokens(self, mock_init):
        assistant = Assistant()
        tokens = [
            ['a', 'b']
        ]
        assistant.explorer(tokens)
        mock_init.assert_called_with(tokens)

    @patch('tempfile.TemporaryDirectory')
    def test_create_dataset(self, tempdir_mock):
        input_path = self.get_resources('pdf')
        output_txt_path = '/output_txt'
        output_csv_path = '/output_csv'

        tempdir_mock.return_value.__enter__.return_value = output_txt_path

        assistant = Assistant()
        assistant.pdf_to_text = Mock()
        assistant.text_to_csv = Mock()

        assistant.dataset(
            input_path,
            output_csv_path
        )
        assistant.pdf_to_text.assert_called_once_with(
            input_path,
            output_txt_path
        )
        assistant.text_to_csv.assert_called_once_with(
            output_txt_path,
            output_csv_path
        )
