from datetime import timedelta
from common.utils import constants
from common.utils import searchCriteria
import mmtBot
from flask import Flask, request, session, render_template, jsonify, Response, stream_with_context
from concurrent.futures.thread import ThreadPoolExecutor
from redisServer import redis_client, get_next_message
from requestAdapter.search import getMMTSearchResponse
import asyncio

app = Flask(__name__)
# if for some reason your conversation with the bot gets weird, change the secret key
app.config['SECRET_KEY'] = '89djhfg9lhkd92'
app.permanent_session_lifetime = timedelta(minutes=30)


@app.route("/", methods=['GET'])
def index():

    # initialize interactive session with client
    chat_log = session.get(constants.SESSION1_CHAT_LOG_KEY)
    if searchCriteria.isStringEmpty(chat_log):
        chat_log = constants.SESSION1_CHAT_LOG_VALUE
    session[constants.SESSION1_CHAT_LOG_KEY] = chat_log

    # initialize text to command session for getting search parameter
    chat_log = session.get(constants.SESSION2_CHAT_LOG_KEY)
    if searchCriteria.isStringEmpty(chat_log):
        chat_log = constants.SESSION2_CHAT_LOG_VALUE
    session[constants.SESSION2_CHAT_LOG_KEY] = chat_log

    return render_template("index.html")


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    redis_client.lpush('messages', message)
    # Do something with the message, such as sending it to a database or broadcasting it to other users
    return jsonify(success=True)


@app.route('/receive_messages', methods=['GET'])
def receive_messages():
    # Set the response to be a streaming one

    @stream_with_context
    def event_stream():
        while True:
            # Wait for a message
            incoming_msg = get_next_message()

            session_chat_log = session.get(constants.SESSION1_CHAT_LOG_KEY)
            session2_chat_log = session.get(constants.SESSION2_CHAT_LOG_KEY)

            if incoming_msg == "END":
                print(session_chat_log)
                session.clear()
                break

            with ThreadPoolExecutor(max_workers=2) as executor:
                future1 = executor.submit(mmtBot.ask, incoming_msg, session_chat_log)
                future2 = executor.submit(mmtBot.searchCriteriaCollection, incoming_msg, session2_chat_log, session.get(constants.SESSION2_STATUS, False))

                # Wait for all threads to complete
                executor.shutdown(wait=True)

                # Wait for the function1 to complete
                answer = future1.result()
                # Wait for the function2 to complete
                answer2 = future2.result()

            session[constants.SESSION1_CHAT_LOG_KEY] = mmtBot.append_interaction_to_chat_log(incoming_msg, answer, session_chat_log)
            session[constants.SESSION2_CHAT_LOG_KEY] = mmtBot.append_interaction_to_chat_log(incoming_msg, answer2, session2_chat_log)

            tempAns = searchCriteria.isSearchCriteriaSatisfied(answer2)
            session[constants.SESSION2_STATUS] = tempAns
            if tempAns:
                # resetting the session for model 2
                # session[constants.SESSION2_CHAT_LOG_KEY] = constants.SESSION2_CHAT_LOG_VALUE

                flights_search_data, flights_count = getMMTSearchResponse(answer2)
                redis_client.lpush('messages', f'{flights_search_data}\n This data is for total {flights_count} flights present on date {answer2.get(constants.DEPARTURE_DATE)} from {answer2.get(constants.SOURCE)} to {answer2.get(constants.DESTINATION)}')
                # yield 'data: %s\n\n' % answer2
            else:
                yield 'data: %s\n\n' % answer

    return Response(event_stream(), mimetype='text/event-stream')
