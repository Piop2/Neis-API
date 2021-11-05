import requests
from .exceptions import *

URL = "https://open.neis.go.kr/hub/schoolInfo"


def get_school_data(key, atpt_ofcdc_sc_code=None, sd_schul_code=None, schul_nm=None, schul_knd_sc_nm=None,
                    lctn_sc_nm=None,fond_sc_nm=None, pindex: int = 1, psize: int = 100):
    """
    신청주소: https://open.neis.go.kr/hub/schoolInfo
    신청제한횟수: 제한없음
    :param key: 인증키
    :param atpt_ofcdc_sc_code: 시도교육청코드
    :param sd_schul_code: 표준학교코드
    :param schul_nm: 학교명
    :param schul_knd_sc_nm: 학교종류명
    :param lctn_sc_nm: 소재지명
    :param fond_sc_nm: 설립명
    :param pindex: 페이지 위치
    :param psize: 페이지 당 신청 숫자
    :return: 검색된 모든 학교
    """

    params = {
        "KEY": key,
        "Type": "json",
        "pIndex": pindex,
        "pSize": psize,
        "ATPT_OFCDDC_SC_CODE": atpt_ofcdc_sc_code,
        "SD_SCHUL_CODE": sd_schul_code,
        "SCHUL_NM": schul_nm,
        "SCHUL_KND_SC_NM": schul_knd_sc_nm,
        "LCTN_SC_NM": lctn_sc_nm,
        "FOND_SC_NM": fond_sc_nm,
    }

    res = requests.get(url=URL, params=params, verify=False, json=True)
    res.encoding = "UTF-8"
    request_json = res.json()

    try:
        status_code = request_json["schoolInfo"][0]["head"][1]["RESULT"]["CODE"]
    except KeyError:
        status_code = request_json["RESULT"]["CODE"]

    if status_code == "ERROR-300":
        raise Error300()
    elif status_code == "ERROR-290":
        raise Error290()
    elif status_code == "ERROR-333":
        raise Error333()
    elif status_code == "ERROR-336":
        raise Error336()
    elif status_code == "ERROR-337":
        raise Error337()
    elif status_code == "ERROR-500":
        raise Error500()
    elif status_code == "ERROR-600":
        raise Error600()
    elif status_code == "ERROR-601":
        raise Error601()
    elif status_code == "INFO-300":
        raise Info300()
    elif status_code == "INFO-200":
        raise Info200()

    return tuple(SchoolInfo(data) for data in request_json["schoolInfo"][1]["row"])

class SchoolInfo:
    def __init__(self, school_data):
        self.data = school_data