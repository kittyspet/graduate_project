import os
import logging
import torch
from pathlib import Path
from typing import Optional, Union
from sentence_transformers import SentenceTransformer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from transformers import AutoTokenizer, AutoModelForCausalLM
from pybotx import IncomingMessage

logger = logging.getLogger(__name__)

MODEL_PATH = ""
EMBEDDING_MODEL_NAME = ""
DB_URL = ""
FILES_STORAGE = ""



class DeepSeekR1:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_PATH).to(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        self.model.eval()

    def generate(self, prompt: str, max_new_tokens: int = 512) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            top_p=0.95,
            do_sample=True,
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

class VectorDatabase:
    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url)
        self.async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    async def find_relevant_context(self, query: str, top_k: int = 1) -> str:
        query_embedding = self.embedding_model.encode([query])[0].tolist()
        async with self.async_session() as session:
            result = await session.execute(
                text(f"""
                    SELECT content
                    FROM embeddings
                    ORDER BY embedding <-> :embedding::vector
                    LIMIT {top_k}
                """),
                {"embedding": query_embedding},
            )
            rows = result.fetchall()
            return "\n".join(row[0] for row in rows) if rows else ""

class FileService:
    def __init__(self, storage_path: str):
        self.storage_path = Path(storage_path)

    def read_file(self, file_id: str) -> Optional[str]:
        file_path = self.storage_path / f"{file_id}.txt"  # Предполагаем, что файлы хранятся в виде .txt
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                logger.error(f"Ошибка при чтении файла {file_id}: {e}")
        return None

class NeuralBot:
    def __init__(self):
        self.model = DeepSeekR1()
        self.db = VectorDatabase(DB_URL)
        self.file_service = FileService(FILES_STORAGE)

    async def process_query(self, message: IncomingMessage) -> str:
        question = message.body
        file_id = message.file.id if message.file else None

        
        context = await self.db.find_relevant_context(question)

        
        if file_id:
            file_content = self.file_service.read_file(file_id)
            if file_content:
                context += f"\n\nФайл ({file_id}):\n{file_content[:1000]}"  

        
        prompt = f"""
        Контекст:
        {context}

        Вопрос:
        {question}

        Ответ:
        """.strip()

        
        try:
            response = self.model.generate(prompt)
            return response.split("Ответ:")[-1].strip()
        except Exception as e:
            logger.error(f"Ошибка генерации ответа: {e}")
            return "Произошла ошибка при обработке вашего запроса."


from pybotx import Bot

bot = Bot()

@bot.on.message()
async def handle_user_message(message: IncomingMessage):
    neural_bot = NeuralBot()
    response = await neural_bot.process_query(message)
    await message.state.bot.send_message(
        chat_id=message.chat.id,
        body=response,
    )