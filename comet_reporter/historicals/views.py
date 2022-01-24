
from django.http.response import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import requests
import pandas as pd
from database.comet import Comet
import os
from dotenv import load_dotenv
load_dotenv()
# Create your views here.
@csrf_exempt
def historicalView(request):
    try:
        header_key = request.headers["x-api-key"]
        if request.method == "GET":
            version = request.GET.get("version")
            username = request.GET.get("username")
            comet = Comet(version)
            comet.cloud_connect()
            reporter_key = comet.retrieve("reporter_key").iloc[0]["key"]
            if header_key == reporter_key:
                final = comet.retrieve_historicals(username).round(decimals=2)[["time","crypto","signal","velocity","inflection","p_sign_change","price","bid","ask"]]
                comet.disconnect()
                if final.index.size > 0:
                    final["time"] = pd.to_datetime(final["time"])
                    final.sort_values("time",inplace=True)
                    final["time"] = [str(x).split(".")[0] for x in final["time"]]
                    final["p_sign_change"] = [str(x) for x in final["p_sign_change"]]
                    complete = final.iloc[::-1].head(10).to_dict("records")
                else:
                    complete = []
            else:
                complete = {"error":"incorrect_key"}
        elif request.method == "DELETE":
            complete = {}
        elif request.method == "UPDATE":
            complete = {}
        elif request.method == "POST":
            complete = {}
        else:
            complete = {}
    except Exception as e:
        complete = {}
        print(str(e))
    return JsonResponse(complete,safe=False)