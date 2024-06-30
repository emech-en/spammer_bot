import unittest
from unittest.mock import AsyncMock, patch
from spammer_bot import check_spam, user_messages, user_last_warning, PERSONAL_MAX_PER_MINUTE, FORWARD_MAX_PER_HOUR, \
    FORWARD_MAX_PER_FIVE_HOURS, WARNING_COOLDOWN


class TestSpamFilterBot(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        user_messages.clear()
        user_last_warning.clear()
        self.update = AsyncMock()
        self.context = AsyncMock()
        self.update.message.from_user.id = 12345
        self.update.message.from_user.username = "test_user"
        self.update.effective_chat.id = 67890

    @patch('time.time', return_value=1000000)
    async def test_personal_spam_detection(self, mock_time):
        self.update.message.forward_date = None
        for _ in range(PERSONAL_MAX_PER_MINUTE):
            is_spam = await check_spam(self.update, self.context)
            self.assertFalse(is_spam)

        is_spam = await check_spam(self.update, self.context)
        self.assertTrue(is_spam)
        self.update.message.delete.assert_called_once()
        self.context.bot.send_message.assert_called_once()

    @patch('time.time', return_value=1000000)
    async def test_forward_spam_detection(self, mock_time):
        self.update.message.forward_date = 999999
        for _ in range(FORWARD_MAX_PER_HOUR):
            is_spam = await check_spam(self.update, self.context)
            self.assertFalse(is_spam)

        is_spam = await check_spam(self.update, self.context)
        self.assertTrue(is_spam)
        self.update.message.delete.assert_called_once()
        self.context.bot.send_message.assert_called_once()

    @patch('time.time', return_value=1000000)
    async def test_warn_once_per_hour(self, mock_time):
        self.update.message.forward_date = None
        for _ in range(PERSONAL_MAX_PER_MINUTE + 2):
            await check_spam(self.update, self.context)

        self.context.bot.send_message.assert_called_once()
        self.assertEqual(self.update.message.delete.call_count, 2)

    @patch('time.time', return_value=1000000)
    async def test_warn_again_after_hour(self, mock_time):
        self.update.message.forward_date = None
        for _ in range(PERSONAL_MAX_PER_MINUTE + 1):
            await check_spam(self.update, self.context)
        self.context.bot.send_message.assert_called_once()
        self.context.bot.send_message.reset_mock()

        with patch('time.time', return_value=1000000 + WARNING_COOLDOWN + 1):
            for _ in range(PERSONAL_MAX_PER_MINUTE + 1):
                await check_spam(self.update, self.context)
            self.context.bot.send_message.assert_called_once()

    @patch('time.time', return_value=1000000)
    async def test_no_warn_for_normal_messages(self, mock_time):
        self.update.message.forward_date = None
        for _ in range(PERSONAL_MAX_PER_MINUTE):
            is_spam = await check_spam(self.update, self.context)
            self.assertFalse(is_spam)

        self.context.bot.send_message.assert_not_called()
        self.update.message.delete.assert_not_called()

    @patch('time.time')
    async def test_forward_spam_five_hours(self, mock_time):
        mock_time.return_value = 1000000
        self.update.message.forward_date = 999999
        hour_increment = 3600

        for i in range(FORWARD_MAX_PER_FIVE_HOURS):
            mock_time.return_value = 1000000 + i * hour_increment
            is_spam = await check_spam(self.update, self.context)
            self.assertFalse(is_spam, f"Message {i + 1} was incorrectly marked as spam")

        mock_time.return_value = 1000000 + FORWARD_MAX_PER_FIVE_HOURS * hour_increment
        is_spam = await check_spam(self.update, self.context)
        self.assertTrue(is_spam, "Spam was not detected after exceeding five-hour limit")
        self.update.message.delete.assert_called_once()
        self.context.bot.send_message.assert_called_once()

    @patch('time.time')
    async def test_forward_spam_hourly(self, mock_time):
        mock_time.return_value = 1000000
        self.update.message.forward_date = 999999

        for i in range(FORWARD_MAX_PER_HOUR):
            is_spam = await check_spam(self.update, self.context)
            self.assertFalse(is_spam, f"Message {i + 1} was incorrectly marked as spam")

        is_spam = await check_spam(self.update, self.context)
        self.assertTrue(is_spam, "Spam was not detected after exceeding hourly limit")
        self.update.message.delete.assert_called_once()
        self.context.bot.send_message.assert_called_once()


if __name__ == '__main__':
    unittest.main()
