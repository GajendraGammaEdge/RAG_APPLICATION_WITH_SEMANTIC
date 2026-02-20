from sqlalchemy.orm import Session
from utils.prompt_loader import load_prompt
from service.user_service import get_user_by_id
from utils.semantic_search import SemanticSearch
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi import HTTPException
from db_configuration.config import settings

openai_api_key = settings.openai_apikey
gemini_api_key = settings.google_api_key


gpt_lllm = OpenAI(
    api_key=openai_api_key,
    temperature=0.6,
    max_tokens=1500,
    max_retries=3,
    model="gpt-4o-mini"
)

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    api_key=gemini_api_key
)


class RagUtilsGPT:
    def __init__(self, db: Session):
        self.db = db
        self.semantic_search = SemanticSearch(db)

    async def gpt_5_model(
        self,
        query: str,
        top_k: int = 5,
        query_vector: list[float] | None = None,
        user_id: int | None = None,
    ):
        try:
            chunks = await self.semantic_search.cosine_search(
                top_k=top_k,
                query_vector=query_vector,
            )

            if not chunks:
                return "No relevant information found."

            context = "\n".join(chunks)

            user = get_user_by_id(self.db, user_id)
            if not user:
                raise ValueError("User not found")

            prompt_text = load_prompt(
                "document_summary.prompt",
                user_name=user.user_name,
                age=user.age,
                profession=user.profession,
            )

            full_prompt = f"""
            {prompt_text}

            Document Content:
            {context}

            Question:
            {query}

            Answer:
            """

            prompt_template = PromptTemplate(
                input_variables=["input"],
                template="{input}",
            )

            chain = prompt_template | gpt_lllm | StrOutputParser()
            response = await chain.ainvoke({"input": full_prompt})

            return response

        except Exception as e:
            return f"GPT-5 model error: {str(e)}"

    async def gpt_4_model(
        self,
        query: str,
        top_k: int = 5,
        query_vector: list[float] | None = None,
        user_id: int | None = None,
    ):
        try:
            chunks = await self.semantic_search.euclidean_search(
                top_k=top_k,
                query_vector=query_vector,
            )

            if not chunks:
                return "No relevant information found."

            context = "\n".join(chunks)

            user = get_user_by_id(self.db, user_id)
            if not user:
                raise ValueError("User not found")

            prompt_text = load_prompt(
                "document_summary.prompt",
                user_name=user.user_name,
                age=user.age,
                profession=user.profession,
            )

            full_prompt = f"""
            {prompt_text}
            Document Content:
            {context}
            Question:
            {query}
            Answer:
            """

            prompt_template = PromptTemplate(
                input_variables=["input"],
                template="{input}",
            )

            chain = prompt_template | gpt_lllm | StrOutputParser()
            response = await chain.ainvoke({"input": full_prompt})

            return response

        except Exception as e:
            return f"GPT-4 model error: {str(e)}"

    async def gemini_25_model(
        self,
        query: str,
        top_k: int = 5,
        query_vector: list[float] | None = None,
        user_id: int | None = None,
    ):
        try:
            chunks = await self.semantic_search.cosine_search(
                top_k=top_k,
                query_vector=query_vector,
            )

            if not chunks:
                return "No relevant information found."

            context = "\n".join(chunks)

            user = get_user_by_id(self.db, user_id)
            if not user:
                raise ValueError("User not found")

            prompt_text = load_prompt(
                "document_summary.prompt",
                user_name=user.user_name,
                age=user.age,
                profession=user.profession,
            )

            full_prompt = f"""
            {prompt_text}

            Document Content:
            {context}

            Question:
            {query}

            Answer:
            """

            prompt_template = PromptTemplate(
                input_variables=["input"],
                template="{input}",
            )

            chain = prompt_template | gemini_llm | StrOutputParser()
            response = await chain.ainvoke({"input": full_prompt})

            return response

        except HTTPException:
            return (
                "Gemini 2.5 Flash Lite quota exceeded. "
                "Please retry later or switch model."
            )

        except Exception as e:
            return f"Gemini 2.5 model error: {str(e)}"

    async def gemini_2_model(
        self,
        query: str,
        top_k: int = 5,
        query_vector: list[float] | None = None,
        user_id: int | None = None,
    ):
        try:
            chunks = await self.semantic_search.euclidean_search(
                top_k=top_k,
                query_vector=query_vector,
            )

            if not chunks:
                return "No relevant information found."

            context = "\n".join(chunks)

            user = get_user_by_id(self.db, user_id)
            if not user:
                raise ValueError("User not found")

            prompt_text = load_prompt(
                "document_summary.prompt",
                user_name=user.user_name,
                age=user.age,
                profession=user.profession,
            )

            full_prompt = f"""
            {prompt_text}
            Document Content:
            {context}
            Question:
            {query}
            Answer:
            """

            prompt_template = PromptTemplate(
                input_variables=["input"],
                template="{input}",
            )

            chain = prompt_template | gemini_llm | StrOutputParser()
            response = await chain.ainvoke({"input": full_prompt})

            return response

        except HTTPException:
            return "Gemini 2.0 Flash quota exceeded."

        except Exception as e:
            return f"Gemini 2.0 model error: {str(e)}"
