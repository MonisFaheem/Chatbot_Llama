import streamlit as st
import replicate
import os

st.set_page_config(page_title="🦙💬 RepliChat")


#Create a Side bar
with st.sidebar:
    st.title("🦙💬 RepliChat")
    st.header("Settings")

    add_replicate_api=st.text_input('Enter the Replicate API token', type='password')
    if not (add_replicate_api.startswith('r8_') and len(add_replicate_api)==40):
        st.warning('Please enter your credentials', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')

    st.subheader("Models and Parameters")

    select_model=st.selectbox("Choose a Llama 2 Model", ['Llama 2 7b', 'Llama 2 13b', 'Llama 2 70b'], key='select_model')
    if select_model=='Llama 2 7b':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif select_model=='Llama 2 13b':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    else:
        llm = 'replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48'

    temperature=st.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p=st.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length=st.slider('max_length', min_value=64, max_value=4096, value=512, step=8)

    st.markdown('created by Monis faheem (BSE-20F-054)')

os.environ['REPLICATE_API_TOKEN']=add_replicate_api
api_key = os.getenv('REPLICATE_API_TOKEN', '')  # Default to empty string if not found
if api_key:  # Only set if a valid key exists
    os.environ['REPLICATE_API_TOKEN'] = api_key

#Store the LLM Generated Reponese

if "messages" not in st.session_state.keys():
    st.session_state.messages=[{"role": "assistant", "content":"How may I assist you today?"}]

# Diplay the chat messages

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Clear the Chat Messages
def clear_chat_history():
    st.session_state.messages=[{"role":"assistant", "content": "How may I assist you today"}]

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Create a Function to generate the Llama 2 Response
def generate_llama2_response(prompt_input):
    default_system_prompt="You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for data in st.session_state.messages:
        print("Data:", data)
        if data["role"]=="user":
            default_system_prompt+="User: " + data["content"] + "\n\n"
        else:
            default_system_prompt+="Assistant" + data["content"] + "\n\n"
    output=replicate.run(llm, input={"prompt": f"{default_system_prompt} {prompt_input} Assistant: ",
                                     "temperature": temperature, "top_p":top_p, "max_length": max_length, "repititon_penalty":1})

    return output


#User -Provided Prompt

if prompt := st.chat_input(disabled=not add_replicate_api):
    st.session_state.messages.append({"role": "user", "content":prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a New Response if the last message is not from the asssistant

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Sochne do..."):
            response=generate_llama2_response(prompt)
            placeholder=st.empty()
            full_response=''
            for item in response:
                full_response+=item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)

    message= {"role":"assistant", "content":full_response}
    st.session_state.messages.append(message)




