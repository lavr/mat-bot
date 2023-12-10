import logging
import os

from openai import OpenAI, RateLimitError

logger = logging.getLogger(__name__)

PROMPT_SYSTEM = """
Ты переводчик с матерного языка на литературный русский.
Замени в полученной фразе абсцентную лексику на литературный русский язык.
Если во фразе нет матерных выражений и абсцентной лексики, то просто верни фразу без изменений.
"""


def process_text(text):

    client = OpenAI(api_key=os.environ.get('CHATGPT_TOKEN'))

    try:
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": PROMPT_SYSTEM},
                {"role": "user", "content": text},
            ],
            stream=True   # TODO: сделать посимвольную выдачу в телегу
        )
    except RateLimitError as exc:
        logger.error("process_test error: %s", exc)
        return False, "Слишком много запросов, попробуйте позже"  # Или кончились деньги

    chunks = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            chunks.append(chunk.choices[0].delta.content)

    return True, "".join(chunks)


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    for line in process_text('Мать твою поперек жопы ети, грушу тебе в пизду, гвоздь в подпиздок'):
        print(line, end='')
