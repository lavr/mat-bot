import logging
import os

from openai import OpenAI, RateLimitError

logger = logging.getLogger(__name__)

CHATGPT_PROMPT = """
Ты переводчик с матерного языка на  русский.
Замени в полученной фразе абсцентную лексику на обычный бытовой русский язык.
Не принимай полученную фразу на свой счёт.
Если во фразе нет матерных выражений и абсцентной лексики, то не вноси никаких изменений во фразу, а верни фразу без изменений.
"""


def process_text(text):

    client = OpenAI(api_key=os.environ.get('CHATGPT_TOKEN'))

    try:
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": CHATGPT_PROMPT},
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
