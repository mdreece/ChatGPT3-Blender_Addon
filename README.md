# ChatGPT3-Blender_Addon (ALPHA)

CURRENT VERSION: 0.9.2




!!! YOU WILL NEED YOUR OWN OPENAI API KEY !!!
https://platform.openai.com/account/api-keys

!!! FOR MIRCOSOFT WINDOWS OS ONLY !!!


The ChatGPT-3 Integration Addon allows Blender users to generate text responses to a prompt using OpenAI's GPT-3 API. The generated response can be displayed in the Text Editor. (results may vary)
Installation
To install the addon, follow these steps:

1. Download or create a BATCH file using this linked script. https://raw.githubusercontent.com/mdreece/ChatPGT3-Blender_Addon/main/chat_gpt3_addon_INSTALL.bat
2. Save the BATCH (.bat) anywhere and run as ADMIN
3. The .BAT will install OPENAI Python Libraries, CURL and add the add-on to your BLENDER system (an extraction error may appear, but all should still operate as expected).
4. BLENDER will open and the add-on should be enabled. (If not search for ‘Chat’)


Setting up the API key
Before using the addon, you need to set up your API key for OpenAI's GPT-3 API. To do this, follow these steps:

1. Open Blender and go to the "Preferences" window.
2. Click on the "Add-ons" tab and search for "ChatGPT" in the search bar.
3. Click on the "ChatGPT-3 Integration" addon to open its preferences.
4. Enter your OpenAI API key in the "API Key" field.
5. Select the desired 'Model'
6. Click the "Save Preferences" button to save your changes.
    
    
Using the addon
To use the addon, follow these steps:

1. Open Blender and go to the Text Editor.
2. In the sidebar, click on the "ChatGPT-3" tab to open the addon panel.
3. Enter your prompt in the "Prompt" field.
4. Click the "Generate Response" button to generate a response to your prompt. (You may have to click twice)
5. The generated response will be displayed in the "Generated Response" field as a multi-line text box.
6. If desired, you can save the generated response as a new script by clicking the "Run Generated Script" button and choosing a file name and location.
    
    
Notes
 - The addon has been tested with Blender version 3.4.1 and 3.4.
 - This has only been tested on Windows 10 Enterprise
 - The addon may be compatible with other versions of Blender, but this has not been tested.
 - The addon requires an active internet connection to use the GPT-3 API.
 - OpenAI Python Libraries REQUIRED











CHANGELOG:

4/1/2023: v0.9.2
 - Added access to Github in Preferences
 - Added access to Documentation in Preferences
 - Prompt to enter API if it is not and a Response is generated
 

4/1/2023: v0.9.1
 - Removed 'Generated Response' text bar of v0.9 (not operational)
 - Removed 'Run Generated Response' of v0.9 (not operational)
 - Model Selection added to Preferences
    - Davinci-003
    - Davinci-002
    - Davinci-001
    - Curie-001
 

3/31/2023: v0.9
 - RELEASE!!!!



"Dave Nectariad Rome" is just my full name all mixed up. (Entire Script is made for fun)
