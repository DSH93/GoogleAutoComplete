class AutoCompleteData:
  completed_sentence : str
  source_text : str
  offset : int
  score : int
  
  def __str__(self):
    return f'Sentence: {self.completed_sentence} (source: {self.source_text}, offset: {self.offset}) score: [{self.score}]'