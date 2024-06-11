

def calculate_WAWQI(predictions,standard_values, ideal_values, weights):
    subindices = {}
    del predictions['EC']
    del predictions['Temperature']
    for parameter in predictions:
        Vi = predictions[parameter]  # Directly use the predicted value
        Si = standard_values[parameter]
        Ii = ideal_values[parameter]
        subindices[parameter] = ((Vi - Ii) / (Si - Ii)) * 100
    

    
    weighted_subindices = {parameter: subindices[parameter] * weights[parameter] for parameter in subindices}
    WAWQI = sum(weighted_subindices.values()) / sum(weights.values())
    
    return WAWQI
