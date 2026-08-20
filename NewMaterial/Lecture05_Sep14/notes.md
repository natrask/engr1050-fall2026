# Lecture 5: Introduction to microcontrollers and the Thonny IDE

This Monday, Prof. Trask had to present at a conference and lecture was covered by Mr. Shaffer. To prepare for writing small microcontroller problem on robots, we need to set up Thonny, an integrated development environment (IDE) that lets you run Python programs on your own computer and on Raspberry Pis. While Colab runs on some GPU server in Google's basement, you are now able to run code directly on your laptop, which is necessary now that you'll be hooking your computer up to microcontrollers and robots.

We also will give a first overview on what the Raspberry Pi is, how it works, and how you'll program it in Thonny. This is just an introductory lecture to get oriented; you'll get your bearings on how to actually use this stuff in the first lab session. Your only objective today is to get Thonny installed on your computer, and the assignment confirms that you have successfully done that.

**Directions for installing Thonny:**

Below are very explicit, step-by-step instructions for installing Thonny on Windows and macOS. Follow only the steps for the computer you are using. If you get stuck, ask a classmate or instructor for help — these steps are written for people with little or no installation experience.

Windows:

1. Prepare:
   - Make sure you are connected to the Internet.
   - Close other programs while installing (optional but helpful).

2. Download Thonny:
   - Open a web browser (Chrome, Edge, or Firefox).
   - Go to: https://thonny.org/ (type it into the address bar and press Enter).
   - Click the big green "Download" button and choose the Windows installer (it will be an .exe file). Save the file when prompted.

3. Run the installer:
   - In your browser, click the downloaded file (or open your Downloads folder and double‑click the .exe file).
   - If Windows asks "Do you want to allow this app to make changes to your device?", click "Yes".
   - Follow the installer prompts. Accept the default options unless you know you need something different. Click "Next" and then "Install".

4. Finish and open Thonny:
   - When installation completes, click "Finish" and then open the Start menu and type "Thonny" to find and run it.

5. Verify it works (simple test):
   - In Thonny's editor (top area) type: print("Hello, Thonny!")
   - Click the green Run button (or press F5). You should see Hello, Thonny! in the bottom "Shell" area.

6. Troubleshooting (Windows):
   - If the installer won’t run, right‑click the .exe and choose "Run as administrator".
   - If Windows blocks the app, open "Settings → Update & Security → Windows Security → App & browser control" and allow the app, or ask an instructor.

macOS:

1. Prepare:
   - Make sure you are connected to the Internet and you know the password for your Mac account (you may need it to allow installs).

2. Download Thonny:
   - Open Safari (or another browser) and go to: https://thonny.org/
   - Click the "Download" button and choose the macOS installer. If there are different choices, pick the one labeled for your CPU: "macOS (Intel)" for older Macs, or "macOS (Apple Silicon)" for M1/M2 Macs. Save the .dmg file.

3. Install Thonny:
   - Double‑click the downloaded .dmg file in your Downloads folder.
   - A small window will open showing the Thonny app icon. Drag the Thonny icon into the Applications folder icon in that window.
   - After copying finishes, eject the mounted installer (right‑click the Thonny disk on the Desktop or in Finder and choose "Eject").

4. Open Thonny:
   - Open the Applications folder and double‑click Thonny to run it.
   - The first time you open it, macOS may warn that it is an app downloaded from the Internet. If you see that, open "System Preferences → Security & Privacy" and click "Open Anyway" for Thonny.

5. Verify it works (simple test):
   - In Thonny's editor, type: print("Hello, Thonny!")
   - Click Run (or press F5). You should see the output in the Shell.

6. Troubleshooting (macOS):
   - If macOS prevents opening the app, go to "System Preferences → Security & Privacy → General" and click "Open Anyway" next to the message about Thonny.
   - If you aren’t sure which macOS download to use (Intel vs Apple Silicon), check your Mac: Apple menu → About This Mac. If it mentions "Apple M1" or "Apple M2", choose Apple Silicon.

Quick tips for everyone

- After installing, you can create a simple Python file:
  - In Thonny's editor type:
    print("My name is <your name>")
  - Save the file (File → Save) in a folder you can find (Desktop or Documents).
  - Press Run → Run current script (or F5) to execute it.

**If you have any issues getting Thonny set up bring your laptop to office hours and we'll get you squared away.**
