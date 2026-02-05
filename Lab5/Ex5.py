responses = [5, 7, 3, 8]
responses_ids = (1012, 1035, 1021, 1053)

survey_dict = dict(zip(responses_ids, responses))
print("Survey responses with respondent IDs:" , survey_dict)

print(f"Response from respondent 1021: {survey_dict[1021]}")