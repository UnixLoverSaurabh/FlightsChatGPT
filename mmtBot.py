import os
import openai
from common.utils import constants
import json
from aiohttp import ClientSession

openai.aiosession.set(ClientSession())

openai.api_key = os.getenv("CHATGPT_API_KEY")


def searchCriteriaCollection(question, chat_log=constants.SESSION2_CHAT_LOG_VALUE, session_status=False) -> dict:

    ans = {"source": "", "destination": "", "departure_date": ""}

    if session_status:
        return ans

    prompt_text = f'{chat_log}{constants.restart_sequence}: {question}{constants.start_sequence}:'
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_text,
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.2,
        presence_penalty=0
    )
    command = response['choices'][0]['text']

    try:
        ans = json.loads(command.replace("'", '"'))
    except Exception as ex:
        print(f'Error decoding response: {command}, Ex: {ex}')
    return ans


def ask(question, chat_log=constants.SESSION1_CHAT_LOG_VALUE):
    prompt_text = f'{chat_log}{constants.restart_sequence}: {question}{constants.start_sequence}:'
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt_text,
      temperature=0.8,
      max_tokens=150,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0.3,
      stop=["\n"],
    )
    story = response['choices'][0]['text']
    print(f'question: {question}\t answer: {str(story)}')
    return str(story)


def append_interaction_to_chat_log(question, answer, chat_log=""):
    return f'{chat_log}{constants.restart_sequence} {question}{constants.start_sequence}{answer}'


def closeOpenAISession():
    openai.aiosession.get().close()