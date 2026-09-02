class Interface:
#     def __init__(self, functions: List[Function]):
#         self._prompt_builder: PromptBuilder = PromptBuilder(functions)
#         self._model: Small_LLM_Model = Small_LLM_Model()
#         self._tokenizer: Tokenizer = Tokenizer(
#             self._model.get_path_to_vocab_file,
#             self._model.get_path_to_merges_file,
#             self._model.get_path_to_tokenizer_file)
#         self._guardian: Guardian = Guardian(
#             self._tokenizer.get_vocab(),
#             self._tokenizer.get_reversed_vocab(),
#             functions)