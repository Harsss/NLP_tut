import os

from langchain.llms import OpenAI
from langchain import PromptTemplate
import streamlit as st
import PIL
from langchain.chains import LLMChain
os.environ["OPENAI_API_KEY"]='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'
from langchain.memory import ConversationBufferMemory

from langchain.chains import SimpleSequentialChain
# streamlit framework

st.title('Safeguard of PII data from LLM, Team HS TK')
input_text=st.text_input("Enter your prompt")

first_input_prompt = PromptTemplate(
    input_variables=['text'],
    template="Convert the following text while concealing any sensitive information and removing any code-related context. Additionally, provide a list of the data that has been concealed for future reference. Text is: {text}"
)



conceal_data = ConversationBufferMemory(input_key='masked', memory_key='chat_history')

llm=OpenAI(temperature=0.8)

chain=LLMChain(llm=llm,prompt=first_input_prompt,verbose=True,output_key='mask_prompt')


second_input_prompt = PromptTemplate(
    input_variables=['mask_prompt'],
    template="What suggestion you can give me if, {mask_prompt}",
)


chain2=LLMChain(llm=llm,prompt=second_input_prompt,verbose=True,output_key='mask_output')


parent_ch=SimpleSequentialChain(chains=[chain,chain2],verbose=True)
if input_text:
    mask=chain.run(input_text)
    print('The output from our Falcon is {mask}')
    st.write(mask)
    st.write(chain2.run(mask))
    # st.write(parent_ch.run(input_text))
    


