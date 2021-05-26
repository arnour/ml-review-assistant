from ml_review_assistant.exploration import Explorer
from ml_review_assistant.preparation import Preparator
from ml_review_assistant.extraction import Extractor
from pathlib import Path
import csv


class Assistant:
    """Class with assistant utilities"""

    def __init__(self, extractor=None, preparator=None):
        self.__extractor = extractor if extractor else Extractor()
        self.__preparator = preparator if preparator else Preparator()

    def pdf_to_text(self, input_path, output_dir_path):
        """
        Read PDF files and extract text from them.

        Args:
            input_path (str): Path to pdf file or directory containing files
            output_dir_path (str): Path to output directory
        """
        output = self.__validate_output(output_dir_path)
        files = self.__read_input_files(input_path, "*.pdf")
        for file in files:
            output_file = output.joinpath(file.name.replace(".pdf", ".txt"))
            with open(output_file, "w", encoding="utf-8") as textfile:
                textfile.write(self.__extractor.text(file))

    def text_to_csv(self, input_path, output_dir_path):
        """
        Read text file and create a csv dataset with cleaned texts.

        Args:
            input_path (str): Path to text file or directory containing files
            output_dir_path (str): Path to output directory
        """
        output = self.__validate_output(output_dir_path)
        files = self.__read_input_files(input_path, "*.txt")
        with open(output.joinpath("dataset.csv"), "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["paper", "content"])
            for file in files:
                with open(file, "r", encoding="utf-8") as textfile:
                    text = " ".join(textfile.readlines())
                    cleaned = self.__preparator.prepare(text, stem=True)
                    writer.writerow([file.name.replace(".txt", ""), cleaned])

    def explorer(self, tokens):
        """
        Create a explorer instance for provided tokens dataset

        Args:
            tokens (list): Dataset with array of words for each document

        Returns:
            Explorer: explorer with loaded corpus for analysis
        """
        return Explorer(tokens)

    def __read_input_files(self, input_path, pattern="*.pdf"):
        input = Path(input_path)
        if not input.exists():
            raise Exception("Provided input path does not exist")
        files = []
        if input.is_file() and pattern.endswith(input.suffix):
            files.append(input)
        elif input.is_dir():
            files.extend(list(input.glob(pattern)))
        return files

    def __validate_output(self, output_dir_path):
        output = Path(output_dir_path)
        if output.exists() and not output.is_dir():
            raise Exception("Provided input path should be a directory")
        output.mkdir(parents=True, exist_ok=True)
        return output
