from typing import Optional
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import AiAnalysisLog
from .services import ExampleAPIResponse, ExampleAPIClient

import time


@csrf_exempt  # デバッグ不便なので今回は雑に無効化
def analysis(request):
    try:  # 大概ミドルウェアで処理しそう
        if request.method == 'POST':
            image_path = request.POST.get('image_path')

            if image_path is None:
                # 400 Bad Request
                return HttpResponse(status=400)

            # UnixTimeを取得
            request_timestamp = int(time.time())

            # APIリクエスト
            api_client = ExampleAPIClient()

            # POSTリクエストを投げて、ExampleAPIResponseとタイムスタンプを取得
            response, response_timestamp = api_client.post_analysis_request(
                image_path)

            # DB登録
            if response is not None and isinstance(response, ExampleAPIResponse):
                # AIAiAnalysisLog登録
                AiAnalysisLog.objects.create(
                    image_path=image_path,
                    success=response.success,
                    message=response.message,
                    # class_idがnon-nullableなので、Noneの場合は0を登録
                    class_id=response.class_id if response.class_id is not None else 0,
                    # confidenceがnon-nullableなので、Noneの場合は0を登録
                    confidence=response.confidence if response.confidence is not None else 0,
                    request_timestamp=request_timestamp,
                    response_timestamp=response_timestamp
                )
            else:
                # 500 Internal Server Error
                return HttpResponse(status=500)

            return HttpResponse(status=200)
        else:
            # 405 Method Not Allowed
            return HttpResponse(status=405)
    except Exception as e:
        # logging
        print(e)
        # 500 Internal Server Error
        return HttpResponse(status=500)
