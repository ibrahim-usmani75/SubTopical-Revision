import json
import time

def load_data(filepath="questions.json"):
    """Loads and validates the JSON dataset without crashing."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                print("⚠️ Warning: questions.json is empty!")
                return []
            return json.loads(content)
    except FileNotFoundError:
        print(f"❌ Error: {filepath} file not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error reading JSON formatting: {e}")
        return []

# ==========================================
#          TIMER HELPER FUNCTION
# ==========================================

def get_timer_status(start_time, total_minutes=90):
    """Calculates elapsed time and returns remaining minutes status."""
    elapsed_seconds = time.time() - start_time
    elapsed_minutes = int(elapsed_seconds // 60)
    remaining_minutes = total_minutes - elapsed_minutes

    if remaining_minutes <= 0:
        return "🚨 TIME IS UP! (0 MINUTES LEFT)"
    elif remaining_minutes <= 5:
        return f"⚠️ 5 MINUTES LEFT! ({remaining_minutes} Mins Remaining)"
    else:
        return f"⏱️  Time Remaining: {remaining_minutes} Mins"

# ==========================================
#       SEARCH & FILTERING FUNCTIONS
# ==========================================

def search_questions(data, keyword="", paper_code="", session="", min_year=None, max_year=None):
    """Filters questions by keyword, paper code, session, or year range."""
    results = []
    keyword_clean = keyword.lower().strip()
    paper_clean = paper_code.lower().strip()
    session_clean = session.lower().strip()

    for q in data:
        # Check Keyword match
        matches_keyword = True
        if keyword_clean:
            matches_keyword = (
                keyword_clean in q.get("subtopic", "").lower() or
                keyword_clean in q.get("learning_objective", "").lower() or
                keyword_clean in q.get("question_text", "").lower()
            )

        # Check Specific Paper match (e.g., 's24_11' or '9618_s24_qp_11')
        matches_paper = True
        if paper_clean:
            matches_paper = paper_clean in q.get("id", "").lower()

        # Check Session match (e.g., 'May/June' or 'Oct/Nov')
        matches_session = True
        if session_clean:
            matches_session = session_clean in q.get("session", "").lower()

        # Check Year Range match
        matches_year = True
        q_year = q.get("year", 0)
        if min_year is not None and max_year is not None:
            matches_year = min_year <= q_year <= max_year

        if matches_keyword and matches_paper and matches_session and matches_year:
            results.append(q)

    return results

# ==========================================
#            DISPLAY FUNCTIONS
# ==========================================

def display_question(q, show_ms_directly=False, start_time=None):
    """Displays question metadata, text, and optionally handles interactive MS reveal."""
    marks = q.get('marks_alloted', q.get('marks', 'N/A'))
    
    print("\n" + "="*70)
    if start_time:
        print(f"{get_timer_status(start_time)}")
        print("-" * 70)
        
    print(f"📌 [{q.get('session', '')} {q.get('year', '')}] Paper {q.get('paper', '')} - Q{q.get('question_number', '')}  |  [{marks} Marks]")
    print(f"🏷️  Subtopic: {q.get('subtopic', 'N/A')}")
    print(f"🎯 Objective: {q.get('learning_objective', 'N/A')}")
    print("-" * 70)
    print(f"\n❓ QUESTION:\n{q.get('question_text', '')}\n")
    
    if show_ms_directly:
        print("✅ MARK SCHEME:")
        ms = q.get('mark_scheme', [])
        if isinstance(ms, list):
            for point in ms:
                print(f"  • {point}")
        else:
            print(f"  • {ms}")
            
        if q.get('examiner_report'):
            print(f"\n💡 EXAMINER REPORT:\n  {q.get('examiner_report')}")
    else:
        choice = input("👉 Show Mark Scheme? (y/n): ").strip().lower()
        if choice == 'y':
            print("\n✅ MARK SCHEME:")
            ms = q.get('mark_scheme', [])
            if isinstance(ms, list):
                for point in ms:
                    print(f"  • {point}")
            else:
                print(f"  • {ms}")
                
            if q.get('examiner_report'):
                print(f"\n💡 EXAMINER REPORT:\n  {q.get('examiner_report')}")
        else:
            print("Mark Scheme hidden.")
            
    print("="*70)

# ==========================================
# 📝 MODE 1: SEARCH BY KEYWORD (ENHANCED)
# ==========================================
def handle_keyword_search(data):
    """Handles search with sub-options for scoping paper ranges."""
    print("\n--- SEARCH SCOPE SELECTION ---")
    print("1. Search across ALL available papers")
    print("2. Search within a SPECIFIC Paper (e.g., s24_11)")
    print("3. Search by SPECIFIC Session & Year (e.g., May/June 2025)")
    print("4. Search across a RANGE of Years (e.g., 2024 to 2025)")
    
    scope_choice = input("\nSelect scope option (1-4): ").strip()
    kw = input("Enter search keyword/subtopic (e.g., 'printer', 'security'): ").strip()
    
    results = []
    
    if scope_choice == "1":
        results = search_questions(data, keyword=kw)
        
    elif scope_choice == "2":
        paper_code = input("Enter paper code (e.g., 's24_11' or 'w24_12'): ").strip()
        results = search_questions(data, keyword=kw, paper_code=paper_code)
        
    elif scope_choice == "3":
        sess_input = input("Enter session (1 for May/June, 2 for Oct/Nov): ").strip()
        session_str = "May/June" if sess_input == "1" else "Oct/Nov"
        try:
            yr = int(input("Enter year (e.g., 2025): ").strip())
            results = search_questions(data, keyword=kw, session=session_str, min_year=yr, max_year=yr)
        except ValueError:
            print("❌ Invalid year entered.")
            return

    elif scope_choice == "4":
        try:
            start_yr = int(input("Enter start year (e.g., 2024): ").strip())
            end_yr = int(input("Enter end year (e.g., 2025): ").strip())
            results = search_questions(data, keyword=kw, min_year=start_yr, max_year=end_yr)
        except ValueError:
            print("❌ Invalid year range entered.")
            return
    else:
        print("❌ Invalid selection.")
        return

    print(f"\nFound {len(results)} matching question(s):")
    for idx, q in enumerate(results, 1):
        print(f"\n--- Result {idx} of {len(results)} ---")
        display_question(q, show_ms_directly=False)
        if idx < len(results):
            cont = input("\nPress [ENTER] for next question (or 'q' to return to main menu): ").strip().lower()
            if cont == 'q':
                break

# ==========================================
# 🎓 MODE 2: ATTEMPT A YEARLY PAST PAPER
# ==========================================
def handle_yearly_attempt(data):
    """Simulates a full past paper exam environment."""
    print("\n==========================================")
    print(" 📝 ATTEMPT A YEARLY PAST PAPER")
    print("==========================================")
    
    # 1. Ask Year
    try:
        yr = int(input("Enter Year (e.g., 2024, 2025): ").strip())
    except ValueError:
        print("❌ Invalid year.")
        return

    # 2. Ask Session
    print("\nSelect Session:")
    print("1. May/June (s)")
    print("2. Oct/Nov (w)")
    sess_choice = input("Enter choice (1 or 2): ").strip()
    session_str = "May/June" if sess_choice == "1" else "Oct/Nov"
    session_code = "s" if sess_choice == "1" else "w"

    # 3. Ask Variant
    variant = input("Enter Variant/Paper number (e.g., 11, 12, 13): ").strip()

    # Formulate Paper Identifier
    paper_num = int(variant) if variant.isdigit() else 11
    paper_search_id = f"{session_code}{str(yr)[-2:]}_{variant}"

    # Filter Dataset for Exact Paper
    paper_questions = [
        q for q in data 
        if q.get("year") == yr 
        and session_str.lower() in q.get("session", "").lower() 
        and (q.get("paper") == paper_num or paper_search_id in q.get("id", "").lower())
    ]

    if not paper_questions:
        print(f"\n❌ No questions found for {session_str} {yr} Paper {variant}.")
        print("💡 Ensure your questions.json has 'year', 'session', and 'paper' fields filled accurately.")
        return

    # Display Exam Header
    print("\n" + "═"*60)
    print(f"  📋 EXAM PAPER: Cambridge 9618/1{variant[-1]} {session_str} {yr}")
    print(f"  ⏱️  TIME DURATION: 1 Hour 30 Minutes (90 Mins)")
    print(f"  💯 TOTAL MARKS: 75 Marks")
    print(f"  ❓ TOTAL QUESTIONS IN DATASET: {len(paper_questions)}")
    print(f"  GOOD LUCK!")
    print("═"*60 + "\n")

    # Ask View Mode
    print("How would you like to attempt this paper?")
    print("1. One by One (Interactive - test yourself with live timer)")
    print("2. All Questions at Once (with Mark Schemes)")
    view_mode = input("Select mode (1 or 2): ").strip()

    # Start 90-Minute Timer
    start_time = time.time()

    if view_mode == "1":
        print("\n🚀 EXAM STARTED! Timer running...")
        for idx, q in enumerate(paper_questions, 1):
            print(f"\n--- Question {idx} of {len(paper_questions)} ---")
            display_question(q, show_ms_directly=False, start_time=start_time)
            
            if idx < len(paper_questions):
                cont = input("\nPress [ENTER] for next question (or 'q' to end exam): ").strip().lower()
                if cont == 'q':
                    print("\n🛑 Exam session ended early.")
                    break
        
        elapsed_total = int((time.time() - start_time) // 60)
        print(f"\n🎉 EXAM COMPLETED in {elapsed_total} minutes!")

    elif view_mode == "2":
        print("\n📄 DISPLAYING FULL EXAM PAPER & MARK SCHEMES:\n")
        for idx, q in enumerate(paper_questions, 1):
            print(f"\n--- Question {idx} of {len(paper_questions)} ---")
            display_question(q, show_ms_directly=True)
            
        print("\n✅ End of Paper.")

# ==========================================
#                MAIN MENU
# ==========================================
def main_menu():
    """Interactive CLI menu meeting rubric UX guidelines."""
    data = load_data()
    print(f"\n==========================================")
    print(f" 🎯 9618 P1 Revision & Exam Tool")
    print(f"==========================================")
    print(f"Loaded {len(data)} questions from dataset.\n")

    while True:
        print("\nMain Menu:")
        print("1. Search Questions by Keyword / Subtopic (with Scope Filters)")
        print("2. Attempt a Yearly Past Paper (Full Exam Mode)")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()

        if choice == "1":
            handle_keyword_search(data)

        elif choice == "2":
            handle_yearly_attempt(data)

        elif choice == "3":
            print("\nExiting application. Good luck with your 9618 revision!")
            break
        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()