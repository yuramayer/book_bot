"""Methods working with text: pages & translations"""

from nltk.tokenize import sent_tokenize
import openai
from config.conf import OPENAI_TOKEN


def prettify_text(page, text):
    """Prettify page before the sending"""

    txt = '\n\n'.join(sent_tokenize(text))
    txt += f'\n\n📖 <b>page {page}</b>\n\n'
    return txt


CLIENT_GPT = openai.OpenAI(api_key=OPENAI_TOKEN)


def translate_word(word: str) -> str:
    """Translate the phrase with the ChatGPT"""
    question = CLIENT_GPT.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': f'Переведи фразу на русский: "{word}".\
                    При переводе учитывай, \
                        что она связана с "Властелином Колец"'
            }
        ],
        model='gpt-4o'
    )
    answer = question.choices[0].message.content
    return answer
