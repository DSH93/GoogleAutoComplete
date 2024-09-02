import os
from string import punctuation


class DataParser:
    def __init__(self, folder_path: str = None, files_paths: list = None):
        sentences = []
        if folder_path is not None:
            sentences += self.load_files_from_folder(folder_path)
        else:
            if files_paths is None:
                raise ValueError(
                    'You must provide a folder path or a list of file paths')
            for file_path in files_paths:
                sentences += self.load_file(file_path)
        self.lines = self.lowercase_and_remove_punctuation(sentences)

    def load_files_from_folder(self, folder_path) -> list:
        sentences = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.txt'):
                    sentences += self.load_file(os.path.join(root, file))
        return sentences

    def load_file(self, file_path) -> list:
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
                offset += len(line)
        return lines

    def get_sentences(self) -> list:
        return self.lines

    def lowercase_and_remove_punctuation(self, sentences: list) -> list:
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
