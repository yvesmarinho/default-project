"""
Tests for Chat Capture Module (IMP-55)

Tests the ChatCapture, ChatMessage, and ChatMetadata classes.

Author: @yves_marinho
Created: 2026-04-14
"""

import json
from datetime import datetime
from pathlib import Path

import pytest

from scripts.lib.chat_capture import ChatCapture, ChatMessage, ChatMetadata


# Fixtures

@pytest.fixture
def sample_transcript_data():
    """Sample transcript JSONL entries."""
    return [
        {
            "type": "session.start",
            "data": {
                "sessionId": "test-session-123",
                "version": 1,
                "producer": "copilot-agent",
            },
            "id": "session-start-id",
            "timestamp": "2026-04-14T10:00:00.000Z",
            "parentId": None
        },
        {
            "type": "user.message",
            "data": {"content": "Hello, can you help me with IMP-55?"},
            "id": "user-msg-1",
            "timestamp": "2026-04-14T10:00:05.000Z",
            "parentId": "session-start-id"
        },
        {
            "type": "assistant.message",
            "data": {
                "content": "Sure! I'll help with IMP-55 (Sistema CHAT-*.md).",
                "toolRequests": [
                    {"toolCallId": "tool-1", "name": "read_file", "arguments": "{}"}
                ],
                "reasoningText": "User is asking about IMP-55..."
            },
            "id": "assistant-msg-1",
            "timestamp": "2026-04-14T10:00:10.000Z",
            "parentId": "user-msg-1"
        }
    ]


@pytest.fixture
def temp_transcript(tmp_path, sample_transcript_data):
    """Create temporary transcript file."""
    transcript_path = tmp_path / "test-session-123.jsonl"
    with open(transcript_path, "w", encoding="utf-8") as f:
        for entry in sample_transcript_data:
            f.write(json.dumps(entry) + "\n")
    return transcript_path


# ChatMessage tests

def test_chat_message_creation():
    """Test ChatMessage dataclass creation."""
    msg = ChatMessage(
        role="user",
        content="Test message",
        timestamp=datetime.now(),
        message_id="msg-123",
    )

    assert msg.role == "user"
    assert msg.content == "Test message"
    assert msg.message_id == "msg-123"
    assert msg.parent_id is None
    assert msg.tool_requests == []


def test_chat_message_to_markdown():
    """Test ChatMessage markdown conversion."""
    msg = ChatMessage(
        role="assistant",
        content="Hello from assistant",
        timestamp=datetime(2026, 4, 14, 10, 30, 0),
        message_id="msg-456",
        tool_requests=[{"name": "read_file"}, {"name": "grep_search"}],
    )

    md = msg.to_markdown()

    assert "## 10:30:00 — ASSISTANT" in md
    assert "Hello from assistant" in md
    assert "**Tools used:**" in md
    assert "- `read_file`" in md
    assert "- `grep_search`" in md
    assert "---" in md


def test_chat_message_with_reasoning():
    """Test ChatMessage with reasoning text."""
    msg = ChatMessage(
        role="assistant",
        content="Response",
        timestamp=datetime(2026, 4, 14, 10, 30, 0),
        message_id="msg-789",
        reasoning_text="This is a long reasoning explanation that should be collapsed...",
    )

    md = msg.to_markdown()

    assert "<details>" in md
    assert "<summary>Reasoning</summary>" in md
    assert "This is a long reasoning" in md


# ChatMetadata tests

def test_chat_metadata_duration():
    """Test ChatMetadata duration calculation."""
    metadata = ChatMetadata(
        session_id="session-123",
        start_time=datetime(2026, 4, 14, 10, 0, 0),
        end_time=datetime(2026, 4, 14, 11, 30, 45),
    )

    assert metadata.duration_seconds == 5445  # 1h 30min 45s
    assert metadata.duration_formatted == "1h 30min 45s"


def test_chat_metadata_duration_short():
    """Test ChatMetadata short duration formatting."""
    metadata = ChatMetadata(
        session_id="session-123",
        start_time=datetime(2026, 4, 14, 10, 0, 0),
        end_time=datetime(2026, 4, 14, 10, 2, 30),
    )

    assert metadata.duration_seconds == 150
    assert metadata.duration_formatted == "2min 30s"


def test_chat_metadata_to_yaml_frontmatter():
    """Test ChatMetadata YAML frontmatter generation."""
    metadata = ChatMetadata(
        session_id="session-123",
        start_time=datetime(2026, 4, 14, 10, 0, 0),
        end_time=datetime(2026, 4, 14, 11, 0, 0),
        participants=[{"user": "yves_marinho"}, {"agent": "github-copilot"}],
        topics=["IMP-55", "chat capture", "testing"],
    )

    yaml_str = metadata.to_yaml_frontmatter()

    assert yaml_str.startswith("---\n")
    assert yaml_str.endswith("---\n")
    assert "type: chat" in yaml_str
    assert "session_date: '2026-04-14'" in yaml_str
    assert "session_id: session-123" in yaml_str
    assert "start_time: '10:00:00'" in yaml_str
    assert "end_time: '11:00:00'" in yaml_str
    assert "topics:" in yaml_str
    assert "- IMP-55" in yaml_str


# ChatCapture tests

def test_chat_capture_init(tmp_path):
    """Test ChatCapture initialization."""
    capture = ChatCapture(workspace_root=tmp_path)

    assert capture.workspace_root == tmp_path
    assert capture.sessions_dir == tmp_path / "docs" / "SESSIONS"


def test_parse_transcript(tmp_path, temp_transcript):
    """Test transcript parsing."""
    capture = ChatCapture(workspace_root=tmp_path)

    metadata, messages = capture.parse_transcript(temp_transcript)

    # Check metadata
    assert metadata.session_id == "test-session-123"
    assert metadata.start_time.year == 2026
    assert metadata.start_time.month == 4
    assert metadata.start_time.day == 14

    # Check messages
    assert len(messages) == 2  # user + assistant (session.start is not a message)

    # User message
    assert messages[0].role == "user"
    assert "IMP-55" in messages[0].content
    assert messages[0].message_id == "user-msg-1"

    # Assistant message
    assert messages[1].role == "assistant"
    assert "IMP-55" in messages[1].content
    assert len(messages[1].tool_requests) == 1
    assert messages[1].tool_requests[0]["name"] == "read_file"
    assert "reasoningText" in messages[1].content or messages[1].reasoning_text


def test_extract_topics():
    """Test topic extraction from messages."""
    capture = ChatCapture(workspace_root=Path.cwd())

    messages = [
        ChatMessage(
            role="user",
            content="Working on IMP-55 and IMP-56. Need to edit database.py and search.py",
            timestamp=datetime.now(),
            message_id="msg-1",
        ),
        ChatMessage(
            role="assistant",
            content="I'll help with the database implementation and search integration.",
            timestamp=datetime.now(),
            message_id="msg-2",
        )
    ]

    topics = capture.extract_topics(messages)

    # IMP-XXX patterns
    assert "IMP-55" in topics
    assert "IMP-56" in topics

    # Technical keywords
    assert "database" in topics or "search" in topics or "implementation" in topics

    # File extensions detected (database.py → database, py)
    assert len(topics) > 2  # Should extract multiple topics


def test_capture_to_markdown(tmp_path, temp_transcript):
    """Test full capture workflow."""
    # Setup
    sessions_dir = tmp_path / "docs" / "SESSIONS"
    sessions_dir.mkdir(parents=True)

    capture = ChatCapture(workspace_root=tmp_path)

    # Capture
    chat_path = capture.capture_to_markdown(temp_transcript, session_date="2026-04-14")

    # Verify file created
    assert chat_path.exists()
    assert chat_path.parent == sessions_dir / "2026-04-14"
    assert chat_path.name.startswith("CHAT-2026-04-14-")

    # Verify content
    content = chat_path.read_text()

    assert "---\n" in content[:10]  # YAML frontmatter
    assert "type: chat" in content
    assert "session_id: test-session-123" in content
    assert "# CHAT — 2026-04-14" in content
    assert "IMP-55" in content
    assert "## 10:00:" in content  # Timestamps
    assert "USER" in content
    assert "ASSISTANT" in content


def test_generate_markdown(tmp_path):
    """Test markdown generation."""
    capture = ChatCapture(workspace_root=tmp_path)

    metadata = ChatMetadata(
        session_id="test-session",
        start_time=datetime(2026, 4, 14, 10, 0, 0),
        end_time=datetime(2026, 4, 14, 11, 0, 0),
        topics=["testing", "implementation"],
    )

    messages = [
        ChatMessage(
            role="user",
            content="Test message",
            timestamp=datetime(2026, 4, 14, 10, 0, 5),
            message_id="msg-1",
        )
    ]

    md = capture._generate_markdown(metadata, messages)

    assert "---\n" in md[:10]
    assert "type: chat" in md
    assert "# CHAT — 2026-04-14 10:00" in md
    assert "**Session ID**: test-session" in md
    assert "**Duration**: 1h 0min 0s" in md
    assert "**Topics**: testing, implementation" in md
    assert "## 10:00:05 — USER" in md
    assert "Test message" in md
    assert "## Summary" in md


# Edge cases

def test_empty_transcript(tmp_path):
    """Test handling of empty transcript."""
    empty_transcript = tmp_path / "empty.jsonl"
    empty_transcript.write_text("")

    capture = ChatCapture(workspace_root=tmp_path)

    with pytest.raises(ValueError, match="missing session_id"):
        capture.parse_transcript(empty_transcript)


def test_malformed_jsonl(tmp_path):
    """Test handling of malformed JSONL."""
    bad_transcript = tmp_path / "bad.jsonl"
    bad_transcript.write_text("not valid json\n{also bad\n")

    capture = ChatCapture(workspace_root=tmp_path)

    # Should handle gracefully and skip bad lines
    with pytest.raises(ValueError):
        capture.parse_transcript(bad_transcript)


def test_very_long_conversation(tmp_path):
    """Test handling of very long conversation."""
    long_transcript = tmp_path / "long.jsonl"

    # Create transcript with many messages
    with open(long_transcript, "w", encoding="utf-8") as f:
        # Session start
        f.write(json.dumps({
            "type": "session.start",
            "data": {"sessionId": "long-session"},
            "id": "start",
            "timestamp": "2026-04-14T10:00:00.000Z",
            "parentId": None
        }) + "\n")

        # Generate 1000 messages
        for i in range(1000):
            f.write(json.dumps({
                "type": "user.message" if i % 2 == 0 else "assistant.message",
                "data": {"content": f"Message {i}"},
                "id": f"msg-{i}",
                "timestamp": f"2026-04-14T10:{i // 60:02d}:{i % 60:02d}.000Z",
                "parentId": f"msg-{i-1}" if i > 0 else "start"
            }) + "\n")

    capture = ChatCapture(workspace_root=tmp_path)
    metadata, messages = capture.parse_transcript(long_transcript)

    assert len(messages) == 1000
    assert metadata.duration_seconds > 0


# Integration test

def test_full_workflow_integration(tmp_path, temp_transcript):
    """Test complete workflow: detect, parse, capture, verify."""
    sessions_dir = tmp_path / "docs" / "SESSIONS"
    sessions_dir.mkdir(parents=True)

    capture = ChatCapture(workspace_root=tmp_path)

    # 1. Capture transcript
    chat_path = capture.capture_to_markdown(temp_transcript)

    assert chat_path.exists()

    # 2. Verify file structure
    assert chat_path.parent.name.startswith("2026-")
    assert chat_path.name.startswith("CHAT-")
    assert chat_path.suffix == ".md"

    # 3. Verify content structure
    content = chat_path.read_text()

    # YAML frontmatter
    assert content.startswith("---\n")
    assert "type: chat\n" in content

    # Title
    assert "# CHAT — " in content

    # Metadata summary
    assert "**Session ID**:" in content
    assert "**Duration**:" in content

    # Messages
    assert "## " in content  # At least one message header
    assert "USER" in content or "ASSISTANT" in content

    # Summary section
    assert "## Summary" in content
    assert "**Topics covered**:" in content
    assert "**Decisions made**:" in content
    assert "**Next steps**:" in content
