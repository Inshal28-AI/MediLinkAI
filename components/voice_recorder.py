import streamlit as st

def voice_recorder_component(key="voice_main"):
    """
    Renders a browser-based voice recorder using the Web Speech API.
    """
    component_html = f"""
    <div class="voice-recorder-wrap">
        <div style="font-size:0.68rem;font-weight:600;letter-spacing:1.2px;
                    color:#06b6d4;text-transform:uppercase;margin-bottom:0.6rem;">
            🎙 Voice Dictation
        </div>
        <div style="display:flex;gap:0.6rem;align-items:center;flex-wrap:wrap;">
            <button class="recorder-btn" id="recBtn_{key}" onclick="toggleRec_{key}()">
                🎤 &nbsp;Start Recording
            </button>
            <button class="recorder-btn" id="clearBtn_{key}"
                    style="background:linear-gradient(135deg,#374151,#1f2937);border-color:rgba(255,255,255,0.1);"
                    onclick="clearTranscript_{key}()">
                ✕ &nbsp;Clear
            </button>
            <button class="recorder-btn" id="useBtn_{key}"
                    style="background:linear-gradient(135deg,#065f46,#064e3b);border-color:rgba(16,185,129,0.3);"
                    onclick="useTranscript_{key}()">
                ✓ &nbsp;Use Text
            </button>
        </div>
        <div class="transcript-box" id="transcript_{key}">
            {st.session_state.get('voice_transcript','') or 'Transcription will appear here as you speak…'}
        </div>
        <div class="rec-status" id="status_{key}">
            ⚠ Works best in Chrome or Edge. Click Start Recording and allow microphone access.
        </div>
    </div>

    <script>
    (function() {{
        const key = '{key}';
        let recognition = null;
        let isRecording = false;
        let fullTranscript = `{st.session_state.get('voice_transcript','').replace('`','\\`')}`;

        const btn     = document.getElementById('recBtn_'    + key);
        const box     = document.getElementById('transcript_'+ key);
        const statusEl= document.getElementById('status_'   + key);

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {{
            statusEl.textContent = '❌ Speech recognition not supported in this browser. Use Chrome or Edge.';
            btn.disabled = true; btn.style.opacity = '0.4';
            return;
        }}

        function buildRecognition() {{
            const r = new SpeechRecognition();
            r.continuous      = true;
            r.interimResults  = true;
            r.lang            = 'en-US';

            r.onstart = () => {{
                isRecording = true;
                btn.textContent = '⏹  Stop Recording';
                btn.classList.add('recording');
                statusEl.textContent = '🔴 Recording… speak clearly.';
            }};

            r.onresult = (e) => {{
                let interim = '';
                for (let i = e.resultIndex; i < e.results.length; i++) {{
                    const t = e.results[i][0].transcript;
                    if (e.results[i].isFinal) {{ fullTranscript += t + ' '; }}
                    else {{ interim = t; }}
                }}
                box.textContent = fullTranscript + (interim ? '[' + interim + ']' : '');
            }};

            r.onerror = (e) => {{
                statusEl.textContent = '❌ Mic error: ' + e.error + '. Check browser permissions.';
                stopRec();
            }};

            r.onend = () => {{ if (isRecording) r.start(); }};
            return r;
        }}

        function stopRec() {{
            isRecording = false;
            if (recognition) {{ recognition.onend = null; recognition.stop(); }}
            btn.textContent = '🎤  Start Recording';
            btn.classList.remove('recording');
            statusEl.textContent = '✓ Recording stopped. Click "Use Text" to copy to notes.';
        }}

        window['toggleRec_' + key] = function() {{
            if (!isRecording) {{
                recognition = buildRecognition();
                recognition.start();
            }} else {{
                stopRec();
            }}
        }};

        window['clearTranscript_' + key] = function() {{
            fullTranscript = '';
            box.textContent = 'Transcription will appear here as you speak…';
            statusEl.textContent = 'Transcript cleared.';
        }};

        window['useTranscript_' + key] = function() {{
            if (!fullTranscript.trim()) {{
                statusEl.textContent = '⚠ Nothing to copy yet — record first.';
                return;
            }}
            const textareas = window.parent.document.querySelectorAll('textarea');
            let target = null;
            textareas.forEach(ta => {{
                if (ta.placeholder && ta.placeholder.includes('Pt presents')) target = ta;
            }});
            if (target) {{
                const nativeSetter = Object.getOwnPropertyDescriptor(
                    window.HTMLTextAreaElement.prototype, 'value').set;
                nativeSetter.call(target, (target.value ? target.value + ' ' : '') + fullTranscript.trim());
                target.dispatchEvent(new Event('input', {{ bubbles: true }}));
                statusEl.textContent = '✓ Text appended to clinical notes!';
            }} else {{
                navigator.clipboard.writeText(fullTranscript.trim()).then(() => {{
                    statusEl.textContent = '📋 Copied to clipboard — paste into notes manually.';
                }});
            }}
        }};
    }})();
    </script>
    """
    st.components.v1.html(component_html, height=220, scrolling=False)