from dotenv import load_dotenv
from openai import OpenAI
import os
import threading
import time
import sys

# Model configuration
# Using gpt-4o-mini: most cost-effective model that supports function calling for Google Suite actions
MODEL = "gpt-4o-mini"

# constants
ACTION = "ACTION"
NON_ACTION = "NON_ACTION"
N = "N"
E = "E"

### GOALS:
### create a simple AI agent that can answer questions and interact with google suite of apps to perform tasks
### A. use the open AI API to answer questions -- done
### B. enable actions 
###         we must decide if a query is an action. ask LLM? 
###     1. send action query + all tools available to LLM
###         how do you get all tools available?
###     2. LLM decides which tool would be best to use
###         how do you extract the answer in a reliable way? "give a one word answer"?
###     3. agent then has to execute the tool
###         no idea how to do this without composio
###     4. send the result back to LLM to generate natural query response
###         easy peasy

print("Welcome to Devam's first AI Agent")


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Authenticate API key by making a simple API call
try:
    client = OpenAI(api_key=OPENAI_API_KEY)
    models = client.models.list()
    print(f"Connected to OPEN AI API successfully")
except Exception as e:
    print(f"✗ Authentication failed: {e}")
    exit(1)


# Create a response using the chat completions API
# Why chat/completions instead of /v1/responses?
# - Supports custom function calling (needed for Google Suite APIs - Sheets, Docs, Gmail, etc.)
# - Responses API only has built-in tools (file search, web search) which don't cover Google Suite
# - More mature API with better documentation/examples
# - Cost-effective with gpt-4o-mini
# - Full control over conversation state and tool execution
def converse():
    print(f"enter {N} to create new conversation. {E} to exit.")
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    try:
        # Start loading animation and get the stop function
        # stop_loading_fn = start_loading_animation()
        while 1:
            user_input = input(">>")
            if user_input in ["N", "E"]:
                return user_input

            userInputMessage = {"role": "user", "content": user_input}
            isActionMessage = [
                {"role": "system", "content": f"You are helping me figure out if this user message is asking for an action to be taken in their google suite, or if its a generic question. Answer {ACTION} or {NON_ACTION}"},
                userInputMessage
            ]

            isActionResponse = response = client.chat.completions.create(
                model=MODEL,
                messages=isActionMessage
            )

            requestType = isActionResponse.choices[0].message.content
            print(f"The nature of this request is: {requestType}")

            if requestType == NON_ACTION:
                messages.append(userInputMessage)
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages
                )
                # Extract and print the assistant's response
                assistant_response = response.choices[0].message.content
                messages.append({"role": "system", "content": assistant_response})
                print(f"{assistant_response}")
            else: 
                print("Actions are not supported yet\n")
    except Exception as e:
        print(f"\n✗ Error generating response: {e}")


print("How can we help you today?\n")
response = ""
while 1:
    response = converse()
    if response == N:
        continue
    if response == E:
        break
