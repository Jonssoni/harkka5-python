import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
url = "https://gist.githubusercontent.com/Jonssoni/2b2416c850b9f71f79ec91c897805515/raw/924b20991896b1e31c00186831d22ed3f6c8160d/gistfile1.txt"
df = pd.read_csv(url)

# Streamlit Page Config
st.set_page_config(page_title="Titanic Dashboard", page_icon="🚢", layout="wide")

# Title & Subtitle
st.title("🚢 Titanic Data Dashboard")
st.markdown("Explore insights from the Titanic dataset with interactive visualizations.")

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")
sex_filter = st.sidebar.radio("Filter by Gender", ["All", "Male", "Female"])
pclass_filter = st.sidebar.multiselect("Select Passenger Class", [1, 2, 3], default=[1, 2, 3])

# Apply filters
filtered_df = df[df["Pclass"].isin(pclass_filter)]
if sex_filter != "All":
    filtered_df = filtered_df[filtered_df["Sex"] == sex_filter.lower()]

# Layout: Key Figures in Columns
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Passengers", filtered_df.shape[0])
col2.metric("Survival Rate", f"{filtered_df['Survived'].mean() * 100:.2f}%")
col3.metric("Avg Fare ($)", f"{filtered_df['Fare'].mean():.2f}")
col4.metric("Avg Age", f"{filtered_df['Age'].mean():.1f}")

# --- Visualizations ---
st.subheader("📊 Survival Rate by Class")
survival_by_class = filtered_df.groupby("Pclass")["Survived"].mean() * 100

fig, ax = plt.subplots()
survival_by_class.plot(kind="bar", color=["blue", "orange", "green"], ax=ax)
ax.set_ylabel("Survival Rate (%)")
ax.set_xlabel("Passenger Class")
ax.set_title("Survival Rate by Class")
st.pyplot(fig)

st.subheader("🎭 Gender Distribution")
gender_counts = filtered_df["Sex"].value_counts()
fig, ax = plt.subplots()
ax.pie(gender_counts, labels=gender_counts.index, autopct="%1.1f%%", colors=["lightblue", "pink"])
st.pyplot(fig)

# Correlation Heatmap
st.subheader("📈 Correlation Heatmap")
fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# Display Data
st.subheader("📋 Filtered Data Preview")
st.dataframe(filtered_df.head())

# Submit GitHub Gist link
st.text_input("📌 Submit your GitHub Gist link here:")
