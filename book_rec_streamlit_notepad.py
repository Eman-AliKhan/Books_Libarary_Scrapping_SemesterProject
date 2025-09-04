import streamlit as st
import pandas as pd
import numpy as np
########################
import matplotlib.pyplot as plt
import seaborn as sns
import os


pd.set_option('display.max_rows', None)

df_fiction = pd.read_csv('1000 fiction books.csv')
df_autobio = pd.read_csv('1000 autobio books.csv')
df_history = pd.read_csv('1000 history books.csv')
df_children = pd.read_csv('1000_children books.csv')

df_all_books = pd.concat([df_children, df_fiction, df_autobio, df_history], ignore_index=True)

convert_to_int = ['Number of People Who Want to Read', 'First Published Year', 'Number of Ratings', 'Number of Editions', 'Number of Pages']
for df in [df_all_books, df_fiction, df_autobio, df_history, df_children]:
    for column in convert_to_int:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors='coerce').astype('Int64')

def add_bg_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({image_url});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_image("https://img.freepik.com/premium-photo/study-reading-room-design-home_924723-930.jpg") 

main_image_url = "https://miro.medium.com/v2/resize:fit:1400/1*6Jp3vJWe7VFlFHZ9WhSJng.jpeg"
st.image(main_image_url)
st.title("Book Management System")

genre_options = {
    "All Books": df_all_books,
    "Fiction": df_fiction,
    "Autobiography": df_autobio,
    "History": df_history,
    "Children": df_children,
}
genre_images = {
    "All Books": "https://pics.craiyon.com/2023-11-12/MmhZmm4RTA6VvrafkKTgnQ.webp",
    "Fiction": "https://www.creativefabrica.com/wp-content/uploads/2023/02/24/Fantasy-Castle-In-The-Sky-Graphic-62281124-1.png",
    "Autobiography": "https://t3.ftcdn.net/jpg/00/61/52/46/360_F_61524655_Yk7kNJfGI0xcmZIYkyyMGOItCjtb8t9X.jpg",
    "History": "https://i.pinimg.com/originals/fd/56/67/fd56675dbc66213f622abd4343c18c18.jpg",
    "Children": "https://thumbs.dreamstime.com/b/hand-drawn-cartoon-kids-playing-ai-generated-simple-playful-look-happy-joyful-children-324142751.jpg",
}
selected_genre = st.sidebar.selectbox("Choose a Genre", list(genre_options.keys()), index=0)
selected_df = genre_options[selected_genre]
selected_image = genre_images.get(selected_genre, None)

if selected_image:
    st.sidebar.image(selected_image)

def find_specific_books(df):
    st.subheader("Find Specific Books")
    search_option = st.selectbox(
        "Find Specific Books by",
        ["Title", "Author", "Publisher", "Subjects", "Language", "First Published Year"]
    )
    search_term = st.text_input(f"Enter the {search_option}:")
    
    if search_term:
        if search_option == "Title":
            filtered_df = df[df['Title'].fillna('').str.contains(search_term, case=False, na=False)]
        elif search_option == "Author":
            filtered_df = df[df['Authors'].fillna('').str.contains(search_term, case=False, na=False)]
        elif search_option == "Publisher":
            filtered_df = df[df['Publishers'].fillna('').str.contains(search_term, case=False, na=False)]
        elif search_option == "Subjects":
            filtered_df = df[df['Subjects'].fillna('').str.contains(search_term, case=False, na=False)]
        elif search_option == "Language":
            filtered_df = df[df['Languages'].fillna('').str.contains(search_term, case=False, na=False)]
        elif search_option == "First Published Year":
            filtered_df = df[df['First Published Year'].fillna('').astype(str).str.contains(search_term, case=False, na=False)]
        
        st.dataframe(filtered_df)

def sort_books(df):
    st.subheader("Sort Books")
    sort_options = [
        "Alphabetically by Author",
        "Number of Ratings",
        "Rating",
        "Publishing Year",
        "Number of Pages",
        "Number of People Who Want to Read",
    ]
    sort_choice = st.selectbox("Sort Books by", sort_options)
    ascending = st.radio("Order", ["Ascending", "Descending"]) == "Ascending"

    if sort_choice == "Alphabetically by Author":
        sorted_df = df.sort_values(by="Authors", ascending=ascending, ignore_index=True)
    elif sort_choice == "Number of Ratings":
        sorted_df = df.sort_values(by="Number of Ratings", ascending=ascending, ignore_index=True)
    elif sort_choice == "Rating":
        sorted_df = df.sort_values(by="Ratings", ascending=ascending, ignore_index=True)
    elif sort_choice == "Publishing Year":
        sorted_df = df.sort_values(by="First Published Year", ascending=ascending, ignore_index=True)
    elif sort_choice == "Number of Pages":
        sorted_df = df.sort_values(by="Number of Pages", ascending=ascending, ignore_index=True)
    elif sort_choice == "Number of People Who Want to Read":
        sorted_df = df.sort_values(by="Number of People Who Want to Read", ascending=ascending, ignore_index=True)

    st.dataframe(sorted_df)

def advanced_search(df):
    st.subheader("Advanced Search Options")
    options = [
        "Books with specific range of pages",
        "Books with specific range of ratings",
        "Greatest or least rating",
        "Greatest or least pages",
        "Oldest or newest book",
        "Books with pages/rating/year/people greater or smaller than a specific value",
        "Books published within a specific range of years",
    ]
    choice = st.selectbox("Choose an Advanced Search Option", options)

    if choice == "Books with specific range of pages":
        min_pages = st.number_input("Minimum pages", min_value=0, step=1)
        max_pages = st.number_input("Maximum pages", min_value=0, step=1)
        st.dataframe(df[(df['Number of Pages'] >= min_pages) & (df['Number of Pages'] <= max_pages)])
    elif choice == "Books with specific range of ratings":
        min_rating = st.number_input("Minimum rating", min_value=0.0, max_value=5.0, step=0.1)
        max_rating = st.number_input("Maximum rating", min_value=0.0, max_value=5.0, step=0.1)
        st.dataframe(df[(df['Ratings'] >= min_rating) & (df['Ratings'] <= max_rating)])
    elif choice == "Greatest or least rating":
        st.write("Book with the highest rating:")
        st.write(df.loc[df['Ratings'].idxmax()])
        st.write("Book with the lowest rating:")
        st.write(df.loc[df['Ratings'].idxmin()])
    elif choice == "Greatest or least pages":
        st.write("Book with the most pages:")
        st.write(df.loc[df['Number of Pages'].idxmax()])
        st.write("Book with the least pages:")
        st.write(df.loc[df['Number of Pages'].idxmin()])
    elif choice == "Oldest or newest book":
        st.write("Oldest book:")
        st.write(df.loc[df['First Published Year'].idxmin()])
        st.write("Newest book:")
        st.write(df.loc[df['First Published Year'].idxmax()])
    ##########################################
    elif choice == "Books with pages/rating/year/people greater or smaller than a specific value":
        attr_options = ["Number of Pages", "Ratings", "First Published Year", "Number of People Who Want to Read"]
        attr_choice = st.selectbox("Choose Attribute for Filtering", attr_options)

        start_point = st.number_input(f"Enter the starting value for {attr_choice}", min_value=0.0, step=0.1)
        direction = st.radio("Choose filter direction:", ["Greater than", "Less than"])

        if attr_choice == "Number of Pages":
            if direction == "Greater than":
                st.dataframe(df[df['Number of Pages'] > start_point])
            else:
                st.dataframe(df[df['Number of Pages'] < start_point])

        elif attr_choice == "Ratings":
            if direction == "Greater than":
                st.dataframe(df[df['Ratings'] > start_point])
            else:
                st.dataframe(df[df['Ratings'] < start_point])

        elif attr_choice == "First Published Year":
            if direction == "Greater than":
                st.dataframe(df[df['First Published Year'] > start_point])
            else:
                st.dataframe(df[df['First Published Year'] < start_point])

        elif attr_choice == "Number of People Who Want to Read":
            if direction == "Greater than":
                st.dataframe(df[df['Number of People Who Want to Read'] > start_point])
            else:
                st.dataframe(df[df['Number of People Who Want to Read'] < start_point])
    elif choice == "Books published within a specific range of years":
        min_year = st.number_input("Minimum year", min_value=0, step=1)
        max_year = st.number_input("Maximum year", min_value=0, step=1)
        st.dataframe(df[(df['First Published Year'] >= min_year) & (df['First Published Year'] <= max_year)])

def plot_graphs(df):
    st.subheader("Graphs and Charts")
    graph_options = [
        "Distribution of Books by Language Categories",
        "Count of Books by Subject",
        "Number of Books per Author",
        "Distribution of Book Ratings",
        "Number of Pages vs Ratings",
        "Box Plot: Number of Ratings",
    ]
    selected_graph = st.selectbox("Choose a Graph to View", graph_options)

    if selected_graph == "Distribution of Books by Language Categories":
        count_english_only = len(df[df['Languages'].fillna('').str.contains('eng', case=False)])
        count_other_languages = len(df[~df['Languages'].fillna('').str.contains('Eng', case=False)])
        count_both = len(df[df['Languages'].fillna('').str.contains('English.*', case=False)])
        labels = ['Only English', 'Others', 'Both']
        sizes = [count_english_only, count_other_languages, count_both]
        colors = ['lightblue', 'lightgreen', 'gold']
        plt.figure(figsize=(10, 5))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
        plt.title('Distribution of Books by Language Categories')
        st.pyplot(plt)

    elif selected_graph == "Count of Books by Subject":
        subject_counts = {
            'youth': 0,
            'Family': 0,
            'general': 0,
            'women': 0,
            'biography': 0
        }
        for _, row in df.iterrows():
            subjects = str(row.get("Subjects", "")).lower()
            for subject in subject_counts:
                if subject.lower() in subjects:
                    subject_counts[subject] += 1
        subjects = list(subject_counts.keys())
        counts = list(subject_counts.values())
        plt.figure(figsize=(10, 6))
        plt.bar(subjects, counts, color=['skyblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightpink'])
        plt.title('Count of Books by Subject')
        plt.xlabel('Subjects')
        plt.ylabel('Number of Books')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(plt)

    elif selected_graph == "Number of Books per Author":
        author_count = df['Authors'].value_counts()
        plt.figure(figsize=(10, 6))
        author_count.head(20).plot(kind='bar', color='skyblue')
        plt.title('Number of Books per Author')
        plt.xlabel('Author')
        plt.ylabel('Number of Books')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(plt)

    elif selected_graph == "Distribution of Book Ratings":
        df['Ratings'] = pd.to_numeric(df['Ratings'], errors='coerce')
        df_cleaned = df.dropna(subset=['Ratings'])
        plt.figure(figsize=(10, 6))
        plt.hist(df_cleaned['Ratings'], bins=20, color='skyblue', edgecolor='black')
        plt.title('Distribution of Book Ratings')
        plt.xlabel('Ratings')
        plt.ylabel('Number of Books')
        plt.grid(True, alpha=0.75)
        plt.tight_layout()
        st.pyplot(plt)

    elif selected_graph == "Number of Pages vs Ratings":
        df['Ratings'] = pd.to_numeric(df['Ratings'], errors='coerce')
        df['Number of Pages'] = pd.to_numeric(df['Number of Pages'], errors='coerce')
        df_cleaned = df.dropna(subset=['Ratings', 'Number of Pages'])
        plt.figure(figsize=(10, 6))
        plt.scatter(df_cleaned['Number of Pages'], df_cleaned['Ratings'], color='skyblue', edgecolors='black', alpha=0.7)
        plt.title('Scatter Plot: Number of Pages vs. Ratings')
        plt.xlabel('Number of Pages')
        plt.ylabel('Ratings')
        plt.grid(True, alpha=0.5)
        plt.tight_layout()
        st.pyplot(plt)

    elif selected_graph == "Box Plot: Number of Ratings":
        df['Ratings'] = pd.to_numeric(df['Ratings'], errors='coerce')
        df_cleaned = df.dropna(subset=['Ratings'])
        plt.figure(figsize=(12, 8))
        sns.boxplot(data=df_cleaned, x='Number of Ratings', y='Ratings', palette='Set2')
        plt.title('Box Plot: Number of Ratings', fontsize=16)
        plt.xlabel('Authors', fontsize=12)
        plt.ylabel('Number of Ratings', fontsize=12)
        plt.xticks(rotation=90)
        plt.tight_layout()
        st.pyplot(plt)

def images(df):
    st.subheader("Book Cover Images")
    
    genre_folders = {
        "All Books": "D:/FAST_NUCES/3rd_Semester/Programming_for_AI/AI_Semester_Project/correct_datasets/Fatiqas_pics/All_books",  
        "Fiction": "D:/FAST_NUCES/3rd_Semester/Programming_for_AI/AI_Semester_Project/correct_datasets/Fatiqas_pics/Fiction", 
        "Autobiography": "D:/FAST_NUCES/3rd_Semester/Programming_for_AI/AI_Semester_Project/correct_datasets/Fatiqas_pics/Autobio", 
        "History": "D:/FAST_NUCES/3rd_Semester/Programming_for_AI/AI_Semester_Project/correct_datasets/Fatiqas_pics/history", 
        "Children": "D:/FAST_NUCES/3rd_Semester/Programming_for_AI/AI_Semester_Project/correct_datasets/Fatiqas_pics/children_books" 
    }

    selected_genre = st.selectbox("Select Genre", ["All Books", "Fiction", "Autobiography", "History", "Children"])

    image_folder = genre_folders.get(selected_genre)
        
    if image_folder and os.path.exists(image_folder):
        image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
        for image_file in image_files:
            full_img_path = os.path.join(image_folder, image_file)
                
                
            st.image(full_img_path)  
    else:
        st.warning(f"The folder does not exist: {image_folder}")


tab1, tab2, tab3, tab4, tab5 = st.tabs(["Find Specific Books", "Sort Books", "Advanced Search", "Graphs and Charts", "Book Cover Images"])

with tab1:
    find_specific_books(selected_df)

with tab2:
    sort_books(selected_df)

with tab3:
    advanced_search(selected_df)

with tab4:
    plot_graphs(selected_df)

with tab5:
    images(selected_df)

