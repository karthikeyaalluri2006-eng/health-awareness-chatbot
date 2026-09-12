"""Quick integration test for HealthAware AI"""
from database.connection import get_db_session
from services.rag_service import RAGService
from auth.authentication import AuthService

# Test auth
success, msg, u_data = AuthService.login_user('demouser', 'User@123')
print(f'Auth login: {success} - {msg}')
if u_data:
    user_name = u_data.get('full_name', u_data.get('username'))
    print(f'User: {user_name} role={u_data["role"]}')

# Test full chat pipeline
uid = u_data['id'] if u_data else 1
with get_db_session() as db:
    result = RAGService.process_query(
        db=db,
        query='How can I prevent heart disease?',
        user_id=uid,
        conversation_id=None,
        language='en'
    )
    print(f'RAG success: {result["success"]}')
    sources = result.get('sources', [])
    print(f'Sources found: {len(sources)}')
    response = result.get('response', '')
    print(f'Response length: {len(response)} chars')
    print()
    print('=== RESPONSE PREVIEW ===')
    print(response[:500])
    print()
    if sources:
        print('=== SOURCES ===')
        for s in sources:
            print(f'  - {s["title"]} | {s["category"]}')

print('\n=== TEST PASSED ===')
