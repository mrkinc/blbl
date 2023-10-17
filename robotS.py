import sys

import requests

session = requests.Session()
cookie = "buvid3=28EC906E-BCF7-DA0A-2217-427C64F1D68124073infoc; i-wanna-go-back=-1; _uuid=C7E1054110-510D1-A35A-10DC8-FC1061B2A93D423172infoc; FEED_LIVE_VERSION=V8; nostalgia_conf=-1; CURRENT_FNVAL=4048; rpdid=|(u|Jll)~RR~0J'uY)Y|YJkYR; b_nut=1686063263; buvid_fp_plain=undefined; header_theme_version=CLOSE; DedeUserID=213248764; DedeUserID__ckMd5=5afb3c021bafa4cf; b_ut=5; LIVE_BUVID=AUTO8016943597833299; hit-dyn-v2=1; SESSDATA=e53b53ae%2C1711871995%2C5eca2%2Aa2CjBfgWtljVNYOw4D38A6gpC6WAoU38rYSI5CM2CeDROxjmSEQmJGY90DTZ2z7c9qSVMSVnFraGVhQ0ptTkpWM0pSUFFLTVpUMGI3TGNLYlhzN1BNcnZaZ3lVaGFjbEtzTHlJT1U1bDhCTHZtVE5UTHhTdTNJc0dUc09QaEg1UncwLVhMa2tMdGxBIIEC; bili_jct=08b6496b0ff3af1bcc3a769b3b7643b3; buvid4=16489DBE-67DB-38C1-570B-EF6C50828EE925517-023060622-EHDpG6f5%2FKRXYLw0zqkkkw%3D%3D; CURRENT_QUALITY=80; enable_web_push=DISABLE; fingerprint=f7af7a462f7ff4b0f28fe1692b067bc4; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTc2MDk5NjgsImlhdCI6MTY5NzM1MDcwOCwicGx0IjotMX0.okxLNnxO5SPh5qDiIFjVgjGsWavXyoY4sLkmP-wc9x4; bili_ticket_expires=1697609908; PVID=1; bp_video_offset_213248764=853010415172452354; innersign=0; home_feed_column=4; bsource=search_google; buvid_fp=38d0f5720413c72b6ce6e4fe674dfb23; sid=7985huql; browser_resolution=864-770; b_lsid=FD35B10EC_18B3B95455A"

def _requests(method, url, decode_level=2,  retry=10, timeout=15, **kwargs):
    if method in ["get", "post"]:
        for _ in range(retry + 1):
            response = getattr(session, method)(url, timeout=timeout, **kwargs)
            return response.json() if decode_level == 2 else response.content if decode_level == 1 else response
    return None

def TestCookie():
    url = f"https://api.bilibili.com/x/space/myinfo"
    headers = {'Host': "api.bilibili.com",
               'cookie': cookie}
    response = _requests("get", url, headers=headers)
    if response and response.get("code") != -101:
        print("Cookie仍有效")
        return True
    else:
        print("Cookie已失效")
        return False


if __name__ == '__main__':
    pass