import json

from pytest_mock import MockerFixture

from k8s_triage.agent.tools import TOOLS_REGISTRY, execute_tool, get_openai_tools


def test_get_openai_tools() -> None:
    tools = get_openai_tools()
    assert len(tools) == len(TOOLS_REGISTRY)
    assert all(t["type"] == "function" for t in tools)
    assert all(t["function"]["strict"] is True for t in tools)


def test_execute_tool_invalid_name() -> None:
    result = execute_tool("invalid_tool", "{}")
    assert "Error: Tool invalid_tool not found." in result


def test_execute_tool_invalid_args(mocker: MockerFixture) -> None:
    # This will fail pydantic validation
    result = execute_tool("list_pods_with_conditions", json.dumps({"wrong_arg": "default"}))
    assert "Error executing tool" in result
    assert "Field required" in result or "namespace" in result


def test_execute_tool_valid(mocker: MockerFixture) -> None:
    mock_api = mocker.MagicMock()
    
    mock_ns = mocker.MagicMock()
    mock_ns.metadata.name = "default"
    mock_ns2 = mocker.MagicMock()
    mock_ns2.metadata.name = "kube-system"
    mock_api.list_namespace.return_value.items = [mock_ns, mock_ns2]
    
    mocker.patch("k8s_triage.k8s.operations.get_core_v1_api", return_value=mock_api)
    result = execute_tool("list_namespaces", "{}")
    assert "default" in result
    assert "kube-system" in result
