import sys;import requests
class RequestVerification:
    @staticmethod
    def verify(r,c):
        if r.ok:return 1
        elif 400<=r.status_code<500:
            try:print(f"Error during {r.status_code}: {c} : {r.json()} ",file=sys.stderr)
            except:print(f"Error during {r.status_code}: {c}",file=sys.stderr)
        else:
            try:print(f"Error during {r.status_code}: {c} {r.json()}",file=sys.stderr)
            except:print(f"Error during {r.status_code}: {c}",file=sys.stderr)
    @staticmethod
    def post_request(u,p={}):
        try:
            r=requests.post(url=u,params=p);return r
        except:
            print("Error during connection with web api, please verify his status",file=sys.stderr);return 0
    @staticmethod
    def get_request(u,p={}):r=requests.get(url=u,params=p);return r;print("Error during connection with web api, please verify his status",file=sys.stderr);return 0
