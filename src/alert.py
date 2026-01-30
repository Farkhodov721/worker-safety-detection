"""
Telegram alert system for safety violations
Sends notifications with screenshots to Telegram
"""

import telegram
from datetime import datetime
from pathlib import Path

async def send_violation_alert(bot_token, chat_id, image_path, violations):
    """
    Send violation alert to Telegram
    
    Args:
        bot_token: Telegram bot token
        chat_id: Telegram chat ID
        image_path: Path to violation screenshot
        violations: List of detected violations
    """
    if not violations:
        print("⚠️ No violations to report")
        return
    
    try:
        bot = telegram.Bot(token=bot_token)
        
        # Create alert message
        violation_types = [v['class'] for v in violations]
        violation_summary = ', '.join(set(violation_types))
        
        message = f"""
⚠️ *SAFETY VIOLATION DETECTED* ⚠️

🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📍 Type: {violation_summary}
🔢 Count: {len(violations)} violation(s)

⚡ Immediate action required!
        """
        
        # Send photo with caption
        if image_path and Path(image_path).exists():
            with open(image_path, 'rb') as photo:
                await bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=message,
                    parse_mode='Markdown'
                )
            print(f"✅ Alert sent to Telegram")
        else:
            print(f"❌ Screenshot not found: {image_path}")
            
    except telegram.error.TelegramError as e:
        print(f"❌ Telegram error: {e}")
    except FileNotFoundError:
        print(f"❌ Screenshot file not found: {image_path}")
    except Exception as e:
        print(f"❌ Unexpected error sending alert: {e}")

async def test_telegram_connection(bot_token, chat_id):
    """Test Telegram bot connection"""
    try:
        bot = telegram.Bot(token=bot_token)
        await bot.send_message(
            chat_id=chat_id,
            text="🤖 Worker Safety Detection System is now active!"
        )
        print("✅ Telegram connection successful!")
        return True
    except telegram.error.TelegramError as e:
        print(f"❌ Telegram connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
