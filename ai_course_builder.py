import streamlit as st
import json
from main_app import ai_course_builder

st.set_page_config(page_title="Incrify Ai Course builder",
                   page_icon="📚",
                   layout="wide")


api_key = st.secrets["api_key"]

# # Path to the JSON file
# json_file_path = r'ai_course.json'  # Replace with the actual path to your JSON file

# # Reading the JSON file
# with open(json_file_path, 'r') as file:
#     result = json.load(file)

# Streamlit app
def main():
      # External links
    st.sidebar.title("Our Other Projects")
    st.sidebar.markdown("<a href='https://incrify90.streamlit.app/' target='_blank'>Chat with PDF's</a>", unsafe_allow_html=True)
    st.sidebar.markdown("<a href='https://incrify-avi.streamlit.app/' target='_blank'>Audio Video Intelligence</a>", unsafe_allow_html=True)
    st.sidebar.markdown("<a href='https://incrify-ai-course-builder.streamlit.app/' target='_blank'>Ai Course Builder</a>", unsafe_allow_html=True)
  
    st.title("Ai Course builder")
    user_input = st.text_input("Enter your Topic Name on which you want to Generate the Course :")
    # Create a button and check if it is clicked
    if st.button('Generate Course'):
        # If the button is clicked, perform the desired action
        # For example, display the input back to the user
        if user_input:

            result = ai_course_builder(user_input, api_key)
            
            for i in range(len(result['M_T'])):
                st.markdown("---")
                st.header(f"Module {i + 1} : {result['M_T'][i]}")
                st.write(f"{result['module_c'][i]}")

                for j in range(len(result['SM_T'][i])):

                    st.subheader(f"SubModule {i+1}.{j + 1} : {result['SM_T'][i][j]}", divider=True)

                    st.write(f"{result['submodule_c'][i][j]}")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.subheader(f"SubModule {i+1}.{j + 1} : Usecases", divider=True)
                        st.write(f"{result['submodule_usecase'][i][j]}")

                    with col2:
                        st.subheader(f"SubModule {i+1}.{j + 1} : MCQ", divider=True)

                        text = result['submodule_mcq'][i][j]
                        lines = text.count('\n') + 1
                        average_line_height = 20
                        estimated_height = lines * average_line_height
                        min_height = 1250
                        height = max(estimated_height, min_height)
                        print(height)
                        # Generate a unique key for each text area
                        unique_key = f"text_area_mcq_{i}_{j}"

                        st.text_area(label="", value=text, height=height, disabled=False, key=unique_key)


                    with col3:
                        st.subheader(f"SubModule {i+1}.{j + 1} : Resouces", divider=True)

                        text = result['submodule_rflink'][i][j]
                        lines = text.count('\n') + 1
                        average_line_height = 20
                        estimated_height = lines * average_line_height
                        min_height = 1250
                        height = max(estimated_height, min_height)
                        print(height)
                        # Generate a unique key for each text area
                        unique_key = f"text_area_resources_{i}_{j}"

                        st.text_area(label="", value=text, height=height, disabled=False, key=unique_key)

        else:
            st.header("Enter your Topic Name on which you want to Generate the Course")




if __name__ == "__main__":
    main()
