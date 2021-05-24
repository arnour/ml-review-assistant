from . import TestBase
from ml_review_assistant.extraction import Extractor


class ExtractionTestCase(TestBase):

    def test_extract_full_text_from_file(self):
        file_path = self.get_resource('3382494.3422167-cropped.pdf')
        expected = """程序错误\n–\n–\nABSTRACT \nBackground.  Testing  is  an  essential  activity  in  the  software \ndevelopment life cycle. Nowadays, testing activities are widely  • CCS → Software and its engineering → Software creation and \nmanagement → Software verification and validation\n程序错误\nIn ESEM’ 20: ACM/IEEE International Sy\nSoftware Engineering and Measurement (ESEM) (ESEM’ 20), October 8–\nor \n–"""
        extractor = Extractor()
        result = extractor.text(file_path)
        self.assertEqual(result, expected, 'Extracted text is not as expected')

    def test_extract__list_of_words_from_file(self):
        file_path = self.get_resource('3382494.3422167-cropped.pdf')
        expected = ['程序错误', '–', '–', 'ABSTRACT', 'Background.', 'Testing', 'is', 'an', 'essential', 'activity', 'in', 'the', 'software', 'development', 'life', 'cycle.', 'Nowadays,', 'testing', 'activities', 'are', 'widely', '•', 'CCS', '→', 'Software', 'and', 'its', 'engineering', '→', 'Software', 'creation', 'and', 'management', '→', 'Software', 'verification', 'and', 'validation', '程序错误In', 'ESEM’', '20:', 'ACM/IEEE', 'International', 'Sy', 'Software', 'Engineering', 'and', 'Measurement', '(ESEM)', '(ESEM’', '20),', 'October', '8–', 'or', '–']
        extractor = Extractor()
        result = extractor.words(file_path)
        self.assertEqual(result, expected)
