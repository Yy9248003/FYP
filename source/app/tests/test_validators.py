"""输入验证器测试。"""
from django.test import SimpleTestCase

from app.validators import InputValidator


class InputValidatorTestCase(SimpleTestCase):
    """测试 InputValidator 的边界行为。"""

    def test_validate_phone_allows_blank_after_strip(self):
        """手机号为纯空白时按可选字段处理。"""
        is_valid, error = InputValidator.validate_phone('   ')
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_email_allows_blank_after_strip(self):
        """邮箱为纯空白时按可选字段处理。"""
        is_valid, error = InputValidator.validate_email('\t  ')
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_password_rejects_whitespace_only_password(self):
        """密码不能全部由空白字符组成。"""
        is_valid, error = InputValidator.validate_password('      ')
        self.assertFalse(is_valid)
        self.assertEqual(error, '密码不能全为空白字符')

    def test_validate_password_accepts_normal_password(self):
        """合法密码应通过校验。"""
        is_valid, error = InputValidator.validate_password('abc123!')
        self.assertTrue(is_valid)
        self.assertIsNone(error)
