from typing import Optional

import requests
import time


class ExampleAPIResponse():
    def __init__(self, success: bool, message: str, class_id: Optional[int], confidence: Optional[float]):
        if not self._validate(success, message, class_id, confidence):
            raise ValueError("Invalid value")

        self._success = success
        self._message = message
        self._class_id = class_id
        self._confidence = confidence

    @staticmethod
    def _validate(success: bool, message: str, class_id: int, confidence: float) -> bool:
        if not isinstance(success, bool):
            return False
        if not isinstance(message, str):
            return False

        # success = Falseの場合はclass_id, confidenceはNone
        if success:
            if not isinstance(class_id, int):
                return False
            if not isinstance(confidence, float):
                return False

            # confidenceは0~1の範囲
            if not (0 <= confidence <= 1):
                return False

        return True

    @property
    def success(self) -> bool:
        return self._success

    @property
    def message(self) -> str:
        return self._message

    @property
    def class_id(self) -> Optional[int]:
        return self._class_id

    @property
    def confidence(self) -> Optional[float]:
        return self._confidence


class ExampleAPIClient():
    def __init__(self):
        self.api_url = "http://example.com"

    # POSTリクエストを投げて、ExampleAPIResponseとタイムスタンプを返す
    def post_analysis_request(self, image_path: str) -> (Optional[ExampleAPIResponse], int):
        try:
            # UnixTimeを取得
            response_timestamp = int(time.time())

            # POST
            response = requests.post(
                self.api_url, data={'image_path': image_path})

            print("response: ", response.status_code)

            # レスポンスが200以外の場合はエラー
            if response.status_code != 200:
                print("api request error")
                return None, response_timestamp

            data = response.json()

            success = data.get('success')
            message = data.get('message')
            estimated_data = data.get('estimated_data')
            class_id = estimated_data.get('class')
            confidence = estimated_data.get('confidence')

            return ExampleAPIResponse(success, message, class_id, confidence), response_timestamp

        except requests.RequestException as e:
            print(f"Error occurred: {e}")
            return None, response_timestamp
        except ValueError as e:
            print(f"Validation error: {e}")
            return None, response_timestamp
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None, response_timestamp
