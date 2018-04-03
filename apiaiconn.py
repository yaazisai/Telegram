import os.path
import sys
import json

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

def getAction(session_id,CLIENT_ACCESS_TOKEN,itext):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'en'  # optional, default value equal 'en'
    request.session_id = session_id
    request.query = itext
    response = request.getresponse()
    res = json.loads(response.read())
    return res
