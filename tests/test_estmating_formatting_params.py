import pytest

from musescore_part_formatter.estimating_formatting_params import predict_params_based_on_score_info


@pytest.mark.parametrize(
    "input_param, input_param_value, res_param, res_param_value", [
        ("num_staves", 6, "staff_spacing", '0.7246'),
        #TODO: Add more of these once more params are confuigured to be auto detected
    ]
)
def test_predict_params_based_on_score_info(input_param, input_param_value, res_param, res_param_value):
    score_info = {input_param: input_param_value}
    
    res = predict_params_based_on_score_info(score_info)
    assert res[res_param] == res_param_value


#TODO: Write tests that test that the getter fields get the right values from sample mscz files