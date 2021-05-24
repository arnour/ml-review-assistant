import pdfplumber


class Extractor:
    """Extract text from pdf file"""

    def text(self, file_path):
        """Extract all pages text from file"""
        with pdfplumber.open(file_path) as pdf:
            words = []
            for page in pdf.pages:
                words.append(page.extract_text(x_tolerance=3, y_tolerance=3))
            return ''.join(words)

    def words(self, file_path):
        """Extract all words from file"""
        all_words = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                words = page.extract_words(
                        x_tolerance=3, y_tolerance=3, keep_blank_chars=False,
                        use_text_flow=False, horizontal_ltr=True,
                        vertical_ttb=True, extra_attrs=[]
                    )
                for word in words:
                    all_words.append(word['text'])
            return all_words
