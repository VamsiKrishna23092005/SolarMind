# Connecting Local Ollama to Streamlit Cloud using Ngrok

When you run SolarMind on **Streamlit Community Cloud**, the cloud server cannot directly access the Models (like Llama3) running on your personal computer because `localhost` on the cloud means the cloud server itself (which does not have Ollama installed).

To bridge this gap and allow the free cloud dashboard to use your free local hardware, we use a tunneling tool called **Ngrok**.

Follow this full-fledged guide to set it up in 3 minutes!

---

## 🛠 Step 1: Install Ngrok
Ngrok is a safe, widely-used utility that creates a secure public URL (a tunnel) straight to an app running on your local machine.

1. **Sign up for a free Ngrok account:** [ngrok.com/signup](https://dashboard.ngrok.com/signup)
2. **Download Ngrok** for your operating system: [Download Page](https://ngrok.com/download)
   - *Windows users:* You can simply open Command Prompt and run: `winget install ngrok`
3. **Authenticate Ngrok:** Go to your Ngrok Dashboard, copy your Authtoken, and run this in your terminal:
   ```bash
   ngrok config add-authtoken <YOUR_TOKEN_HERE>
   ```

## 🔓 Step 2: Configure Ollama for External Traffic
By default, Ollama refuses connections from outside your own computer. You must tell it to allow Ngrok's traffic.

**On Windows:**
1. Open the **Start Menu** and search for "Environment Variables".
2. Click **"Edit the system environment variables"**.
3. In the window that pops up, click the **"Environment Variables..."** button at the bottom.
4. Under the "User variables" section, click **"New"**.
5. Set the Variable Name to `OLLAMA_ORIGINS`
6. Set the Variable Value to `*`
7. Click OK -> OK.
8. **CRITICAL:** Fully exit the Ollama app (right-click the llama icon in your bottom-right system tray and click "Quit Ollama"). Then restart Ollama from the Start Menu.

*(For Mac/Linux, run `OLLAMA_ORIGINS="*" ollama serve` in a terminal).*

## 🔌 Step 3: Start the Ngrok Tunnel
Open a fresh terminal window on your PC and run this command:

```bash
ngrok http 11434 --host-header="localhost:11434"
```
*(Port 11434 is Ollama's default listening port).*

You will see a black terminal screen pop up with a line that looks like this:
`Forwarding     https://a1b2-34-56-78-90.ngrok-free.app -> http://localhost:11434`

## 🚀 Step 4: Connect the Dashboard
1. Copy the **Forwarding URL** from your Ngrok terminal (e.g., `https://a1b2-34-56-78-90.ngrok-free.app`). **Do not copy the `localhost` part.**
2. Go to your live SolarMind Dashboard on Streamlit Community Cloud.
3. Open the **⚙️ Configuration** sidebar on the left side of the dashboard.
4. Paste the URL you copied into the **Ollama Base URL** text box.
5. Press Enter.

**🎉 You're done!** 
Now, when you click "Run Pipeline" on Streamlit Cloud, it will securely tunnel the heavy AI processing straight to your physical computer for free, and display the final report back on the public website!

*(Remember: If you turn your computer off or close the Ngrok terminal, the cloud website will disconnect. You must run Step 3 anytime you want the public site to work).*
