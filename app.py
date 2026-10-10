import base64
import streamlit as st
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pss

st.set_page_config(
    page_title="CryptaSign | Digital Signature Security",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --bg:#080d18; --panel:#101a2b; --line:#25344a; --muted:#9aabc3; --cyan:#5ce1e6; --violet:#a78bfa; }
html, body, [class*="css"] { font-family: 'Manrope', sans-serif; }
.stApp { background: radial-gradient(ellipse at 80% 0%, #14264a 0%, #080d18 45%); color:#edf5ff; }
.block-container { max-width: 1180px; padding-top: 2rem; padding-bottom: 4rem; }
section[data-testid="stSidebar"] { background:#0b1322; border-right:1px solid var(--line); }
.hero { border:1px solid #263b55; border-radius:24px; padding:32px; background:linear-gradient(125deg,rgba(20,40,68,.96),rgba(17,23,43,.86)); box-shadow:0 20px 60px #0003; }
.eyebrow { color:var(--cyan); letter-spacing:2px; font-size:.76rem; font-weight:800; text-transform:uppercase; }
.hero h1 { font-size:clamp(2.2rem,5vw,4.1rem); line-height:1.04; letter-spacing:-2px; margin:.6rem 0 1rem; color:#f3f8ff; }
.hero p { color:#b6c7dc; max-width:690px; font-size:1.05rem; }
.pill { display:inline-block; border:1px solid #35506c; color:#d8e9fa; border-radius:99px; padding:6px 11px; margin:5px 5px 0 0; font-size:.78rem; }
.panel { background:rgba(16,26,43,.84); border:1px solid var(--line); border-radius:18px; padding:20px; min-height:120px; }
.metric { color:var(--muted); font-size:.82rem; }
.metric strong { display:block; color:#f1f7ff; font-size:1.55rem; margin-top:8px; }
.section-title { font-size:1.35rem; font-weight:800; margin:1rem 0 .25rem; }
.muted { color:var(--muted); }
.stButton > button { border-radius:11px; min-height:2.8rem; font-weight:700; border:1px solid #3b5876; }
.stButton > button[kind="primary"] { background:linear-gradient(90deg,#4dd9e0,#8b9cfb); color:#07111e; border:0; }
div[data-baseweb="tab-list"] { gap:8px; border-bottom:1px solid var(--line); }
button[data-baseweb="tab"] { border-radius:10px 10px 0 0; }
textarea, input { font-family:'DM Mono',monospace !important; }
code { font-family:'DM Mono',monospace !important; }
div[data-testid="stExpander"] { border:1px solid var(--line); border-radius:12px; }
.small-note { color:#8fa5c0; font-size:.8rem; }
</style>
""", unsafe_allow_html=True)

def init_state():
    defaults = {
        "private_key": None,
        "public_key": None,
        "signature": "",
        "signed_message": "",
        "verify_result": None,
        "verify_detail": "",
        "verification_count": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

with st.sidebar:
    st.markdown("## 🔐 CRYPTASIGN")
    st.caption("DIGITAL TRUST STUDIO")
    st.markdown("---")
    st.markdown("### Workspace")
    page = st.radio(
        "Navigate",
        ["Overview", "Sign a message", "Verify a signature", "Learn the cryptography"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("### Security status")
    st.success("RSA + SHA-256 ready")
    st.caption("RSA-PSS signature scheme")
    st.markdown("---")
    st.markdown('<div class="small-note">Educational prototype · Local session only</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="eyebrow">CRYPTOGRAPHY • INTEGRITY • TRUST</div>
  <h1>Make trust<br>verifiable.</h1>
  <p>A hands-on digital signature studio. Sign a message with a private key, then independently verify it with the matching public key — and see what happens when data changes.</p>
  <span class="pill">RSA-2048</span><span class="pill">SHA-256</span><span class="pill">RSA-PSS</span><span class="pill">Interactive lab</span>
</div>
""", unsafe_allow_html=True)

st.write("")
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown('<div class="panel"><div class="metric">KEY PAIR</div><strong>RSA-2048</strong><div class="muted">Private + public key</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="panel"><div class="metric">MESSAGE FINGERPRINT</div><strong>SHA-256</strong><div class="muted">Fixed-length digest</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="panel"><div class="metric">SIGNATURE SCHEME</div><strong>RSA-PSS</strong><div class="muted">Probabilistic signature</div></div>', unsafe_allow_html=True)

st.write("")
if page == "Overview":
    st.markdown('<div class="section-title">Your verification journey</div>', unsafe_allow_html=True)
    st.markdown('<div class="muted">Complete the steps in order. Everything runs in this app session.</div>', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    with a:
        st.markdown('<div class="panel"><h3>01 · Create keys</h3><p class="muted">Generate a private key for signing and a public key for verification.</p></div>', unsafe_allow_html=True)
        if st.button("Generate RSA key pair", type="primary", use_container_width=True):
            key = RSA.generate(2048)
            st.session_state.private_key = key.export_key().decode()
            st.session_state.public_key = key.publickey().export_key().decode()
            st.session_state.signature = ""
            st.session_state.signed_message = ""
            st.session_state.verify_result = None
            st.success("New key pair generated.")
    with b:
        st.markdown('<div class="panel"><h3>02 · Sign message</h3><p class="muted">Create a signature for the exact message using the private key.</p></div>', unsafe_allow_html=True)
        if st.button("Open signing studio", use_container_width=True):
            st.session_state["nav_jump"] = "Sign a message"
            st.info("Choose “Sign a message” in the sidebar.")
    with c:
        st.markdown('<div class="panel"><h3>03 · Verify result</h3><p class="muted">Check the signature with the public key and test message integrity.</p></div>', unsafe_allow_html=True)
        if st.button("Open verification lab", use_container_width=True):
            st.info("Choose “Verify a signature” in the sidebar.")
    if st.session_state.public_key:
        st.success("Key pair is ready. Continue to “Sign a message” in the sidebar.")
        with st.expander("Inspect public key"):
            st.code(st.session_state.public_key, language="text")
        with st.expander("Inspect private key (keep secret)"):
            st.warning("For this educational demo only. Never share a private key.")
            st.code(st.session_state.private_key, language="text")
    else:
        st.info("Start by generating an RSA key pair above.")
    st.markdown("#### What makes a signature useful?")
    x, y = st.columns(2)
    with x:
        st.markdown('<div class="panel"><h4>✓ Integrity</h4><p class="muted">A modified message should fail verification.</p></div>', unsafe_allow_html=True)
    with y:
        st.markdown('<div class="panel"><h4>✓ Key correspondence</h4><p class="muted">Verification checks that the signature matches the supplied public key.</p></div>', unsafe_allow_html=True)

elif page == "Sign a message":
    st.markdown('<div class="section-title">02 / Signing studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="muted">Write a message, then create its digital signature.</div>', unsafe_allow_html=True)
    if not st.session_state.private_key:
        st.warning("Generate a key pair first on the Overview page.")
        if st.button("Generate keys now", type="primary"):
            key = RSA.generate(2048)
            st.session_state.private_key = key.export_key().decode()
            st.session_state.public_key = key.publickey().export_key().decode()
            st.success("Key pair generated. You can sign now.")
    message = st.text_area("Message to sign", value=st.session_state.signed_message, height=140, placeholder="Example: Approve document version 1.0")
    left, right = st.columns([1, 1])
    with left:
        if st.button("✍️ Create digital signature", type="primary", use_container_width=True):
            if not st.session_state.private_key:
                st.error("Generate a key pair first.")
            elif not message:
                st.error("Enter a message before signing.")
            else:
                key = RSA.import_key(st.session_state.private_key)
                digest = SHA256.new(message.encode("utf-8"))
                sig = pss.new(key).sign(digest)
                st.session_state.signature = base64.b64encode(sig).decode("ascii")
                st.session_state.signed_message = message
                st.session_state.verify_result = None
                st.success("Signature created for this exact message.")
    with right:
        if st.button("Clear signature", use_container_width=True):
            st.session_state.signature = ""
            st.session_state.signed_message = ""
            st.session_state.verify_result = None
            st.rerun()
    if st.session_state.signature:
        st.markdown("#### Signature output")
        st.code(st.session_state.signature, language="text")
        st.caption(f"Message length: {len(st.session_state.signed_message.encode('utf-8'))} bytes · Signature encoding: Base64")
        st.download_button("Download signature (.txt)", st.session_state.signature, file_name="digital_signature.txt", mime="text/plain")
        with st.expander("View public key for sharing"):
            st.code(st.session_state.public_key, language="text")
        st.info("Copy the signature and public key when you need to verify this message. Keep the private key secret.")

elif page == "Verify a signature":
    st.markdown('<div class="section-title">03 / Verification lab</div>', unsafe_allow_html=True)
    st.markdown('<div class="muted">Paste a message, signature, and public key. Any change to the signed message should invalidate the signature.</div>', unsafe_allow_html=True)
    default_msg = st.session_state.signed_message
    default_sig = st.session_state.signature
    default_pub = st.session_state.public_key or ""
    verify_message = st.text_area("Message to verify", value=default_msg, height=120, key="verify_message_input")
    verify_sig = st.text_area("Digital signature (Base64)", value=default_sig, height=120, key="verify_signature_input", placeholder="Paste the complete Base64 signature")
    verify_pub = st.text_area("Public key (PEM)", value=default_pub, height=180, key="verify_public_input", placeholder="-----BEGIN PUBLIC KEY----- ...")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔎 Verify signature", type="primary", use_container_width=True):
            st.session_state.verification_count += 1
            try:
                if not verify_message:
                    raise ValueError("Enter the message to verify.")
                if not verify_sig.strip():
                    raise ValueError("Paste the generated Base64 signature, not the message text.")
                if not verify_pub.strip():
                    raise ValueError("Paste the public key.")
                key = RSA.import_key(verify_pub.strip())
                if key.has_private():
                    key = key.publickey()
                sig = base64.b64decode(verify_sig.strip(), validate=True)
                digest = SHA256.new(verify_message.encode("utf-8"))
                pss.new(key).verify(digest, sig)
                st.session_state.verify_result = True
                st.session_state.verify_detail = "The signature is valid for this message and public key."
            except (ValueError, TypeError, IndexError):
                st.session_state.verify_result = False
                st.session_state.verify_detail = "Verification failed. Check the message, Base64 signature, and public key."
            except Exception:
                st.session_state.verify_result = False
                st.session_state.verify_detail = "The signature does not match this message and public key."
    with c2:
        if st.button("🧪 Load tampering test", use_container_width=True):
            if st.session_state.signed_message:
                st.session_state["verify_message_input"] = st.session_state.signed_message + " [modified]"
                st.session_state["verify_signature_input"] = st.session_state.signature
                st.session_state["verify_public_input"] = st.session_state.public_key or ""
                st.session_state.verify_result = None
                st.rerun()
            else:
                st.warning("Sign a message first, then try the tampering test.")
    if st.session_state.verify_result is True:
        st.success("✅ VALID SIGNATURE")
        st.write(st.session_state.verify_detail)
    elif st.session_state.verify_result is False:
        st.error("✕ INVALID SIGNATURE")
        st.write(st.session_state.verify_detail)
    st.caption("For best results, sign a message first, then verify it without editing any field.")
    with st.expander("What does the result mean?"):
        st.write("VALID means the signature verifies for the supplied message and public key. INVALID means the signature, message, or key is wrong or malformed. A valid signature alone does not prove a real-world identity unless the public key is trusted.")

else:
    st.markdown('<div class="section-title">Cryptography, made understandable</div>', unsafe_allow_html=True)
    st.markdown("#### The process")
    st.markdown("""
    1. **Hash:** SHA-256 calculates a fixed-length digest of the message.
    2. **Sign:** RSA-PSS uses the private key to create a signature over that digest.
    3. **Verify:** The public key checks whether the signature matches the exact message.
    4. **Tamper test:** Changing even one character changes the digest, so verification should fail.
    """)
    st.warning("Digital signatures provide integrity and support authenticity checks. They do not encrypt the message or guarantee that its contents are true.")
    st.markdown("#### Key safety")
    st.write("Share the public key and signature as needed. Never share the private key. This classroom prototype keeps keys in the active app session and is not designed for production secrets.")
    st.markdown("#### Technologies")
    st.write("Python · Streamlit · PyCryptodome · RSA-2048 · SHA-256 · RSA-PSS")

st.markdown("---")
st.markdown('<div class="small-note">CRYPTASIGN · CNS MICROPROJECT · Educational prototype. Validate public-key identity through a trusted channel in real deployments.</div>', unsafe_allow_html=True)
