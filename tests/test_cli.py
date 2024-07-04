from click.testing import CliRunner

from openai_agent.cli import cli


def test_cli_direct_run(mock_dependencies):
    runner = CliRunner()
    result = runner.invoke(cli, ['run', '--task', 'sample_task'], '\n')
    assert 'Response from OpenAI' in result.output
