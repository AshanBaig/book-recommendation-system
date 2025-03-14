import streamlit as st
import pickle
import numpy as np
import pandas as pd
data=pickle.load(open("popular.pkl","rb"))
similarity=pickle.load(open("similarity.pkl","rb"))
pt=pickle.load(open("pt.pkl","rb"))
books=pickle.load(open("books.pkl","rb"))


st.set_page_config(page_title="Multi-Page App")
# Create a navigation system
page = st.sidebar.radio("Navigation", ["Home","Recommendation"])

def home_page():
    #display all 50 iamges
    ind=0
    pic_per_row=4
    for i in range(0, len(data),pic_per_row):
        cols = st.columns(pic_per_row)
        for j in range(pic_per_row):
            if ind<len(data):
                try:
                    cols[j].image(data["Image-URL-M"][ind], use_container_width=True)
                except:
                    pass
                cols[j].markdown(f"""
                    **Title:** {data["Book-Title"][ind]}  
                    **Author:** {data["Book-Author"][ind]}  
                    **Total Votes:** {data["rating_in_num"][ind]}  
                    **Avg Rating:** {data["mean_rating"][ind]:.2f}  
                """)

                ind+=1
            else:
                break


def  recommend(book_name):
  suggestion=[]
  ind=np.where(pt.index==book_name)[0][0]
  similar_items=sorted(list(enumerate(similarity[ind])),reverse=True,key=lambda x: x[1])[1:9]
  for i in similar_items:
    ind=i[0]
    temp_df=books[books["Book-Title"]==pt.index[ind]]
    suggestion.append(temp_df.drop_duplicates("Book-Title").reset_index(drop=True))
  ind = 0
  pic_per_row = 4
  for i in range(0, len(suggestion), pic_per_row):
        cols = st.columns(pic_per_row)
        for j in range(pic_per_row):
            if ind<len(suggestion):
                try:
                    cols[j].image(suggestion[ind]["Image-URL-M"][0], use_container_width=True)
                except:
                    pass
                cols[j].markdown(f"""
                    **Title:** {suggestion[ind]["Book-Title"][0]}
                    **Author:** {suggestion[ind]["Book-Author"][0]}
                   """)
                ind+=1
            else:
                break


  return suggestion





if page == "Home":
    st.title("Top 50 Books")
    home_page()


elif page == "Recommendation":
    st.title("Recommended Book")
    options = st.selectbox("Select a Book", set(pt.index))
    recommend(options)
