def determine_progress1(hits, spins):
    if spins == 0:
        return "Get going!"
    
    hits_spins_ratio = hits / spins

    if hits_spins_ratio > 0:
        progress = "On your way!"
        if hits_spins_ratio >= 0.25:
            progress = "Almost there!"
            if hits_spins_ratio >= 0.5:
                if hits < spins:
                    progress = "You win!"
    else:
        progress = "Get going!"

    return progress

def test_determine_progress(progress_function):
   # Test case 1: spins = 0 returns “Get going!”
    assert progress_function(10, 0) == "Get going!", "Test case 1 failed"
    # Test case 2: hits = 0 and spins = 10 returns “Get going!”
    assert progress_function(0, 10) == "Get going!", "Test case 2 failed"
    # Test case 3: hits = 2 and spins = 10 returns “On your way!”
    assert progress_function(2, 10) == "On your way!", "Test case 3 failed"
    # Test case 4: hits = 3 and spins = 8 returns “Almost there!”
    assert progress_function(3, 8) == "Almost there!", "Test case 4 failed"
    # Test case 5: hits = 5 and spins = 10 returns “You win!”
    assert progress_function(5, 10) == "You win!", "Test case 5 failed"

    print("All test cases passed!")


#Rewrite the determine_progress1 function without using nested if-statements. 
# Do not use elif or else. Call it determine_progress2. 
# Use your test cases to ensure the function works as expected. 
def determine_progress2(hits, spins):
    if spins == 0:
        return "Get going!"
    
    hits_spins_ratio = hits / spins

    if hits_spins_ratio <= 0:
        return "Get going!"
    
    if hits_spins_ratio > 0 and hits_spins_ratio < 0.25:
        return "On your way!"
    
    if hits_spins_ratio >= 0.25 and hits_spins_ratio < 0.5:
        return "Almost there!"
    
    if hits_spins_ratio >= 0.5 and hits < spins:
        return "You win!"
    
    return "On your way!" 

''' Rewrite determine_progress2 function using if-elif conditions. Call it determine_progress3. 
Use your test cases to ensure the function works as expected. 
Explain which version is “better” determine_progress 1,2, or 3?'''

def determine_progress3(hits, spins):
    if spins == 0:
        return "Get going!"
    
    hits_spins_ratio = hits / spins

    if hits_spins_ratio <= 0:
        return "Get going!"
    elif hits_spins_ratio > 0 and hits_spins_ratio < 0.25:
        return "On your way!"
    elif hits_spins_ratio >= 0.25 and hits_spins_ratio < 0.5:
        return "Almost there!"
    elif hits_spins_ratio >= 0.5 and hits < spins:
        return "You win!"
    
    return "On your way!"