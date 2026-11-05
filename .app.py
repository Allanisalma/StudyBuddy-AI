import streamlit as st
from datetime import date
import database
import random
database.create_users_table()
if "logged_in"not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username =""
st.write("Database file:", database.__file__)
st.set_page_config(page_title="StudyBuddy AI", page_icon=":smiley:", layout="wide")
database.create_database()
st.title("StudyBuddy AI")
st.subheader("Your personal study assistant")
tasks = database.get_tasks()
completed_tasks = sum(task["completed"] for task in tasks)
col1, col2, col3 = st.columns(3)
col1.metric("Study tasks", len(tasks))
col2.metric("Completed tasks", completed_tasks)
col2.metric("Notes saved", 0)
col3.metric("Pending tasks", len(tasks) - completed_tasks)
st.divider()
if not st.session_state.logged_in:
    st.title("StudyBuddy AI")
    st.write("Your Personal study companion")
    auth_mode = st.radio("Choose an option",["Login", "Create account"],horizontal=True)
    with st.form("authentication_form"):
        username = st.text_input("Username")
        password = st.text_input("Password",type="password")
        submitted = st.form_submit_button("Continue")
    if submitted:
        if not username.strip() or not password:
            st.warning("Please enter your username and password.")
        elif auth_mode == "Create account":
            success, message = database.register_user(username, password)
            if success:
                st.success(message + " You can now log in.")
            else:
                st.error(message)
        else:
            if database.verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username.strip()
                st.rerun()
            else:
                st.error("Incorrect username or password.")
    st.stop()
st.sidebar.title("🎓 StudyBuddy AI")
st.sidebar.caption("Your personal learning space")
st.sidebar.divider()
st.sidebar.markdown("### 👤 My Account")
st.sidebar.success(f"Logged in as: {st.session_state.username}")
if st.sidebar.button("🚪 Log out", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()
st.sidebar.divider()
st.sidebar.markdown("### 📚 Navigation")
page_labels = {
    "Home": "🏠 Home",
    "Study Planner": "📅 Study Planner",
    "Smart Notes": "📝 Smart Notes",
    "Flashcards and Quizzes": "🧠 Flashcards and Quizzes",
    "Study Assistant": "🤖 Study Assistant",
    "Quiz History": "📊 Quiz History",
    "Study Goals": "🎯 Study Goals"
}
page = st.sidebar.selectbox("Choose a section", options=list(page_labels.keys()), format_func=lambda page: page_labels[page], label_visibility="collapsed")
st.sidebar.divider()
st.sidebar.caption("✨ Learn smarter, not harder.")
if page == "Home":
    st.title("🎓 StudyBuddy AI")
    st.markdown("### Welcome back! 👋")
    st.caption("Your personal space to organize, track, and improve your studies.")
    tasks = database.get_tasks()
    notes = database.get_notes()
    cards = database.get_flashcards()
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if int(task["completed"]) == 1)
    pending_tasks = total_tasks - completed_tasks
    total_notes = len(notes)
    st.write("DEBUG - Notes count:", total_notes)
    total_cards = len(cards)
    st.subheader("📊 Your Study Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📋 Total Tasks", total_tasks)
    with col2:
        st.metric("✅ Completed", completed_tasks)
    with col3:
        st.metric("⏳ Pending", pending_tasks)
    with col4:
        st.metric("📝 Smart Notes", total_notes)
    st.divider()
    st.subheader("📈 Your Progress")
    if total_tasks > 0:
        progress = completed_tasks / total_tasks
        st.progress(progress)
        st.write(f"*{round(progress * 100)}%* of your tasks completed.")
        if progress == 1:
            st.success("Excellent! You completed all your tasks! 🎉")
        elif progress >= 0.5:
            st.info("Great progress! Keep going. 💪")
        else:
            st.info("Keep working! Every small step counts.")
    else:
        st.info("You don't have any tasks yet. Start by adding your first task!")
    st.subheader("Task Analystics")
    if total_tasks > 0:
        chart_data = {"Completed":[completed_tasks], "Pending": [pending_tasks]}
        st.bar_chart(chart_data)
    else:
        st.info("Completed or add tasks to see your analystics.")
    st.divider()
    st.subheader("📅 Upcoming Deadlines")
    today = date.today()
    upcoming_tasks = [
        task for task in tasks
        if int(task["completed"]) == 0
        and task["due_date"]
        and task["due_date"] >= today.isoformat()
    ]
    upcoming_tasks.sort(key=lambda task: task["due_date"])
    if upcoming_tasks:
        for task in upcoming_tasks[:5]:
            due_date = date.fromisoformat(task["due_date"])
            days_left = (due_date - today).days
            if days_left == 0:
                label = "🔴 Due today!"
            elif days_left == 1:
                label = "🟠 Due tomorrow"
            else:
                label = f"🟢 {days_left} days left"
            with st.container(border=True):
                st.markdown(f"📌 {task['title']}**")
                st.caption(
                    f"Subject: {task['subject'] or 'Not specified'}"
                    f" | Due: {due_date.strftime('%d/%m/%Y')}"
                )
                st.write(label)
    else:
        st.success("No upcoming deadlines. You're all caught up! 🎉")
    st.divider()
    st.subheader("📚 Your Learning Resources")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📝 Saved Notes", total_notes)
    with col2:
        st.metric("🧠 Flashcards", total_cards)
elif page == "Study Planner":
    st.header("📅 Study Planner")
    st.caption("Organize your tasks and stay on top of your studies.")
    st.subheader("➕ Add a New Task")
    with st.form("task_form"):
        title = st.text_input("Task Title")
        subject = st.text_input("Subject")
        due_date = st.date_input("Due Date", value=date.today())
        submitted = st.form_submit_button("Add Task", use_container_width=True)
        if submitted:
            if title.strip():
                database.add_task(
                    title.strip(),
                    subject.strip(),
                    due_date.isoformat()
                )
                st.success("Task added successfully!")
                st.rerun()
            else:
                st.error("Please enter a task title.")
    st.divider()
    tasks = database.get_tasks()
    today = date.today()
    completed = [task for task in tasks if int(task["completed"]) == 1]
    pending = [task for task in tasks if int(task["completed"]) == 0]
    overdue = [task for task in pending if task["due_date"] and task["due_date"] < today.isoformat()]
    upcoming = [task for task in pending if not task["due_date"] or task["due_date"] >= today.isoformat()]
    st.subheader("📊 Task Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("📋 Total Tasks", len(tasks))
    col2.metric("⏳ Pending", len(pending))
    col3.metric("✅ Completed", len(completed))
    st.divider()
    def display_task(task):
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"*{task['title']}*")
                st.caption(f"Subject: {task['subject'] or 'Not specified'}")
                if task["due_date"]:
                    due = date.fromisoformat(task["due_date"])
                    st.caption(f"📅 Due: {due.strftime('%d/%m/%Y')}")
                else:
                    st.caption("📅 No due date")
            with col2:
                checked = st.checkbox("Completed", value=bool(task["completed"]), key=f"completed_{task['id']}")
                if checked != bool(task["completed"]):
                    database.update_task_status(task["id"], checked)
                    st.rerun()
                if st.button("🗑️ Delete", key=f"delete_{task['id']}", use_container_width=True):
                    database.delete_task(task["id"])
                    st.rerun()
    st.subheader("🔴 Overdue Tasks")
    if overdue:
        for task in sorted(overdue, key=lambda task: task["due_date"]):
            display_task(task)
    else:
        st.success("No overdue tasks!")
    st.subheader("📅 Upcoming Tasks")
    if upcoming:
        for task in sorted(upcoming, key=lambda task: task["due_date"] or "9999-12-31"):
            display_task(task)
    else:
        st.info("No pending upcoming tasks.")
    st.subheader("✅ Completed Tasks")
    if completed:
        for task in completed:
            display_task(task)
    else:
        st.info("No completed tasks yet.")
elif page == "Smart Notes":
    st.header("📝 Smart Notes")
    st.caption("Create, organize, and review your study notes.")
    with st.expander("➕ Create a New Note", expanded=True):
        with st.form("note_form"):
            title = st.text_input("Note title")
            subject = st.text_input("Subject")
            content = st.text_area("Your notes", height=200, placeholder="Write your study notes here...")
            submitted = st.form_submit_button("💾 Save Note", use_container_width=True)
            if submitted:
                if title.strip() and content.strip():
                    database.add_note(
                        title.strip(),
                        subject.strip(),
                        content.strip()
                    )
                    st.success("Note saved successfully!")
                    st.rerun()
                else:
                    st.error("Please enter a title and note content.")
    st.divider()
    notes = database.get_notes()
    st.subheader("📚 Your Learning Library")
    st.metric("Total saved notes", len(notes))
    if notes:
        search_query = st.text_input("🔎 Search notes", placeholder="Search by title, subject, or content...")
        subjects = sorted({note["subject"].strip() for note in notes if note["subject"] and note["subject"].strip()})
        selected_subject = st.selectbox("📂 Filter by subject", ["All Subjects"] + subjects)
        filtered_notes = notes
        if search_query.strip():
            query = search_query.strip().casefold()
            filtered_notes = [
                note for note in filtered_notes
                if query in (note["title"] or "").casefold()
                or query in (note["subject"] or "").casefold()
                or query in (note["content"] or "").casefold()
            ]
        if selected_subject != "All Subjects":
            filtered_notes = [note for note in filtered_notes if (note["subject"] or "").strip() == selected_subject]
        st.caption(f"Showing {len(filtered_notes)} note(s)")
        if filtered_notes:
            for note in filtered_notes:
                with st.container(border=True):
                    st.markdown(f"### 📝 {note['title']}")
                    st.caption(f"📚 Subject: {note['subject'] or 'Not specified'}")
                    preview = (note["content"] or "").strip()
                    if len(preview) > 250:
                        st.write(preview[:250] + "...")
                        with st.expander("Read full note"):
                            st.write(preview)
                    else:
                        st.write(preview)
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✏️ Edit Note", key=f"edit_note_{note['id']}", use_container_width=True):
                            st.session_state[f"editing_note_{note['id']}"] = True
                    with col2:
                        if st.button("🗑️ Delete note", key=f"delete_note_{note['id']}", use_container_width=True):
                            database.delete_note(note["id"])
                            st.rerun()
            if st.session_state.get(f"editing_note_{note['id']}", False):
                st.divider()
                st.subheader("✏️ Edit your note")
                with st.form(f"edit_form_{note['id']}"):
                    edited_title = st.text_input("Note title", value=note["title"] or "")
                    edited_subject = st.text_input("Subject", value=note["subject"] or "")
                    edited_content = st.text_area("Your notes", value=note["content"] or "", height=200)
                    save_col, cancel_col = st.columns(2)
                    with save_col:
                        save_changes = st.form_submit_button("💾 Save Changes", use_container_width=True)
                    with cancel_col:
                        cancel_edit = st.form_submit_button("Cancel", use_container_width=True)
                    if save_changes:
                        if edited_title.strip() and edited_content.strip():
                            database.update_note(
                                note["id"],
                                edited_title.strip(),
                                edited_subject.strip(),
                                edited_content.strip()
                            )
                            st.session_state[f"editing_note_{note['id']}"] = False
                            st.success("Note updated successfully!")
                            st.rerun()
                        else:
                            st.error("Title and content are required.")
                    if cancel_edit:
                        st.session_state[f"editing_note_{note['id']}"] = False
                        st.rerun()
            else:
                st.info("No notes match your search or selected subject.")
        else:
            st.info("No notes match your search or selected subject.")
    else:
        st.info("Your learning library is empty. Create your first note!")
elif page == "Flashcards and Quizzes":
    st.header("🧠 Flashcards & Quizzes")
    st.caption("Test your knowledge and revise your lessons.")
    with st.expander("➕ Create a New Flashcard", expanded=True):
        with st.form("flashcard_form"):
            question = st.text_input("Question")
            answer = st.text_area("Answer")
            subject = st.text_input("Subject")
            submitted = st.form_submit_button("💾 Save Flashcard", use_container_width=True)
            if submitted:
                if question.strip() and answer.strip():
                    database.add_flashcard(
                        question.strip(),
                        answer.strip(),
                        subject.strip()
                    )
                    st.success("Flashcard saved successfully!")
                    st.rerun()
                else:
                    st.warning("Enter both a question and an answer.")
    st.divider()
    cards = database.get_flashcards()
    st.subheader("📚 Your Flashcard Library")
    st.metric("Total Flashcards", len(cards))
    if cards:
        search_query = st.text_input("🔎 Search Flashcards", placeholder="Search by question, answer, or subject...")
        subjects = sorted({card["subject"].strip() for card in cards if card["subject"] and card["subject"].strip()})
        selected_subject = st.selectbox("📂 Filter by Subject", ["All Subjects"] + subjects)
        filtered_cards = cards
        if search_query.strip():
            query = search_query.strip().casefold()
            filtered_cards = [
                card for card in filtered_cards
                if query in (card["question"] or "").casefold()
                or query in (card["answer"] or "").casefold()
                or query in (card["subject"] or "").casefold()
            ]
        if selected_subject != "All Subjects":
            filtered_cards = [card for card in filtered_cards if (card["subject"] or "").strip() == selected_subject]
        st.caption(f"Showing {len(filtered_cards)} flashcard(s)")
        if filtered_cards:
            for index, card in enumerate(filtered_cards, start=1):
                with st.container(border=True):
                    st.caption(f"FLASHCARD {index}")
                    st.markdown(f"### ❓ {card['question']}")
                    st.caption(f"📚 Subject: {card['subject'] or 'Not specified'}")
                    with st.expander("💡 Reveal Answer"):
                        st.write(card["answer"])
                    if st.button("🗑️ Delete Flashcard", key=f"delete_card_{card['id']}"):
                        database.delete_flashcard(card["id"])
                        st.rerun()
        else:
            st.info("No flashcards match your search or selected subject.")
    else:
        st.info("No flashcards yet. Create your first one!")
elif page == "Study Assistant":
    st.header("🤖 Smart Study Assistant")
    st.caption("Turn your lessons into useful revision material.")
    lesson = st.text_area("📚 Paste your lesson here", height=250, placeholder="Paste your course notes or lesson...")
    if lesson.strip():
        words = lesson.split()
        sentences = [
            sentence.strip()
            for sentence in lesson.replace("!", ".").replace("?", ".").split(".")
            if sentence.strip()
        ]
        col1, col2, col3 = st.columns(3)
        col1.metric("Words", len(words))
        col2.metric("Sentences", len(sentences))
        col3.metric("Characters", len(lesson))
    action = st.radio("What would you like to do?", ["Summarize lesson", "Extract key terms", "Generate revision questions"])
    if st.button("✨ Generate", key="study_assistant_generate"):
        if not lesson.strip():
            st.warning("Please paste your lesson first.")
        elif action == "Summarize lesson":
            st.subheader("📝 Lesson Summary")
            paragraphs = [
                part.strip()
                for part in lesson.split("\n")
                if part.strip()
            ]
            for paragraph in paragraphs[:8]:
                preview = paragraph.split()
                if len(preview) > 50:
                    paragraph = " ".join(preview[:50]) + "..."
                st.markdown(f"- {paragraph}")
            st.caption("Basic text extraction, not an AI-generated summary.")
        elif action == "Extract key terms":
            st.subheader("🔑 Key Terms")
            stop_words = {
                "the", "and", "for", "with", "that", "this",
                "from", "are", "was", "were", "les", "des",
                "une", "dans", "pour", "avec", "est", "sont",
                "que", "qui", "sur", "par", "aux", "du"
            }
            import re
            from collections import Counter
            tokens = re.findall(r"\b[a-zA-ZÀ-ÿ]{4,}\b", lesson.lower())
            keywords = [word for word, count in Counter(tokens).most_common(10) if word not in stop_words]
            if keywords:
                for word in keywords:
                    st.markdown(f"- *{word}*")
            else:
                st.info("No key terms found.")
            st.caption("Keywords are selected by frequency, not semantic AI analysis.")
        else:
            st.subheader("❓ Revision Questions")
            questions = [
                sentence.strip()
                for sentence in lesson.replace("!", ".").replace("?", ".").split(".")
                if len(sentence.strip().split()) >= 4
            ]
            if questions:
                for number, sentence in enumerate(questions[:10], start=1):
                    with st.container(border=True):
                        st.markdown(f"*Question {number}*")
                        st.write(f"Explain this idea in your own words: {sentence}")
            else:
                st.info("Add a longer lesson containing complete sentences.")
elif page == "Quiz History":
    st.header("📊 Quiz History")
    st.caption("Track your quiz performance and monitor your progress.")
    results = database.get_quiz_results()
    if not results:
        st.info("No quiz results yet. Complete your first quiz to see your progress.")
    else:
        total_attempts = len(results)
        latest = results[0]
        latest_percentage = float(latest["percentage"])
        average_percentage = sum(float(result["percentage"]) for result in results) / total_attempts
        best_percentage = max(float(result["percentage"]) for result in results)
        st.subheader("📈 Performance Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Attempts", total_attempts)
        col2.metric("Average Score", f"{average_percentage:.1f}%")
        col3.metric("Best Score", f"{best_percentage:.1f}%")
        st.divider()
        st.subheader("📉 Your Progress")
        chart_data = [{"Attempt": f"Quiz {index}", "Percentage": float(result["percentage"])} for index, result in enumerate(reversed(results), start=1)]
        st.line_chart(chart_data, x="Attempt", y="Percentage")
        st.divider()
        st.subheader("🎯 Smart Study Recommendations")
        st.write(f"Your latest quiz score is *{latest_percentage:.1f}%*.")
        if latest_percentage < 50:
            st.warning("Focus on reviewing your notes and flashcards. " "Take your time to understand the difficult concepts.")
        elif latest_percentage < 80:
            st.info("Good progress! Review the questions you found difficult " "and practise with more flashcards.")
        else:
            st.success("Excellent progress! Keep practising to maintain your results.")
        st.divider()
        st.subheader("📚 Previous Quiz Attempts")
        for index, result in enumerate(results, start=1):
            percentage = float(result["percentage"])
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"*Quiz Attempt #{index}*")
                    st.caption(f"Date: {result['created_at']}")
                with col2:
                    st.metric("Score", f"{percentage:.1f}%")
                st.write(f"Correct answers: {result['score']} / {result['total']}")
                st.progress(max(0.0, min(1.0, percentage / 100)))
elif page == "Study Goals":
    st.title("🎯 My Study Goals")
    st.caption("Build consistent study habits and track your weekly progress.")
    saved_goal = database.get_study_goal()
    if saved_goal is None:
        default_goal = 10.0
        default_hours = 0.0
    else:
        default_goal = float(saved_goal["weekly_goal"])
        default_hours = float(saved_goal["hours_studied"])
    st.subheader("⚙️ Set Your Weekly Target")
    with st.form("study_goals_form"):
        col1, col2 = st.columns(2)
        with col1:
            weekly_goal = st.number_input(
                "Weekly study goal (hours)",
                min_value=1.0,
                max_value=168.0,
                value=min(168.0, max(1.0, default_goal)),
                step=1.0
            )
        with col2:
            hours_studied = st.number_input(
                "Hours studied this week",
                min_value=0.0,
                max_value=168.0,
                value=min(168.0, max(0.0, default_hours)),
                step=0.5
            )
        submitted = st.form_submit_button("💾 Save my goal", use_container_width=True)
    if submitted:
        database.save_study_goal(weekly_goal, hours_studied)
        st.success("Your study goal has been saved!")
        st.rerun()
    progress = min(hours_studied / weekly_goal, 1.0)
    remaining = max(0.0, weekly_goal - hours_studied)
    st.divider()
    st.subheader("📊 Weekly Progress")
    col1, col2, col3 = st.columns(3)
    col1.metric("Weekly Target", f"{weekly_goal:g} hrs")
    col2.metric("Studied", f"{hours_studied:g} hrs")
    col3.metric("Remaining", f"{remaining:g} hrs")
    st.progress(progress)
    st.markdown(f"*{progress * 100:.1f}% completed*")
    if hours_studied >= weekly_goal:
        st.success("🎉 Congratulations! You achieved your weekly study goal!")
    elif progress >= 0.5:
        st.info("👏 You're more than halfway there. Keep going!")
    else:
        st.write("🌱 Every study session counts. Keep building your progress!")
    st.divider()
    st.subheader("💡 Study Tip")
    if remaining > 0:
        st.write(f"You have {remaining:g} hours remaining to reach your weekly target. " "Try dividing them into shorter, manageable study sessions.")
    else:
        st.write("You reached your target! Keep a balanced schedule " "and maintain your learning habits.")
else:
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_finished = False
    if st.button("🔄 Start a new quiz"):
        cards = database.get_flashcards()
        if not cards:
            st.warning("Add at least one flashcard first")
        else:
            st.session_state.quiz_questions = random.sample(list(cards), len(cards))
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_finished = False
        st.session_state.quiz_result_saved = False
        st.rerun()
    if not st.session_state.quiz_questions:
        st.info("Click 'Start a new quiz' to begin.")
    elif st.session_state.quiz_finished:
        total = len(st.session_state.quiz_questions)
        score = st.session_state.quiz_score
        percentage = round(score / total * 100)if total > 0 else 0
        if not st.session_state.get("quiz_result_saved", False):
            database.save_quiz_result(score, total)
            st.session_state_quiz_result_saved = True
        st.success("Quiz completed!")
        st.metric("Final score", f"{score}/{total}")
        st.progress(percentage / 100)
        st.write(f"Your result:{percentage}%")
    else:
        index = st.session_state.quiz_index
        total = len(st.session_state.quiz_questions)
        card = st.session_state.quiz_questions[index]
        st.write(f"Question {index + 1} of {total}")
        st.progress((index + 1) / total)
        st.subheader(card["question"])
        with st.form(f"answer_form_{index}"):
            answer = st.text_area("Your answer")
            submitted = st.form_submit_button("Check answer")
        if submitted:
            if not answer.strip():
                st.warning("Please write your answer first.")
            else:
                correct = (
                    answer.strip().casefold()
                    == card["answer"].strip().casefold()
                )
                if correct:
                    st.session_state.quiz_score += 1
                    st.success("✅ Correct!")
                else:
                    st.error("❌ Incorrect!")
                st.info(f"Correct answer: {card['answer']}")
                st.session_state[f"answered_{index}"] = True
        if st.session_state.get(f"answered_{index}", False):
            if index + 1 < total:
                if st.button("➡️ Next question"):
                    st.session_state.quiz_index += 1
                    st.rerun()
            else:
                if st.button("🏁 Finish quiz"):
                    st.session_state.quiz_finished = True
                    st.rerun()
st.divider()
st.caption("StudyBuddy AI | Personal Learning Project")
if "GEMINI_API_KEY" in st.secrets:
    st.success("GEMINI API configuration detected!")
else:
    st.error("GEMINI API cofiguration not found.")