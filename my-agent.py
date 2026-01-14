from dotenv import load_dotenv
from openai import OpenAI
import os
import threading
import time
import sys

# Model configuration
# Using gpt-4o-mini: most cost-effective model that supports function calling for Google Suite actions
MODEL = "gpt-4o-mini"

### GOALS:
### create a simple AI agent that can answer questions and interact with google suite of apps to perform tasks
### right now we are using the open AI API to answer questions

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

# Loading animation function
# def show_loading(stop_event):
#     """Display animated loading dots while waiting for response"""
#     # Alternate between "..." and ".." so the last dot appears to blink
#     dots = ["...", ".."]
#     i = 0
#     while not stop_event.is_set():
#         # Use \r to overwrite the same line, and flush to show immediately
#         sys.stdout.write(f"\rThinking{dots[i % len(dots)]}")
#         sys.stdout.flush()
#         i += 1
#         time.sleep(0.5)
#     # Clear the loading line when done
#     sys.stdout.write("\r" + " " * 20 + "\r")
#     sys.stdout.flush()

# def start_loading_animation():
#     """Start the loading animation and return a function to stop it"""
#     stop_event = threading.Event()
#     loading_thread = threading.Thread(target=show_loading, args=(stop_event,))
#     loading_thread.daemon = True
#     loading_thread.start()
    
#     def stop_fn():
#         """Stop the loading animation"""
#         stop_event.set()
#         loading_thread.join()
#     return stop_fn

# Create a response using the chat completions API
# Why chat/completions instead of /v1/responses?
# - Supports custom function calling (needed for Google Suite APIs - Sheets, Docs, Gmail, etc.)
# - Responses API only has built-in tools (file search, web search) which don't cover Google Suite
# - More mature API with better documentation/examples
# - Cost-effective with gpt-4o-mini
# - Full control over conversation state and tool execution
def converse():
    print("enter N to create new conversation. E to exit.")
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    try:
        # Start loading animation and get the stop function
        # stop_loading_fn = start_loading_animation()
        while 1:
            user_input = input(">>")
            if user_input in ["N", "E"]:
                return user_input
            messages.append({"role": "user", "content": user_input})
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages
            )
            # Stop the loading animation
            # if stop_loading_fn:
            #     stop_loading_fn()
            # Extract and print the assistant's response
            assistant_response = response.choices[0].message.content
            messages.append({"role": "system", "content": assistant_response})
            print(f"{assistant_response}")

    except Exception as e:
        # Stop loading animation if there's an error
        # if stop_loading_fn:
        #     stop_loading_fn()
        print(f"\n✗ Error generating response: {e}")


print("How can we help you today?\n")
response = ""
while 1:
    response = converse()
    if response == "N":
        continue
    if response == "E":
        break
