import json
import os
import boto3 # AWS ile iletişim kurmak için Python kütüphanesi
from langchain_community.chat_message_histories.dynamodb import DynamoDBChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# agent.py dosyamızdaki ana executor'ı import ediyoruz
from agent import agent_executor

# Ortam değişkenlerinden tablo adını ve API anahtarını alıyoruz
# Bunları Lambda ayarlarında tanımlayacağız
TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "FloraAgentChatHistory")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# --- DynamoDB ile Sohbet Geçmişi Yönetimi ---
# LangChain'in yerleşik DynamoDB entegrasyonu var, onu kullanacağız.
def get_session_history(session_id: str):
    """DynamoDB'den sohbet geçmişini alır veya oluşturur."""
    return DynamoDBChatMessageHistory(
        table_name=TABLE_NAME, 
        session_id=session_id
    )

# Agent'ımızı sohbet geçmişi yeteneğiyle sarmalıyoruz
conversational_agent = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# --- Lambda'nın Ana Giriş Fonksiyonu (Handler) ---
def lambda_handler(event, context):
    """
    Bu fonksiyon API Gateway tarafından tetiklenir.
    'event' parametresi, gelen isteğin tüm bilgilerini içerir.
    """
    print(f"Received event: {event}")

    try:
        # Gelen isteğin body'sini alıp JSON'dan Python dict'ine çeviriyoruz
        body = json.loads(event.get("body", "{}"))
        user_message = body.get("message")
        session_id = body.get("session_id")

        if not user_message or not session_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'message' or 'session_id' in request body"})
            }
        
        # Agent'ı çalıştır
        response = conversational_agent.invoke(
            {"input": user_message},
            config={"configurable": {"session_id": session_id}}
        )

        # Başarılı cevabı döndür
        return {
            "statusCode": 200,
            # CORS hatası almamak için header ekliyoruz
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({"response": response['output']})
        }

    except Exception as e:
        print(f"Error processing request: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "An internal error occurred."})
        }