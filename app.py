from flask import Flask,jsonify,request,send_file
import openai
from openai import AzureOpenAI
import json
import json 
import csv
from xlsxwriter.workbook import Workbook
import os

app = Flask(__name__) 
@app.route('/') 
def home(): 

       return  """<title>Generate MCQ Excel file</title>
    <h1>Enter the details</h1>
    <form action="/generatefile" method=post enctype=multipart/form-data>
        <label>Enter the skill about which you want to create questions</label>
        <input type=text name=skills><br>
        <label>Enter No of questions(Maximum : 45 questions)</label>
        <input type=text name=noofquestion><br>
        <label>Enter difficulty level of questions [medium,easy,hard]</label>
        <input type=text name=difficultylevel><br>
        <label>Enter sub Topic</label>
        <input type=text name=topic><br>
        <input type=submit value=Generate And Download File>
    </form>"""

@app.route("/generatefile",methods=['POST','GET'])

def generatefile():
    try:
        api_key="df6489eb3f8f4f838122924dfdd39ecd"
        azure_openai_endpoint="https://rutul-new-openai-1.openai.azure.com/"
        client = AzureOpenAI(
            azure_endpoint = azure_openai_endpoint, 
            api_key=api_key,  
            api_version="2024-02-15-preview"
             )
        data = request.form
        sample="""{
            "questions":[
                {
                "question": ,
                "options": [(list of 4 options without A,B,C,D)],
                "answer" : (it should be answer from the options only)
                }
            ]
        }
        """
        skill=data['skills']
        topic = data['topic']  
        difficultylevel=data['difficultylevel']
        noOfQuestions=data['noofquestion']
        prompt1=f"Generate {noOfQuestions} number of {difficultylevel} mcq question for {skill} on {topic} with 4 options.Return an array of questions in a JSON object where  keys should be question,options,answer and options key values should be a list of 4 option witohout A,B,C,D and answer key as answer from the options and Here is the sample output in which you need to generate the answer strictly in this format <sample>{sample}<sample> and you need to give data in one go"
        response=client.chat.completions.create(
            model="gpt-35-turbo",
            max_tokens=4050,
            messages=[
                {"role": "user", "content": prompt1}
            ]   
            )
        with open("text.txt","w+") as f :
            f.write(response.choices[0].message.content)
            print(response.choices[0].message.content)
            newdata1=json.loads(response.choices[0].message.content)
    # print(newdata1)
        out=1
        if difficultylevel == 'hard':   
         out=3
        if difficultylevel == 'medium': 
            out=2
        answer="ABCD"
        for i in range(0,len(newdata1['questions'])):
            options = newdata1['questions'][i]['options']
            if type(newdata1['questions'][i]['answer']) == list and len(newdata1['questions'][i]['answer']) >1:                
                type1 = 1
                for j in range(0,len(newdata1['questions'][i]['answer'])):
                    val1=val1+f",{answer[int(options.index(newdata1['questions'][i]['answer']))]}"
            else :
                type1 = 0
                val = options.index(newdata1['questions'][i]['answer'])
                val1 = answer[int(val)]
            del newdata1['questions'][i]['answer']
            if 'id' in newdata1['questions'][i].keys():
                del newdata1['questions'][i]['id']
            newdata1['questions'][i]['Question']=newdata1['questions'][i]['question']
            del newdata1['questions'][i]['question']
            newdata1['questions'][i]['A']=f"{newdata1['questions'][i]['options'][0]}"
            newdata1['questions'][i]['B']=f"{newdata1['questions'][i]['options'][1]}"
            newdata1['questions'][i]['C']=f"{newdata1['questions'][i]['options'][2]}"
            newdata1['questions'][i]['D']=f"{newdata1['questions'][i]['options'][3]}"
            newdata1['questions'][i]['Answer'] = val1
            del newdata1['questions'][i]['options']
            newdata1['questions'][i]['Type'] = type1
            newdata1['questions'][i]['Difficulty level']=f'{out}'
            newdata1['questions'][i]['Weightage']=1
            newdata1['questions'][i]['SubTopicName']=topic

        question_data = newdata1['questions']
        file_name=f'{skill}_{topic}_{difficultylevel}_{noOfQuestions}_mcq'
        with open(f'{file_name}.csv','w') as f:
            dw = csv.DictWriter(f,question_data[0].keys(),delimiter='\t',lineterminator='\n')
            dw.writeheader()
            dw.writerows((question_data))

        tsv_file=f'{file_name}.csv'
        with open(f'{file_name}.xlsx','w') as f:
            f.close()
        xlsx_file=f'{file_name}.xlsx'
        workbook = Workbook(xlsx_file)
        worksheet = workbook.add_worksheet()
        with open(tsv_file, 'r', encoding='utf-8') as file:
            read_csv = csv.reader(file, delimiter='\t')
            for row_num, data in enumerate(read_csv):
                worksheet.write_row(row_num, 0, data)
        workbook.close()
        csv.excel
        os.remove(tsv_file)
        return send_file( xlsx_file, as_attachment=False)
    except :
        return "Please try again"


if __name__ == '__main__': 
  
    app.run(debug = True) 