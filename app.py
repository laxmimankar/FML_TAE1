import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import random

# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="LearnPath AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0b1020;
    color: #f8fafc;
}

[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #273449;
}

[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

h1, h2, h3, h4, p, label {
    color: #f8fafc !important;
}

.main-heading {
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 4px;
}

.sub-heading {
    color: #94a3b8 !important;
    font-size: 15px;
    margin-bottom: 25px;
}

.hero {
    background:
        radial-gradient(circle at 85% 15%, rgba(139, 92, 246, .45), transparent 30%),
        linear-gradient(135deg, #312e81, #4f46e5, #7c3aed);
    border-radius: 24px;
    padding: 34px;
    margin-bottom: 25px;
}

.hero-title {
    font-size: 30px;
    font-weight: 800;
    color: white !important;
}

.hero-text {
    color: #ddd6fe !important;
    font-size: 15px;
    line-height: 1.7;
}

.badge {
    display: inline-block;
    background: rgba(255,255,255,.15);
    color: white;
    padding: 7px 13px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 15px;
}

.metric-card,
.course-card,
.roadmap,
.info-panel {
    background: #151d31;
    border: 1px solid #273449;
    border-radius: 18px;
    padding: 22px;
}

.metric-card {
    min-height: 135px;
}

.metric-label {
    color: #94a3b8 !important;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .7px;
}

.metric-value {
    color: #ffffff !important;
    font-size: 25px;
    font-weight: 800;
    margin-top: 12px;
}

.section-title {
    color: white !important;
    font-size: 23px;
    font-weight: 800;
    margin-top: 32px;
    margin-bottom: 16px;
}

.course-card {
    min-height: 175px;
}

.course-icon {
    font-size: 30px;
    margin-bottom: 12px;
}

.course-title {
    color: white !important;
    font-size: 17px;
    font-weight: 700;
}

.course-description {
    color: #94a3b8 !important;
    font-size: 13px;
    line-height: 1.6;
    margin-top: 8px;
}

.step-number {
    color: #a78bfa !important;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
}

.step-title {
    color: white !important;
    font-size: 17px;
    font-weight: 700;
    margin-top: 6px;
}

.step-description {
    color: #94a3b8 !important;
    font-size: 13px;
    margin-top: 5px;
}

.info-panel h4 {
    color: #c4b5fd !important;
}

.info-panel p {
    color: #cbd5e1 !important;
    line-height: 1.7;
    font-size: 14px;
}

.stButton > button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    padding: 12px;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #818cf8, #a78bfa);
}

.footer {
    text-align: center;
    color: #64748b !important;
    font-size: 12px;
    margin-top: 45px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# DATASET LOAD
# =====================================================

DATASET_NAME = "learning_path_dataset.csv"
dataset_path = Path(DATASET_NAME)

dataset = None
dataset_error = None

if dataset_path.exists():
    try:
        dataset = pd.read_csv(dataset_path)
    except Exception as error:
        dataset_error = str(error)

# =====================================================
# SESSION STATE
# =====================================================

if "q_table" not in st.session_state:
    st.session_state.q_table = {}

if "recommended_path" not in st.session_state:
    st.session_state.recommended_path = []

if "progress" not in st.session_state:
    st.session_state.progress = 0

if "reward" not in st.session_state:
    st.session_state.reward = 0

# =====================================================
# LEARNING CONTENT
# =====================================================

LEARNING_PATHS = {
    "Python Programming": [
        ("Python Basics", "Learn syntax, variables and data types."),
        ("Conditions and Loops", "Understand decisions, loops and repetition."),
        ("Functions", "Create reusable and organized programs."),
        ("Object-Oriented Programming", "Learn classes, objects and inheritance."),
        ("Python Project", "Build a practical mini project.")
    ],

    "Data Science": [
        ("Python for Data Science", "Learn Python libraries for data analysis."),
        ("NumPy and Pandas", "Work with arrays, tables and datasets."),
        ("Data Cleaning", "Handle missing, duplicate and incorrect values."),
        ("Exploratory Data Analysis", "Discover patterns and relationships."),
        ("Data Visualization Project", "Create charts and present insights.")
    ],

    "Machine Learning": [
        ("Python and Mathematics", "Revise Python, statistics and mathematics."),
        ("Data Preprocessing", "Prepare clean data for model training."),
        ("Supervised Learning", "Learn regression and classification."),
        ("Unsupervised Learning", "Learn clustering and pattern discovery."),
        ("Machine Learning Project", "Build and evaluate a machine learning model.")
    ],

    "Artificial Intelligence": [
        ("Python Fundamentals", "Build the programming foundation."),
        ("Mathematics for AI", "Study probability, statistics and vectors."),
        ("Machine Learning Basics", "Understand training and prediction."),
        ("Neural Networks", "Learn neurons, layers and activation functions."),
        ("Artificial Intelligence Project", "Apply AI to a real-world problem.")
    ],

    "Data Analytics": [
        ("Excel Fundamentals", "Learn formulas, sorting and filtering."),
        ("SQL Fundamentals", "Retrieve useful information from databases."),
        ("Python Analytics", "Analyze datasets using Python."),
        ("Power BI", "Create interactive dashboards."),
        ("Analytics Project", "Complete an end-to-end data analysis.")
    ],

    "Web Development": [
        ("HTML", "Create the structure of web pages."),
        ("CSS", "Design attractive and responsive interfaces."),
        ("JavaScript", "Add logic and interactivity."),
        ("Frontend Development", "Build interactive frontend applications."),
        ("Full Stack Project", "Create a complete web application.")
    ]
}

# =====================================================
# Q-LEARNING FUNCTIONS
# =====================================================

def get_state(skill_level, goal, style, progress):
    """
    State represents the learner's current condition.
    """
    return f"{skill_level}_{goal}_{style}_{progress}"


def initialize_q_values(state, actions):
    if state not in st.session_state.q_table:
        st.session_state.q_table[state] = {
            action: 0.0 for action in actions
        }


def choose_action(state, actions, epsilon=0.20):
    """
    Epsilon-greedy action selection.
    Exploration: choose random topic.
    Exploitation: choose topic with highest Q-value.
    """
    initialize_q_values(state, actions)

    if random.random() < epsilon:
        return random.choice(actions)

    q_values = st.session_state.q_table[state]
    return max(q_values, key=q_values.get)


def update_q_table(state, action, reward, next_state, next_actions,
                   alpha=0.7, gamma=0.8):
    """
    Q-learning update equation:

    Q(s,a) = Q(s,a) + alpha *
             [reward + gamma * max Q(next_state,next_action) - Q(s,a)]
    """
    initialize_q_values(state, [action])
    initialize_q_values(next_state, next_actions)

    current_q = st.session_state.q_table[state][action]
    next_max_q = max(st.session_state.q_table[next_state].values())

    new_q = current_q + alpha * (
        reward + gamma * next_max_q - current_q
    )

    st.session_state.q_table[state][action] = new_q


def generate_learning_path(skill_level, goal, style, daily_hours):
    topics = LEARNING_PATHS[goal]

    progress = st.session_state.progress
    state = get_state(skill_level, goal, style, progress)

    actions = [topic[0] for topic in topics]

    selected_topics = []
    remaining_actions = actions.copy()

    for _ in range(min(5, len(topics))):
        if not remaining_actions:
            break

        action = choose_action(
            state,
            remaining_actions,
            epsilon=0.15
        )

        selected_topics.append(
            next(topic for topic in topics if topic[0] == action)
        )

        remaining_actions.remove(action)

        next_progress = min(progress + 20, 100)
        next_state = get_state(
            skill_level,
            goal,
            style,
            next_progress
        )

        reward = 10

        if style == "Projects" and "Project" in action:
            reward += 5

        if daily_hours >= 4:
            reward += 2

        update_q_table(
            state,
            action,
            reward,
            next_state,
            remaining_actions if remaining_actions else actions
        )

        state = next_state
        progress = next_progress

    return selected_topics


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown("## 🎓 LearnPath AI")
    st.caption("AI-Powered Learning Assistant")

    st.markdown("---")
    st.markdown("### Student Preferences")

    student_name = st.text_input(
        "Student Name",
        value="Laxmi"
    )

    skill_level = st.selectbox(
        "Skill Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    learning_goal = st.selectbox(
        "Learning Goal",
        [
            "Python Programming",
            "Data Science",
            "Machine Learning",
            "Artificial Intelligence",
            "Data Analytics",
            "Web Development"
        ]
    )

    learning_style = st.selectbox(
        "Learning Style",
        ["Practice", "Videos", "Reading", "Projects"]
    )

    daily_hours = st.slider(
        "Daily Study Hours",
        min_value=1,
        max_value=8,
        value=2
    )

    st.markdown("---")

    generate_button = st.button(
        "✨ Generate Learning Path",
        use_container_width=True
    )

    reset_button = st.button(
        "🔄 Reset Progress",
        use_container_width=True
    )

    if reset_button:
        st.session_state.q_table = {}
        st.session_state.recommended_path = []
        st.session_state.progress = 0
        st.session_state.reward = 0
        st.rerun()

    st.markdown("---")
    st.caption("Q-Learning Based Recommendation System")

# =====================================================
# HEADER
# =====================================================

st.markdown(
    '<div class="main-heading">Learning Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-heading">Track your progress and discover your personalized learning journey.</div>',
    unsafe_allow_html=True
)

# =====================================================
# HERO
# =====================================================

st.markdown(f"""
<div class="hero">
    <div class="badge">SMART LEARNING • Q-LEARNING RECOMMENDATION</div>
    <div class="hero-title">Hello, {student_name}! 👋</div>
    <div class="hero-text">
        Your personalized learning path is generated using your skill level,
        learning goal, preferred learning style and available study time.
        The Q-Learning model improves recommendations using rewards.
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# METRICS
# =====================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">CURRENT LEVEL</div>
        <div class="metric-value">🎯 {skill_level}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">DAILY HOURS</div>
        <div class="metric-value">⏱️ {daily_hours} hrs</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">LEARNING GOAL</div>
        <div class="metric-value">📘 {learning_goal}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">PROGRESS</div>
        <div class="metric-value">📈 {st.session_state.progress}%</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# FEATURE CARDS
# =====================================================

st.markdown(
    '<div class="section-title">✨ Why LearnPath AI?</div>',
    unsafe_allow_html=True
)

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
    <div class="course-card">
        <div class="course-icon">🧠</div>
        <div class="course-title">Personalized Recommendations</div>
        <div class="course-description">
            Learning topics are selected according to student preferences,
            skill level and learning goal.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="course-card">
        <div class="course-icon">📈</div>
        <div class="course-title">Progress Tracking</div>
        <div class="course-description">
            Track your learning progress and update the recommendation model
            using feedback and rewards.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="course-card">
        <div class="course-icon">🤖</div>
        <div class="course-title">Actual Q-Learning</div>
        <div class="course-description">
            The system uses state, action, reward and Q-value updates
            to select suitable learning topics.
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# GENERATE RECOMMENDATION
# =====================================================

if generate_button:
    st.session_state.recommended_path = generate_learning_path(
        skill_level,
        learning_goal,
        learning_style,
        daily_hours
    )

    st.session_state.reward = len(
        st.session_state.recommended_path
    ) * 10

    st.success("Your personalized learning path has been generated using Q-Learning.")

# =====================================================
# RECOMMENDATION SECTION
# =====================================================

if st.session_state.recommended_path:

    st.markdown(
        '<div class="section-title">🧭 Your Recommended Learning Path</div>',
        unsafe_allow_html=True
    )

    st.write(
        f"Recommended roadmap for **{learning_goal}**:"
    )

    recommended_path = st.session_state.recommended_path
    total_topics = len(recommended_path)
    estimated_days = total_topics * 3

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric("Learning Topics", total_topics)

    with m2:
        st.metric("Estimated Days", estimated_days)

    with m3:
        st.metric("Current Reward", st.session_state.reward)

    st.markdown("### 📚 Roadmap Steps")

    for number, item in enumerate(recommended_path, start=1):
        topic, description = item

        st.markdown(f"""
        <div class="roadmap">
            <div class="step-number">STEP {number:02d}</div>
            <div class="step-title">{topic}</div>
            <div class="step-description">{description}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📊 Update Your Progress")

    new_progress = st.slider(
        "How much of your roadmap have you completed?",
        min_value=0,
        max_value=100,
        value=st.session_state.progress
    )

    if new_progress != st.session_state.progress:
        old_progress = st.session_state.progress
        st.session_state.progress = new_progress

        if new_progress > old_progress:
            st.session_state.reward += 10
            st.success("Progress increased. Positive reward added to the Q-Learning model.")

    st.progress(st.session_state.progress / 100)

    if st.session_state.progress == 0:
        st.info("Start your first topic to begin your learning journey.")
    elif st.session_state.progress < 50:
        st.info("Good start! Continue learning consistently.")
    elif st.session_state.progress < 100:
        st.success("Great progress! You are more than halfway there.")
    else:
        st.success("🎉 Congratulations! You completed your learning roadmap.")

    # =================================================
    # RL MODEL EXPLANATION
    # =================================================

    st.markdown("### 🤖 Reinforcement Learning Model")

    r1, r2, r3, r4 = st.columns(4)

    with r1:
        st.markdown("""
        <div class="info-panel">
            <h4>State</h4>
            <p>
                Skill level, learning goal, learning style and current progress.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with r2:
        st.markdown("""
        <div class="info-panel">
            <h4>Action</h4>
            <p>
                Selecting the next suitable learning topic.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with r3:
        st.markdown("""
        <div class="info-panel">
            <h4>Reward</h4>
            <p>
                Positive reward is provided when the learner completes a topic
                or makes progress.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with r4:
        st.markdown("""
        <div class="info-panel">
            <h4>Q-Value</h4>
            <p>
                Q-values are updated to improve future topic recommendations.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # =================================================
    # DOWNLOAD ROADMAP
    # =================================================

    result_df = pd.DataFrame({
        "Step": range(1, total_topics + 1),
        "Topic": [item[0] for item in recommended_path],
        "Description": [item[1] for item in recommended_path]
    })

    st.download_button(
        "⬇️ Download Learning Roadmap",
        data=result_df.to_csv(index=False),
        file_name="learning_roadmap.csv",
        mime="text/csv"
    )

else:
    st.markdown("""
    <div class="info-panel">
        <h4>Ready to start?</h4>
        <p>
            Select your preferences from the sidebar and click
            <b>Generate Learning Path</b> to create your personalized
            Q-Learning based roadmap.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# DATASET STATUS
# =====================================================

with st.expander("📂 Dataset Status"):
    if dataset is not None:
        st.success("Dataset loaded successfully from the project folder.")
        st.write("Rows:", dataset.shape[0])
        st.write("Columns:", dataset.shape[1])
        st.dataframe(dataset.head(10))
    elif dataset_error:
        st.error("Dataset found but could not be loaded.")
        st.write(dataset_error)
    else:
        st.info(
            "Dataset file was not found. The application is running with "
            "the built-in learning roadmap."
        )

# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="footer">
    LearnPath AI • Learning Path Recommendation using Reinforcement Learning
</div>
""", unsafe_allow_html=True)