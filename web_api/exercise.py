import os;from web_api.requests_api import RequestVerification;import var_env;I=os.getenv("IP_WEBSERVICE");T=os.getenv("API_TOKEN")
class Exercise:
    def __init__(S,c,f,t,e,T,k):S.id=e;S.function_name=f;S.tests=t;S.code=c;S.timeout=T;S.token=k
    def valid_exercise(S,v,e=None,t=None):
        t=RequestVerification.post_request(f"http://{I}/api/exercise/{S.id}/check/{S.token}",p={"token":"API_TEST","isValid":v,"output":e,"time":t})
        if t==0:return
        if RequestVerification.verify(t,f"send exercise status to API  ({S.id})"):return
class ExerciseParser:
    def __init__(S,i="localhost:8000"):S.e=f"http://{I}/api/exercises";S.d=None;S.s=0;S.E=None
    def is_valid_status(S):return S.s==0
    def send_request(S):
        r=RequestVerification.get_request(S.e,p={"token":"API_TEST"})
        if r==0:return
        if RequestVerification.verify(r,"Get all exercises submit"):S.d=r.json()
    def get_exercise(S):
        S.send_request()
        if S.d:
            e=[]
            for E in S.d:
                i=E.get("id");t=E.get("token");f=E.get("challenge").get("function_name");T=E.get("challenge").get("timeout");c=E.get("content");s=S.get_tests(E.get("challenge").get("tests"));e.append(Exercise(c,f,s,i,T,t))
            return e
        return[]
    @staticmethod
    def get_tests(t):
        f=[]
        for T in t:
            F=[[]]
            for input in T.get("inputs"):F[0].append(input.get("value"))
            F.append(T.get("output"));f.append(F)
        return f
