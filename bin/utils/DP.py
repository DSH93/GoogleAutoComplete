import os
from string import punctuation


class DataParser:
    """
    Parses data from folder with files or from a list of files.
    """

    def __init__(self, folder_path: str = None, files_paths: list[str] = None):
        sentences = []
        if folder_path is not None:
            sentences += self.load_files_from_folder(folder_path)
        else:
            if files_paths is None:
                raise ValueError(
                    'You must provide a folder path or a list of file paths')
            for file_path in files_paths:
                sentences += self.__load_file(file_path)
        self.lines = self.__lowercase_and_remove_punctuation(sentences)

    def load_files_from_folder(self, folder_path: str) -> list[str]:
        # Load all files from folder to list of sentences
        sentences = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.txt'):
                    sentences += self.__load_file(os.path.join(root, file))
        return sentences

    def get_lines(self) -> list[str]:
        # Get parsed data
        return self.lines

    def __load_file(self, file_path: str) -> list[str]:
        # Load file to list of sentences
        lines = []
        offset = 0
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    lines.append((
                        line,
                        os.path.basename(file_path),
                        offset
                    ))
                offset += 1
        return lines

    def __lowercase_and_remove_punctuation(self, sentences: list[str]) -> list[str]:
        # Helper function to lowercase and remove punctuation from sentences
        cleaned_sentences = []
        translator = str.maketrans('', '', punctuation)
        for sentence, filename, offset in sentences:
            lowercase_sentence = sentence.lower()
            cleaned_sentence = lowercase_sentence.translate(translator)
            cleaned_sentence = ' '.join(cleaned_sentence.split())
            cleaned_sentences.append((
                cleaned_sentence,
                filename,
                offset
            ))

        return cleaned_sentences
