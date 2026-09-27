from unittest.mock import MagicMock

import pytest
from pytest import MonkeyPatch
from pytest_mock import MockerFixture

from k8s_triage.agent.loop import AgentController


def test_agent_controller_initialization_no_key(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("K8S_TRIAGE_OPENAI_API_KEY", "")
    with pytest.raises(ValueError, match="OpenAI API key must be provided"):
        AgentController()


def test_agent_controller_initialization_with_key(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test_key")
    agent = AgentController()
    assert agent.client is not None
    assert len(agent.messages) == 1
    assert agent.messages[0]["role"] == "system"


def test_agent_run_max_iterations(monkeypatch: MonkeyPatch, mocker: MockerFixture) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test_key")
    from k8s_triage.config import config
    config.max_tool_iterations = 2
    
    agent = AgentController()
    
    # Mock OpenAI client
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    
    # Simulate a tool call that never finishes answering
    mock_tool_call = MagicMock()
    mock_tool_call.function.name = "list_namespaces"
    mock_tool_call.function.arguments = "{}"
    mock_tool_call.id = "call_123"
    
    mock_message.tool_calls = [mock_tool_call]
    mock_message.model_dump.return_value = {"role": "assistant", "tool_calls": [{"id": "call_123", "type": "function", "function": {"name": "list_namespaces", "arguments": "{}"}}]}
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    
    # We must patch the function on the instance so we don't hit mypy 'Cannot assign to a method'
    mock_create = mocker.patch.object(agent.client.chat.completions, 'create', return_value=mock_response)
    
    mocker.patch("k8s_triage.agent.loop.execute_tool", return_value="['default']")
    
    result = agent.run("Check namespace")
    assert result == "Agent stopped: Reached maximum tool iterations limit."
    assert mock_create.call_count == 2
