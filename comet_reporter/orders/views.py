
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
def orderView(request):
    try:
        header_key = request.headers["x-api-key"]
        if request.method == "GET":
            version = request.GET.get("version")
            username = request.GET.get("username")
            comet = Comet(version)
            comet.cloud_connect()
            reporter_key = comet.retrieve("reporter_key").iloc[0]["key"]
            if header_key == reporter_key:
                buys = comet.retrieve_completed_buys(username).round(decimals=2)
                sells = comet.retrieve_completed_sells(username).round(decimals=2)
                pending_buys = comet.retrieve_pending_buys(username).round(decimals=2)
                pending_sells = comet.retrieve_pending_sells(username).round(decimals=2)
                pending_buys["status"] = "pending"
                pending_sells["status"] = "pending"
                if pending_buys.index.size >0:
                    pending_buys["order_id"] = pending_buys["id"]
                if pending_sells.index.size > 0:
                    pending_sells["order_id"] = pending_sells["id"]
                buys["status"] = "complete"
                sells["status"] = "complete"
                final = pd.concat([buys,sells,pending_buys,pending_sells])
                print(final)
                if final.index.size > 0:
                    final = final.groupby(["product_id","order_id","status","side"]).agg({"created_at":"first","price": "mean", "size": "sum"}).reset_index()
                    final["created_at"] = pd.to_datetime(final["created_at"])
                    final.sort_values("created_at",inplace=True)
                    final["created_at"] = [str(x).split(".")[0] for x in final["created_at"]]
                    final["order_id"] = [str(x).split("-")[0] for x in final["order_id"]]
                    complete = final[[x for x in final.columns if x != "order_id"]].round(decimals=4).iloc[::-1].head(10).to_dict("records")
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