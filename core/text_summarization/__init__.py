from .main import Text_Summarization

def text_summarization(messages, language="spanish"):
    text_summ = Text_Summarization(messages, language)
    return text_summ.run()
