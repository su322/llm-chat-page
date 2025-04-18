from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import requests, json
from datetime import datetime

# Tortoise ORM models
from src.core.database.models import ChatSession, Conversation

router = APIRouter(tags=["chat"])


# ——— Pydantic Schemas ——————————————————————————————————————————

class MessageRequest(BaseModel):
    message: str
    model: str = "deepseek-r1:latest"


class SessionCreateRequest(BaseModel):
    user_id: int
    title: str = "新对话"


class SessionResponse(BaseModel):
    id: int
    user_id: int
    title: str
    created_at: datetime

    class Config:
        orm_mode = True


class ConversationResponse(BaseModel):
    id: int
    user_message: str
    ai_message: str
    timestamp: datetime
    session_id: Optional[int]

    class Config:
        orm_mode = True


# ——— 配置 ———————————————————————————————————————————————————————

OLLAMA_API_URL = "http://ollama:11434/api/generate"


# ——— 会话管理 Endpoints —————————————————————————————————————————


@router.post("/sessions", response_model=SessionResponse)
async def create_session(req: SessionCreateRequest):
    """创建新对话会话"""
    session = await ChatSession.create(user_id=req.user_id, title=req.title)
    return session


@router.get("/sessions", response_model=List[SessionResponse])
async def list_sessions(user_id: int = Query(..., description="用户 ID")):
    """列出指定用户的所有会话"""
    sessions = await ChatSession.filter(user_id=user_id).order_by("-created_at")
    return sessions


@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session(session_id: int):
    """获取单个会话的信息"""
    session = await ChatSession.get_or_none(id=session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    return session


@router.delete("/sessions/{session_id}", status_code=204)
async def delete_session(session_id: int):
    """删除会话及其所有消息"""
    # 先删消息
    await Conversation.filter(session_id=session_id).delete()
    # 再删会话
    deleted = await ChatSession.filter(id=session_id).delete()
    if not deleted:
        raise HTTPException(404, "Session not found")
    return


# ——— 消息管理 Endpoints —————————————————————————————————————————


@router.get("/sessions/{session_id}/messages", response_model=List[ConversationResponse])
async def get_session_messages(session_id: int):
    """获取某个会话下的所有消息（按时间）"""
    msgs = await Conversation.filter(session_id=session_id).order_by("timestamp")
    return msgs


@router.post("/sessions/{session_id}/messages/stream")
async def send_message_stream(
    session_id: int,
    request: MessageRequest,
    background_tasks: BackgroundTasks,
):
    """
    流式发送用户消息给 Ollama，并在后台保存对话记录。
    """

    # 确保会话存在
    session = await ChatSession.get_or_none(id=session_id)
    if not session:
        raise HTTPException(404, "Session not found")

    # 向 Ollama 请求流式回答
    payload = {
        "model": request.model,
        "prompt": request.message,
        "stream": True
    }
    headers = {"Content-Type": "application/json"}
    ollama_resp = requests.post(
        OLLAMA_API_URL, json=payload, headers=headers, stream=True
    )
    if ollama_resp.status_code != 200:
        raise HTTPException(500, f"Ollama API error: {ollama_resp.text}")

    # 累积 AI 完整回答
    ai_response_parts: List[str] = []

    async def event_generator():
        for line in ollama_resp.iter_lines(decode_unicode=True):
            if not line:
                continue
            try:
                chunk = json.loads(line)
                text = chunk.get("response", "")
                ai_response_parts.append(text)
                yield text
            except Exception:
                yield "\n[Error parsing chunk]\n"

        # 整体对话结束后，后台存库
        full_ai_resp = "".join(ai_response_parts)
        background_tasks.add_task(
            Conversation.create,
            user_id=session.user_id,
            session_id=session.id,
            user_message=request.message,
            ai_message=full_ai_resp
        )

    return StreamingResponse(event_generator(), media_type="text/plain")


@router.post("/chat/stream")
async def chat_stream(request: MessageRequest):
    try:
        data = {
            "model": request.model,
            "prompt": request.message,
            "stream": True
        }

        headers = {
            "Content-Type": "application/json"
        }

        ollama_response = requests.post(f"{OLLAMA_API_URL}", json=data, headers=headers, stream=True)

        if ollama_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Ollama API error")

        def generate_stream():
            for line in ollama_response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        json_data = json.loads(line)
                        content = json_data.get("response", "")
                        yield content
                    except Exception as e:
                        yield f"\n[Error parsing chunk]: {e}"

        return StreamingResponse(generate_stream(), media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))