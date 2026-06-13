# arena-backend/seed.py
from pymongo import MongoClient
import random

# Connect to Database
client = MongoClient('mongodb://localhost:27017/')
db = client['buildathon_db']
challenges = db['challenges']

# Wipe existing data for a clean slate
challenges.delete_many({})

# 15 Core Algorithmic Paradigms (Overflow-Safe)
paradigms = [
    {"type": "Arithmetic", "func": "sum_val", "desc": "Return the sum of A and B.", "op": lambda a,b: a+b, "bug": "-", "correct": "+"},
    {"type": "Arithmetic", "func": "diff_val", "desc": "Return the absolute difference between A and B.", "op": lambda a,b: abs(a-b), "bug": "+", "correct": "-"},
    {"type": "Arithmetic", "func": "mult_val", "desc": "Return the product of A and B.", "op": lambda a,b: a*b, "bug": "/", "correct": "*"},
    {"type": "Logic", "func": "max_val", "desc": "Return the maximum of A and B.", "op": lambda a,b: max(a,b), "bug": "<", "correct": ">"},
    {"type": "Logic", "func": "min_val", "desc": "Return the minimum of A and B.", "op": lambda a,b: min(a,b), "bug": ">", "correct": "<"},
    {"type": "Bitwise", "func": "bit_and", "desc": "Return the bitwise AND of A and B.", "op": lambda a,b: a&b, "bug": "|", "correct": "&"},
    {"type": "Bitwise", "func": "bit_or", "desc": "Return the bitwise OR of A and B.", "op": lambda a,b: a|b, "bug": "&", "correct": "|"},
    {"type": "Bitwise", "func": "bit_xor", "desc": "Return the bitwise XOR of A and B.", "op": lambda a,b: a^b, "bug": "&", "correct": "^"},
    {"type": "Math", "func": "mod_val", "desc": "Return A modulo B (remainder).", "op": lambda a,b: a%b if b!=0 else 0, "bug": "/", "correct": "%"},
    {"type": "Math", "func": "floor_div", "desc": "Return integer division of A by B.", "op": lambda a,b: a//b if b!=0 else 0, "bug": "*", "correct": "/"},
    {"type": "Geometry", "func": "perimeter", "desc": "Calculate perimeter of a rectangle (2A + 2B).", "op": lambda a,b: 2*a + 2*b, "bug": "*", "correct": "+"},
    {"type": "Polynomial", "func": "poly_eval", "desc": "Evaluate the expression (A*B) + A.", "op": lambda a,b: (a*b)+a, "bug": "-", "correct": "+"},
    {"type": "Bitwise", "func": "left_shift", "desc": "Return A bitwise left-shifted by 1.", "op": lambda a,b: a<<1, "bug": ">>", "correct": "<<"},
    {"type": "Bitwise", "func": "right_shift", "desc": "Return A bitwise right-shifted by 1.", "op": lambda a,b: a>>1, "bug": "<<", "correct": ">>"},
    {"type": "Math", "func": "avg_val", "desc": "Return the integer average of A and B.", "op": lambda a,b: (a+b)//2, "bug": "-", "correct": "+"}
]

seeded_data = []
global_id = 1

def generate_track(track_type, difficulty, count, xp_base, scale):
    global global_id
    is_breaker = (track_type == "BREAKER")
    
    for i in range(count):
        # Rotate through paradigms to ensure variety
        paradigm = paradigms[(global_id - 1) % len(paradigms)]
        
        # Generate 3 Unique Mathematical Test Cases
        tcs = []
        for _ in range(3):
            a = random.randint(1 * scale, 10 * scale)
            b = random.randint(2 * scale, 5 * scale) # Ensure B > 0 to avoid zero-division
            expected = paradigm["op"](a, b)
            tcs.append({"a": a, "b": b, "expected": expected})

        # Set narratives based on track type
        if is_breaker:
            task_desc = f"BUG HUNTING [{difficulty.upper()}]: The function `{paradigm['func']}(a, b)` is designed to {paradigm['desc'].lower()} However, a logic bug was introduced during the last commit. Find the syntax flaw and patch it."
            
            starter = {
                "python": f"def {paradigm['func']}(a, b):\n    # Fix the bug below\n    return a {paradigm['bug']} b",
                "javascript": f"function {paradigm['func']}(a, b) {{\n    // Fix the bug below\n    return a {paradigm['bug']} b;\n}}",
                "c": f"#include <stdio.h>\nlong long {paradigm['func']}(long long a, long long b) {{\n    // Fix the bug below\n    return a {paradigm['bug']} b;\n}}",
                "cpp": f"#include <iostream>\nusing namespace std;\nlong long {paradigm['func']}(long long a, long long b) {{\n    // Fix the bug below\n    return a {paradigm['bug']} b;\n}}",
                "java": f"public class Main {{\n    public static long {paradigm['func']}(long a, long b) {{\n        // Fix the bug below\n        return a {paradigm['bug']} b;\n    }}\n"
            }
        else:
            task_desc = f"BUILDER LAB [{difficulty.upper()}]: Target Function `{paradigm['func']}(a, b)`.\n\nObjective: {paradigm['desc']} Implement the solution completely from scratch to pass all memory checks."
            
            starter = {
                "python": f"def {paradigm['func']}(a, b):\n    # Write logic here\n    pass",
                "javascript": f"function {paradigm['func']}(a, b) {{\n    // Write logic here\n}}",
                "c": f"#include <stdio.h>\nlong long {paradigm['func']}(long long a, long long b) {{\n    // Write logic here\n    return 0;\n}}",
                "cpp": f"#include <iostream>\nusing namespace std;\nlong long {paradigm['func']}(long long a, long long b) {{\n    // Write logic here\n    return 0;\n}}",
                "java": f"public class Main {{\n    public static long {paradigm['func']}(long a, long b) {{\n        // Write logic here\n        return 0;\n    }}\n"
            }

        # Multi-Language Test Harness (Explicitly prints Case 1, Case 2, Case 3)
        test_logic = {
            "python": f"""
print('--- SYSTEM EVALUATION ---')
passed = 0
try:
    if {paradigm['func']}({tcs[0]['a']}, {tcs[0]['b']}) == {tcs[0]['expected']}: print('Case 1: PASS'); passed += 1
    else: print('Case 1: FAIL')
    
    if {paradigm['func']}({tcs[1]['a']}, {tcs[1]['b']}) == {tcs[1]['expected']}: print('Case 2: PASS'); passed += 1
    else: print('Case 2: FAIL')
    
    if {paradigm['func']}({tcs[2]['a']}, {tcs[2]['b']}) == {tcs[2]['expected']}: print('Case 3: PASS'); passed += 1
    else: print('Case 3: FAIL')
    
    print('-------------------------')
    if passed == 3: print('Pass: All 3 Test Cases Successful')
    else: print(f'Failed: {{passed}}/3 Passed')
except Exception as e:
    print(f'Runtime Error: {{e}}')
""",
            "javascript": f"""
console.log('--- SYSTEM EVALUATION ---');
let passed = 0;
try {{
    if({paradigm['func']}({tcs[0]['a']}, {tcs[0]['b']}) === {tcs[0]['expected']}) {{ console.log('Case 1: PASS'); passed++; }}
    else console.log('Case 1: FAIL');
    
    if({paradigm['func']}({tcs[1]['a']}, {tcs[1]['b']}) === {tcs[1]['expected']}) {{ console.log('Case 2: PASS'); passed++; }}
    else console.log('Case 2: FAIL');
    
    if({paradigm['func']}({tcs[2]['a']}, {tcs[2]['b']}) === {tcs[2]['expected']}) {{ console.log('Case 3: PASS'); passed++; }}
    else console.log('Case 3: FAIL');
    
    console.log('-------------------------');
    if(passed === 3) console.log('Pass: All 3 Test Cases Successful');
    else console.log(`Failed: ${{passed}}/3 Passed`);
}} catch(e) {{ console.log('Runtime Error: ' + e.message); }}
""",
            "c": f"""
int main() {{
    printf("--- SYSTEM EVALUATION ---\\n");
    int p = 0;
    if({paradigm['func']}({tcs[0]['a']}, {tcs[0]['b']}) == {tcs[0]['expected']}) {{ printf("Case 1: PASS\\n"); p++; }}
    else printf("Case 1: FAIL\\n");
    
    if({paradigm['func']}({tcs[1]['a']}, {tcs[1]['b']}) == {tcs[1]['expected']}) {{ printf("Case 2: PASS\\n"); p++; }}
    else printf("Case 2: FAIL\\n");
    
    if({paradigm['func']}({tcs[2]['a']}, {tcs[2]['b']}) == {tcs[2]['expected']}) {{ printf("Case 3: PASS\\n"); p++; }}
    else printf("Case 3: FAIL\\n");
    
    printf("-------------------------\\n");
    if(p == 3) printf("Pass: All 3 Test Cases Successful\\n");
    else printf("Failed: %d/3 Passed\\n", p);
    return 0;
}}
""",
            "cpp": f"""
int main() {{
    cout << "--- SYSTEM EVALUATION ---\\n";
    int p = 0;
    if({paradigm['func']}({tcs[0]['a']}, {tcs[0]['b']}) == {tcs[0]['expected']}) {{ cout << "Case 1: PASS\\n"; p++; }}
    else cout << "Case 1: FAIL\\n";
    
    if({paradigm['func']}({tcs[1]['a']}, {tcs[1]['b']}) == {tcs[1]['expected']}) {{ cout << "Case 2: PASS\\n"; p++; }}
    else cout << "Case 2: FAIL\\n";
    
    if({paradigm['func']}({tcs[2]['a']}, {tcs[2]['b']}) == {tcs[2]['expected']}) {{ cout << "Case 3: PASS\\n"; p++; }}
    else cout << "Case 3: FAIL\\n";
    
    cout << "-------------------------\\n";
    if(p == 3) cout << "Pass: All 3 Test Cases Successful\\n";
    else cout << "Failed: " << p << "/3 Passed\\n";
    return 0;
}}
""",
            "java": f"""
    public static void main(String[] args) {{
        System.out.println("--- SYSTEM EVALUATION ---");
        int p = 0;
        try {{
            if({paradigm['func']}({tcs[0]['a']}, {tcs[0]['b']}) == {tcs[0]['expected']}) {{ System.out.println("Case 1: PASS"); p++; }}
            else System.out.println("Case 1: FAIL");
            
            if({paradigm['func']}({tcs[1]['a']}, {tcs[1]['b']}) == {tcs[1]['expected']}) {{ System.out.println("Case 2: PASS"); p++; }}
            else System.out.println("Case 2: FAIL");
            
            if({paradigm['func']}({tcs[2]['a']}, {tcs[2]['b']}) == {tcs[2]['expected']}) {{ System.out.println("Case 3: PASS"); p++; }}
            else System.out.println("Case 3: FAIL");
            
            System.out.println("-------------------------");
            if(p == 3) System.out.println("Pass: All 3 Test Cases Successful");
            else System.out.println("Failed: " + p + "/3 Passed");
        }} catch(Exception e) {{ System.out.println("Runtime Error"); }}
    }}
}}
"""
        }

        doc = {
            "id": global_id,
            "difficulty": difficulty.lower(),
            "track_type": track_type,
            "title": f"{track_type}: {paradigm['type']} Task {i + 1}",
            "xp_reward": xp_base,
            "description": task_desc,
            "test_cases": tcs,
            "starter_code": starter,
            "test_logic": test_logic
        }
        seeded_data.append(doc)
        global_id += 1

# Generate exactly 50 Builder Labs
generate_track("BUILDER", "Easy", 17, 100, 1)
generate_track("BUILDER", "Medium", 17, 250, 10)
generate_track("BUILDER", "Hard", 16, 500, 100)

# Generate exactly 50 Breaker Labs
generate_track("BREAKER", "Easy", 17, 150, 1)
generate_track("BREAKER", "Medium", 17, 300, 10)
generate_track("BREAKER", "Hard", 16, 600, 100)

challenges.insert_many(seeded_data)
print(f"Data Payload Confirmed: Seeded exactly {len(seeded_data)} execution environments (50 Builders, 50 Breakers).")