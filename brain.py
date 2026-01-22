from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# 1. ඇප් එක සැකසීම
app = Flask(__name__)
CORS(app) 

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# 1. ඇප් එක සැකසීම
app = Flask(__name__)
CORS(app) 

# --- ආරක්ෂිත පියවර: සැබෑ යතුර මෙතන නැත ---
GENAI_API_KEY = os.environ.get("GEMINI_API_KEY")
# ----------------------------------------

# Gemini සම්බන්ධ කිරීම
genai.configure(api_key=GENAI_API_KEY)
# ... (ඉතිරි කෝඩ් එක කලින් වගේමයි)

# Gemini සම්බන්ධ කිරීම
genai.configure(api_key=GENAI_API_KEY)
# කලින් තිබුනේ 2.0 නේ, අපි ඒක 1.5 ට මාරු කරමු. මේක ගොඩක් Stable.
model = genai.GenerativeModel('gemini-flash-latest')

# මතකය (Memory)
chat_memory = []

@app.route('/chat', methods=['POST'])
def chat_engine():
    data = request.json
    user_input = data.get("message", "")
    
    # 1. හැඟීම් හඳුනා ගැනීම (Emotion Logic)
    emotion = "neutral"
    lower_input = user_input.lower()
    if any(w in lower_input for w in ["good", "happy", "wow", "thanks", "elakiri", "niyamai"]):
        emotion = "happy"
    elif any(w in lower_input for w in ["bad", "sad", "sorry", "awul", "dukai"]):
        emotion = "sad"

    # 2. Gemini වෙත යැවීම
    try:
        # පරණ කතා 5ක් මතක් කරලා දෙනවා
        history = "\n".join([f"User: {m['u']}\nAI: {m['a']}" for m in chat_memory[-5:]])
        prompt = f"Previous chat:\n{history}\n\nUser: {user_input}\nReply in Sinhala or English as appropriate. Keep it short and friendly."
        
        response = model.generate_content(prompt)
        ai_reply = response.text
    except Exception as e:
        ai_reply = "අන්තර්ජාලය පොඩ්ඩක් අවුල් වගේ යාලු. ආයේ බලමුද?"
        print(f"Error: {e}")

    # 3. මතකයේ සේව් කිරීම
    chat_memory.append({"u": user_input, "a": ai_reply})

    return jsonify({
        "reply": ai_reply,
        "emotion": emotion,
        "memory_count": len(chat_memory)
    })

if __name__ == "__main__":
    import os
    # Render එකට අවශ්‍ය Port එක හඳුනා ගැනීම
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Omega Brain is starting on port {port}...")
    # අන්තර්ජාලයට දොරවල් විවෘත කිරීම
    app.run(host='0.0.0.0', port=port)
