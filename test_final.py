"""Final quality verification test"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from services.llm_service import get_llm_provider, _match_topic

tests = [
    ('What are the symptoms of diabetes?', 'diabetes'),
    ('How do I lower blood pressure?', 'hypertension'),
    ('Flu vs cold difference', 'flu'),
    ('Which vaccines should I get?', 'vaccination'),
    ('Healthy cholesterol levels', 'cholesterol'),
    ('How much sleep do adults need?', 'sleep'),
    ('Exercise benefits for heart', 'exercise'),
    ('Good nutrition tips', 'nutrition'),
    ('Anxiety and depression help', 'mental_health'),
    ('How to prevent heart disease?', 'heart'),
]

print('TOPIC DETECTION TEST:')
all_pass = True
for query, expected in tests:
    detected = _match_topic(query)
    status = 'PASS' if detected == expected else f'FAIL (got: {detected})'
    print(f'  [{status}] "{query}"')
    if 'FAIL' in status:
        all_pass = False

print()
print(f'All topic tests passed: {all_pass}')
print()

# Test full response quality for diabetes
llm = get_llm_provider()
test_prompt = 'User Question: What are the symptoms of diabetes?\n'
response = llm.generate_response(test_prompt)
print('DIABETES RESPONSE PREVIEW:')
print(response[:400])
print(f'\nResponse length: {len(response)} chars')
