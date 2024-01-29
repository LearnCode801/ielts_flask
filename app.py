from flask import Flask, request, jsonify
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage

app = Flask(__name__)

def eng_writing_test_PROMPT_of_IELTS(Question, Answer):
    instruction = [SystemMessage(
        content=f""" As an expert in IELTS (International English Language Testing System), your role is to 
         assess the writing proficiency of a user-entered answer, which is provided below:
         
         {Answer}
          
         You are required to examine the relevance of the answer to the given question, indicated as "{Question}" and "{Answer}" respectively.
         Evaluate the answer {Answer} based on the following aspects of the IELTS writing test:

         Task Achievement: Measure the relevance of the answer {Answer} to the question {Question}.
        
         Coherence and Cohesion: Assess the organization and logical flow of ideas in the response.
        
         Lexical Resource: Evaluate the richness and appropriateness of vocabulary used in the context.
        
         Grammatical Range and Accuracy: Examine the variety and correctness of grammatical structures in the answer.
        
         Total Score: Average of all above scores
         
         Your Output Should be the Just Python Dictionary that contains the key-value pair
         in keys their exist different aspects and their respective score in the values of the dictionary

         Remember: The All Results should be based OUT of 10 
        """)]

    return instruction

def setup_model(openai_api):
    eng_writing_test_MODEL_of_IELTS = ChatOpenAI(
        temperature=0.5,
        model_name="gpt-3.5-turbo",
        openai_api_key=openai_api,
        max_tokens=100
    )
    
    return eng_writing_test_MODEL_of_IELTS

def get_score(openai_api, question, answer):
    inst = eng_writing_test_PROMPT_of_IELTS(question, answer)
    eng_writing_test_MODEL_of_IELTS = setup_model(openai_api)
    response = eng_writing_test_MODEL_of_IELTS(inst)
    result = eval(response.content)
    return result

@app.route('/evaluate/', methods=['POST'])
def evaluate_answer():
    try:
        input_parameter = request.get_json()
        openai_api = input_parameter['openai_api']
        question = input_parameter['question']
        answer = input_parameter['answer']
        result = get_score(openai_api, question, answer)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e), "question": question, "answer": answer})

@app.route('/')
def introduction():
    return "Welcome to the IELTS Api"

@app.route('/questions/')
def get_questions():
    return jsonify({
        '1': "What is your full name?",
        '2': "Can I see your ID?",
        '3': "When you go shopping, do you prefer to pay for things in cash or by card? Why?",
        '4': "Do you ever save money to buy special things? Why/Why not?",
        '5': "Would you ever take a job that had low pay? Why/Why not?",
        '6': "Would winning a lot of money make a big difference to your life? Why/Why not?",
        '7': "Describe a toy you liked in your childhood. What was it? Who gave it to you? What it looked like? Explain why it was a special toy for you?",
        '8': "Do you think toys really help in children's development?",
        '9': "Does modern technology have an influence on children's toys?",
        '10': "In general, do children today have many toys?",
        '11': "How do you think toys will change in the future?"
    })


