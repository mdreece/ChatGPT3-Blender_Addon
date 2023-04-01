bl_info = {
    "name": "ChatGPT-3 Integration",
    "author": "Dave Nectariad Rome",
    "version": (0, 9),
    "blender": (3, 40, 1),
    "location": "Text Editor > Sidebar > ChatGPT-3",
    "description": "Integrates ChatGPT-3 into Blender using the OpenAI API",
    "warning": "",
    "doc_url": "",
    "category": "Text Editor",
}

import bpy
import openai
import shutil
import os
import subprocess
import sys
from mathutils import Vector
from bpy_extras.io_utils import ExportHelper


def find_blender_python_executable(python_path):
    python_executable = None

    if python_path:
        python_executable = os.path.join(python_path, "bin", "python3.8" if sys.platform == "darwin" else "python.exe" if sys.platform == "win32" else "python3")

        # If the specified path doesn't exist, set python_executable to None
        if not os.path.exists(python_executable):
            python_executable = None

    # If the specified path is not valid or not provided, try to find the bundled Python executable in the default locations
    if not python_executable:
        paths_to_try = [
            os.path.join(sys.prefix, "bin", "python3.8" if sys.platform == "darwin" else "python.exe" if sys.platform == "win32" else "python3"),
            os.path.join(sys.prefix, "python", "bin", "python3.8" if sys.platform == "darwin" else "python.exe" if sys.platform == "win32" else "python3"),
            os.path.join(sys.prefix, "Scripts", "python.exe" if sys.platform == "win32" else "bin", "python3.8" if sys.platform == "darwin" else "python3"),
        ]

        for path in paths_to_try:
            if os.path.exists(path):
                python_executable = path
                break

    return python_executable



class ChatGPTAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    api_key: bpy.props.StringProperty(
        name="API Key",
        description="Enter your ChatGPT API key",
        default="",
        subtype="PASSWORD",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "api_key")


class GPT_OT_install_openai(bpy.types.Operator):
    bl_idname = "gpt.install_openai"
    bl_label = "Install OpenAI Library"

    def execute(self, context):
        preferences = bpy.context.preferences
        addon_prefs = preferences.addons[__name__].preferences
        python_exe = addon_prefs.python_path

        if not python_exe:
            self.report({'ERROR'}, "Please set the path to python.exe in the addon preferences.")
            return {'CANCELLED'}

        try:
            subprocess.check_call([python_exe, "-m", "pip", "install", "openai"])
            self.report({'INFO'}, "OpenAI Library Installation Complete")
        except subprocess.CalledProcessError as e:
            self.report({'ERROR'}, f"Error installing OpenAI library: {e}")

        return {'FINISHED'}




class GPT_OT_save_preferences(bpy.types.Operator):
    bl_idname = "gpt.save_preferences"
    bl_label = "Save Preferences"

    def execute(self, context):
        bpy.ops.wm.save_userpref()
        self.report({'INFO'}, "Preferences saved.")
        return {'FINISHED'}



class GPT_OT_generate_response(bpy.types.Operator):
    bl_idname = "gpt.generate_response"
    bl_label = "Generate Response"
    bl_options = {'REGISTER'}

    def execute(self, context):
        api_key = get_openai_api_key()
        if not api_key:
            self.report({'ERROR'}, "Please set your ChatGPT API key in the addon preferences.")
            return {'CANCELLED'}

        openai.api_key = api_key

        prompt = context.scene.chat_gpt_prompt
        try:
            response = generate_chat_gpt_response(prompt)
        except openai.error.RateLimitError:
            self.report({'ERROR'}, "You exceeded your current quota. Please check your plan and billing details.")
            return {'CANCELLED'}

        # Create a new Text datablock if not already present
        response_text = bpy.data.texts.get("ChatGPT_Response")
        if not response_text:
            response_text = bpy.data.texts.new("ChatGPT_Response")

        # Set the generated response text as the new property value
        response_text.from_string(response)

        # Open the generated response in the Text Editor
        for area in bpy.context.screen.areas:
            if area.type == "TEXT_EDITOR":
                area.spaces[0].text = response_text
                break

        return {'FINISHED'}



    @staticmethod
    def parse_move_command(response):
        move_vector = None
        move_commands = ['move', 'translate']
        tokens = response.lower().split()

        if any(cmd in tokens for cmd in move_commands):
            try:
                move_index = [tokens.index(cmd) for cmd in move_commands if cmd in tokens][0]
                x = float(tokens[move_index + 1])
                y = float(tokens[move_index + 2])
                z = float(tokens[move_index + 3])
                move_vector = Vector((x, y, z))
            except (ValueError, IndexError):
                pass

        return move_vector

class GPT_OT_run_script(bpy.types.Operator, ExportHelper):
    bl_idname = "gpt.run_script"
    bl_label = "Run Generated Script"

    filename_ext = ".py"
    filter_glob: bpy.props.StringProperty(default="*.py", options={"HIDDEN"})

    def execute(self, context):
        response = context.scene.chat_gpt_response

        # Save the script if desired
        if self.filepath:
            with open(self.filepath, "w") as f:
                f.write(response)

        # Run the generated script
        try:
            exec(response)
        except Exception as e:
            self.report({'ERROR'}, str(e))

        return {'FINISHED'}



class GPT_PT_panel(bpy.types.Panel):
    bl_idname = "GPT_PT_panel"
    bl_label = "ChatGPT-3"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'ChatGPT-3'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "chat_gpt_prompt")
        layout.operator("gpt.generate_response", icon='TRIA_RIGHT', text="Generate Response")

        # Display the generated response as an interactive multiline text box
        row = layout.row()
        row.label(text="Generated Response:")
        row = layout.row()
        row.prop(scene, "chat_gpt_response_text", text="")

        layout.operator("gpt.run_script", icon='PLAY', text="Run Generated Script")


def get_openai_api_key():
    preferences = bpy.context.preferences
    addon_prefs = preferences.addons[__name__].preferences
    return addon_prefs.api_key



def generate_chat_gpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()



def register():
    bpy.utils.register_class(GPT_OT_save_preferences)
    bpy.utils.register_class(ChatGPTAddonPreferences)
    bpy.utils.register_class(GPT_OT_generate_response)
    bpy.utils.register_class(GPT_OT_run_script)
    bpy.utils.register_class(GPT_PT_panel)
    bpy.utils.register_class(GPT_OT_install_openai)
    bpy.types.Scene.chat_gpt_prompt = bpy.props.StringProperty(name="Prompt")
    bpy.types.Scene.chat_gpt_response = bpy.props.PointerProperty(type=bpy.types.Text)  # Changed to PointerProperty
    bpy.types.Scene.chat_gpt_response_text = bpy.props.StringProperty(name="Generated Response", default="", subtype='NONE')

def unregister():
    bpy.utils.unregister_class(GPT_OT_save_preferences)
    bpy.utils.unregister_class(ChatGPTAddonPreferences)
    bpy.utils.unregister_class(GPT_OT_generate_response)
    bpy.utils.unregister_class(GPT_OT_run_script)
    bpy.utils.unregister_class(GPT_PT_panel)
    bpy.utils.unregister_class(GPT_OT_install_openai)
    del bpy.types.Scene.chat_gpt_prompt
    del bpy.types.Scene.chat_gpt_response
    del bpy.types.Scene.chat_gpt_response_text

if __name__ == "__main__":
    register()
