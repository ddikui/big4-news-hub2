import os
import sys

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Vercel 은 이 모듈의 `app` 변수를 WSGI 앱으로 사용한다.
# API 경로 복원(__route)은 app.py 의 ApiRouteMiddleware 가 담당한다.
from app import app  # noqa: E402,F401

app.debug = False
