from unittest.mock import patch
from solarmind.graph import critic_node

@patch('solarmind.graph.llm.invoke')
def test_critic_loop(mock_invoke):
    """
    Test Phase 5 implementation - the critic logic node loop.
    Ensures that when the LLM outputs a failure, the critique flag triggers a loop.
    """
    # Mock LLM response to explicitly mimic the 'FAIL' critique condition setup.
    mock_invoke.return_value = "This report lacks PatchTST info. FAIL."
    state = {"research_report": "Junk data", "critique_flag": False}
    
    # Process evaluating state transition mechanism
    result = critic_node(state)
    
    assert result['critique_flag'] == True, "Critic failed to flag report returning loop."
