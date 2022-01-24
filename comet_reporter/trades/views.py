
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
def tradeView(request):
    try:
        header_key = request.headers["x-api-key"]
        if request.method == "GET":
            version = request.GET.get("version")
            username = request.GET.get("username")
            comet = Comet(version)
            comet.cloud_connect()
            reporter_key = comet.retrieve("reporter_key").iloc[0]["key"]
            if header_key == reporter_key:
                    trades = comet.retrieve_completed_trades(username).round(decimals=2)
                    pending_trades = comet.retrieve_pending_trades(username).round(decimals=2)
                    pending_trades["status"] = "pending"
                    trades["status"] = "complete"
                    final = pd.concat([trades,pending_trades])
                    if final.index.size > 0:
                        final["date"] = pd.to_datetime(final["date"])
                        final.sort_values("date",inplace=True)
                        final["date"] = [str(x).split(".")[0] for x in final["date"]]
                        complete = final[["date","product_id","status","sell_price","size","price"]].round(decimals=4).iloc[::-1].head(10).to_dict("records")
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