from django.test import TestCase

from unittest.mock import patch
from api.models import AiAnalysisLog
from decimal import Decimal

from .mock import MockResponse_1, MockResponse_2


# Create your tests here.
class TestApi(TestCase):

    def setUp(self):
        # テスト用にテーブルを初期化
        AiAnalysisLog.objects.all().delete()

    # 解析成功
    @patch('requests.post', return_value=MockResponse_1())
    def test_analysis_success(self, mocked):
        # POST
        response = self.client.post(
            '/api/analysis', {'image_path': 'hoge.jpg'})

        # Assert: 200
        self.assertEqual(response.status_code, 200)

        # AIAiAnalysisLogの状態を確認
        ai_analysis_log = AiAnalysisLog.objects.all().first()
        self.assertEqual(ai_analysis_log.image_path, 'hoge.jpg')
        self.assertEqual(ai_analysis_log.success, 'True')
        self.assertEqual(ai_analysis_log.message, 'success')
        self.assertEqual(ai_analysis_log.class_id, 1)
        self.assertEqual(ai_analysis_log.confidence, Decimal('0.8683'))

    # 解析失敗
    @patch('requests.post', return_value=MockResponse_2())
    def test_analysis_failure(self, mocked):
        # POST
        response = self.client.post(
            '/api/analysis', {'image_path': 'fuga.jpg'})

        # Assert: 200
        self.assertEqual(response.status_code, 200)

        # AIAiAnalysisLogの状態を確認
        ai_analysis_log = AiAnalysisLog.objects.all().first()
        self.assertEqual(ai_analysis_log.image_path, 'fuga.jpg')
        self.assertEqual(ai_analysis_log.success, 'False')
        self.assertEqual(ai_analysis_log.message, 'Error:E50012')
        self.assertEqual(ai_analysis_log.class_id, 0)
        self.assertEqual(ai_analysis_log.confidence, Decimal('0'))

    # image_pathがない場合
    def test_analysis_no_image_path(self):
        # POST
        response = self.client.post('/api/analysis')

        # Assert: 400
        self.assertEqual(response.status_code, 400)

    # GETリクエスト
    def test_analysis_get(self):
        # GET
        response = self.client.get('/api/analysis')

        # Assert: 405
        self.assertEqual(response.status_code, 405)
