from unittest.mock import patch
import builtins
from click.testing import CliRunner
from openai_agent.cli import cli


@patch.object(builtins, 'input', lambda _: '')
def test_cli_run_with_arg(mock_dependencies):
    runner = CliRunner()
    result = runner.invoke(cli, ['--task', 'sample_task'], '\n')
    assert result.exit_code == 0
    assert 'Response from OpenAI' in result.output
