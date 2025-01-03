from nltk.tokenize import sent_tokenize


def prettify_text(page, text):
    txt = '\n\n'.join(sent_tokenize(text))
    txt += f'\n\n📖 <b>page {page}</b>\n\n'
    return txt

