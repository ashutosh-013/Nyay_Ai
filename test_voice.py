from modules.voice_module import listen_to_user, speak_output

print("Running voice test...")  # NEW LINE

text = listen_to_user()
print("Recognized:", text)

speak_output("You said: " + text)
