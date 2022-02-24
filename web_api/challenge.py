import os;from web_api.requests_api import RequestVerification;import var_env;P=os.getenv("IP_WEBSERVICE");T=os.getenv("API_TOKEN")
class Challenge:
    def __init__(S,f,p,t,i,t=1000):S.id=i;S.timeout=t;S.function_name=f;S.parameters=p;S.tests=t
    def valid_challenge(S,v):
        p={"token":"API_TEST","template":S.get_template(),"isValid":v};r=RequestVerification.post_request(f"http://{P}/api/challenge/{S.id}/check",p=p)
        if r==0:return
        c=f"send challenge status to API  ({S.id})"
        if RequestVerification.verify(r,c):return
    def get_template(S):return f"def {S.function_name}({S.get_format_args(S.parameters)}):\n    "
    @staticmethod
    def get_format_args(a):
        if len(a)==1:return str(a[0])
        return", ".join(a)
class ChallengeParser:
    def __init__(S,i="localhost:8000"):S.e=f"http://{i}/api/challenges";S.d=None;S.s=0;S.E=None
    is_valid_status=lambda S:S.s==0
    def send_request(S):
        r=RequestVerification.get_request(S.e,p={"token":"API_TEST"})
        if r==0:return
        if RequestVerification.verify(r,f"get all challenges not validated"):S.d=r.json()
    def get_challenges(S):
        S.send_request()
        if S.d:
            c=[]
            for C in S.d:
                i=C.get("id");f=C.get("function_name");t=S.get_tests(C.get("tests"));p=S.get_parameters(C.get("tests"));c.append(Challenge(f, p, t, i))
            return c
        return []
    @staticmethod
    def get_tests(t):
        f=[]
        for T in t:
            F=[[]]
            for i in T.get("inputs"):F[0].append(i.get("value"))
            F.append(T.get("output"));f.append(F)
        return f
    @staticmethod
    def get_parameters(t):
        p=[]
        for P in t[0].get("inputs"):p.append(P.get("name"))
        return p
