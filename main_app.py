import os
import time
import requests
import json
from langchain_community.chat_models import ChatOpenAI

def ai_course_builder(topic, api_key):
    llm_course_generator = ChatOpenAI(openai_api_key=api_key)

    # Prompt 1 to get the structure of the course
    question = f"create a course on {topic}, which includes 5 modules and internal 2 submodules, just list the structure only and nothing extra, don't even create any 'Note:' at the end."
    op = llm_course_generator.invoke(question)

    # Module title (M_T) and submodule title (SM_T)
    M_T = []
    SM_T = []
    cont = op.content.split("\n")

    for M_name in cont:
        if "Module" in M_name:
            temp = []
            for SM in cont[cont.index(M_name) + 1:]:
                if SM == "" or "Module" in SM:
                    break
                submodule = SM.split(":")[-1].strip()
                if submodule:  # Exclude empty submodules
                    temp.append(submodule)
            M_T.append(M_name.split(":")[-1].strip())
            SM_T.append(temp)

##############################################################################################################
            
    # Prompt 2 to get modules context
    Data = []

    for module_name in M_T:
        
        
        module = f""" Ignore the previous information,
        Act as a technical content writer who has over 10 years of experience in generating training courses,
        so Generate a topic, information for `{module_name}` only, which will give the student a deeper insight on the topic.

        Make sure to generate the output with at least 300 words but also don't go too lengthyw, even if it is short but complete the statement at a full stop and
        context should not change.

        Note: Give the topic i.e. `{module_name}` specific information only, Do not create Modules or Submodules or sessions further
        just give me the raw content for the topic
        """
        Data.append((module_name, llm_course_generator.invoke(module)))
        time.sleep(20)

    module_c = []
    for i in range(len(Data)):
        module_c.append(Data[i][1].content)

 ##############################################################################################################   
    
    # prompt 3 to get submodules context

    sub_module_indept_intutions = []
    for i in range(len(SM_T)):
        temp = []
        for submodule_name in SM_T[i]:

            prompt_3 = f'''
    I'm looking to generate comprehensive content for educational purposes, specifically focusing on the submodule: '{submodule_name}'.

    1. *Why is a Fundamental Understanding of '{submodule_name}' Essential?*
    - Discuss the importance of grasping the fundamental concepts within '{submodule_name}'. Emphasize how these basics serve as a foundation for broader topics in the field, be it technology, management, or any relevant domain.

    2. *Exploring Core Concepts in '{submodule_name}'*
    - Break down the key principles and core concepts that make up the foundation of '{submodule_name}'. Highlight their significance and relevance in real-world scenarios across various domains.

    3. *Building Blocks of '{submodule_name}'*
    - Provide insights into the essential elements that constitute '{submodule_name}'. This could include basic terminology, key methodologies, or foundational techniques applicable in both technical and management contexts.

    4. *Application in Real-world Scenarios*
    - Illustrate the real-world applications of the fundamental concepts covered in '{submodule_name}'. Discuss how these basics play a crucial role in solving practical problems or contributing to industry practices, spanning technology, management, or any relevant area.

    Each section should be around 500 words. Even if concise, make sure the content is complete and ends with a full stop. Maintain consistency throughout and refrain from introducing additional submodules or sessions.

    Note1: Tailor the content to offer valuable insights into the fundamental aspects of '{submodule_name}', ensuring that it is meaningful and applicable across various subjects, including both technical and management scenarios.

    Note2: Focus on delivering substantial and informative content rather than a mere roadmap.
    '''


            temp.append((submodule_name, llm_course_generator.invoke(prompt_3)))
                # time.sleep(20)
        sub_module_indept_intutions.append(temp)

    submodule_c = []
    # Iterate through the modules in SM_T
    for i, module in enumerate(SM_T):

        temp = []

        # Iterate through the sub-modules in each module
        for j, sub_module_name in enumerate(module):
            # Fetch the content from sub_module_indept_intutions
            content = sub_module_indept_intutions[i][j][1].content
            temp.append(content)
        submodule_c.append(temp)

##############################################################################################################
    
    # prompt 4 to create usecases for submodules

    sub_module_example_usecases = []
    for i in range(len(SM_T)):
        temp = []
        for submodule_name in SM_T[i]:

            prompt_4 = f'''
    I'm seeking in-depth examples and real-world use cases for the submodule: '{submodule_name}'. Please focus on providing practical, relevant, and meaningful information. Avoid generating examples for submodules that lack practical significance.

    1. **Relevant Examples:**
    - Generate detailed and relevant examples showcasing the application of '{submodule_name}'. Ensure the examples are practical, and they help in understanding the real-world utility of this submodule.

    2. **Real-world Use Cases:**
    - Dive into real-world use cases where '{submodule_name}' plays a crucial role. Elaborate on scenarios, industries, or projects where the submodule is applied and brings value.

    Ensure the examples and use cases are meaningful, informative, and contribute to a better understanding of the '{submodule_name}' concept. Do not generate content for submodules that lack practical relevance or significance.

    Note: Provide comprehensive and insightful information without introducing examples for irrelevant submodules.
    '''


            temp.append((submodule_name, llm_course_generator.invoke(prompt_4)))
                # time.sleep(20)
        sub_module_example_usecases.append(temp)

    submodule_usecase = []
    # Iterate through the modules in SM_T
    for i, module in enumerate(SM_T):

        temp = []

        # Iterate through the sub-modules in each module
        for j, sub_module_name in enumerate(module):

            content = sub_module_example_usecases[i][j][1].content
            temp.append(content)
        submodule_usecase.append(temp)

##############################################################################################################
        
    # prompt 5 to create mcq on submodules

    sub_module_mcq = []
    for i in range(len(SM_T)):
        temp = []
        for submodule_name in SM_T[i]:

            prompt_5 = f'''
    I'm creating a set of Multiple Choice Questions (MCQs) for an educational course on '{submodule_name}'.

    For each question:
    1. Provide a detailed and informative question related to the concepts of '{submodule_name}'. But make sure the concept is meaningful enough to make a question upon,
    for example: topics like 'Overview of Machine Learning', here questions on machine learning is important, but Overview of Machine Learning will not mean anything the questions are not going to be usefull.
    another example: topic like 'Introduction to Python for Machine Learning', here questions on pthon for machine learning are important but,  Introduction to Python for Machine Learning is not a meaningful topic for any mcq on its own.
    2. Include 4 options for each question, ensuring that one option is correct.
    3. Aim for a mix of difficulty levels to test the depth of understanding.
    4. At the most generate only 5 questions from each concepts.
    format:
    1. the question.
    a. relevent option a
    b. relevent option b
    c. relevent option c
    d. relevent option d
    ans : the right answer.

    Note: Please ensure that the questions are educational, cover a range of possible misconceptions or nuances related to '{submodule_name}',
    and progress from easy to difficult. Avoid creating questions that are too straightforward or ambiguous.
    '''


            temp.append((submodule_name, llm_course_generator.invoke(prompt_5)))
                # time.sleep(20)
        sub_module_mcq.append(temp)

    submodule_mcq = []
    # Iterate through the modules in SM_T
    for i, module in enumerate(SM_T):

        temp = []

        # Iterate through the sub-modules in each module
        for j, sub_module_name in enumerate(module):
            # Fetch the content from sub_module_mcq
            content = sub_module_mcq[i][j][1].content
            temp.append(content)
        submodule_mcq.append(temp)

##############################################################################################################
        
    # prompt 6 to generate links 

    sub_module_references = []
    for i in range(len(SM_T)):
        temp = []
        for submodule_name in SM_T[i]:

            prompt_6 = f'''
    I'm curating a list of educational resources for the '{submodule_name}' module.
    The goal is to provide learners with high-quality references covering the meaningful concepts within the submodule. Please follow the guidelines below:

    1. Generate one YouTube link and one article link for each submodule concept.
    Ensure that the concepts are meaningful and aligned with the scope of educational content.

    2. Consider the relevance of the content - it should contribute to a comprehensive understanding of each concept. Avoid links that are too basic or advanced.

    3. Make sure that the resources are diverse and cater to different learning preferences.
    For instance, the YouTube link can be a tutorial, lecture, or presentation, while the article link can be a blog post, documentation, or an in-depth explanation.

    4. To enhance the reliability of YouTube links, please ensure that the generated link corresponds to a video with a substantial number of views (at least 10,000 views).

    Format:
    a. Concept 1:
        i. YouTube Link: [Insert YouTube Link]
        ii. Article Link: [Insert Article Link]

    b. Concept 2:
        i. YouTube Link: [Insert YouTube Link]
        ii. Article Link: [Insert Article Link]

    ... (Repeat for each concept)

    Note: Ensure the resource links are up-to-date, relevant, and provide valuable insights for learners studying '{submodule_name}'.
    '''


            temp.append((submodule_name, llm_course_generator.invoke(prompt_6)))
                # time.sleep(20)
        sub_module_references.append(temp)

    submodule_rflink = []

    # Iterate through the modules in SM_T
    for i, module in enumerate(SM_T):

        temp = []

        # Iterate through the sub-modules in each module
        for j, sub_module_name in enumerate(module):
            # Fetch the content from sub_module_references
            content = sub_module_references[i][j][1].content
            temp.append(content)
        submodule_rflink.append(temp)
    
    # creating json file of all the lists
    # Create a dictionary to store all the lists
    data_dict = {
        "M_T": M_T,
        "module_c": module_c,
        "SM_T": SM_T,
        "submodule_c": submodule_c,
        "submodule_usecase": submodule_usecase,
        "submodule_mcq": submodule_mcq,
        "submodule_rflink": submodule_rflink
    }

    return data_dict

# if __name__ == "__main__":
#     topic = input("Enter the topic: ")
#     result = ai_course_builder(topic)

#     # Specify the file path where you want to save the JSON file
#     file_path = os.getcwd()

#     # Save the data to a JSON file
#     with open(file_path, "w") as json_file:
#         json.dump(result, json_file, indent=2)

#     print(f'Data has been saved to {file_path}')
