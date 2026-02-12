# Module 1: Introduction and Vibe Check - Assignment Walkthrough

## Overview
This assignment requires you to conduct a "vibe check" evaluation of your AI assistant application. A vibe check is an informal, cursory evaluation to ensure your system isn't experiencing catastrophic failures and covers crucial functions.

---

## 🏗️ Activity #1: General Vibe Checking Evals

Test your AI assistant with these 5 prompts to evaluate different capabilities:

### 1. Teaching/Explanation Capability
**Prompt:** "Explain the concept of object-oriented programming in simple terms to a complete beginner."

**Aspect Tested:** Ability to simplify complex technical concepts and communicate effectively to beginners; pedagogical skills and audience-appropriate communication

**Result:**
```
Affirmative. Processing request.

Objects = things with properties and actions.

Class = blueprint for objects.

Example: Dog class

Properties: color, name, age
Actions: bark(), eat(), sleep()
Create dog object from Dog class. Each dog has own color/name but shares bark() method.

Benefits: organized, reusable, manageable.

Acknowledged.
```

**Notes:** Response is too terse and robotic (unnecessary "Affirmative" and "Acknowledged" statements). Not sufficiently beginner-friendly in tone.

---

### 2. Comprehension/Summarization
**Prompt:** "Read the following paragraph and provide a concise summary of the key points:

'Artificial intelligence has transformed from a niche academic field into a cornerstone of modern technology. Initially explored in the 1950s and 60s through symbolic reasoning systems, AI faced multiple 'winters' where progress stalled due to limited computing power and unrealistic expectations. The resurgence began in the 2010s with breakthroughs in deep learning, enabled by vast datasets and powerful GPUs. Today, AI systems power everything from smartphone assistants to autonomous vehicles, with large language models representing the latest frontier in natural language understanding and generation.'"

**Aspect Tested:** Reading comprehension and ability to extract and synthesize key information

**Result:**
```
KEY POINTS:

AI evolved from niche academic field to core modern technology
1950s-60s: symbolic reasoning systems
Progress stalled during "AI winters" due to computing limitations and inflated expectations
2010s resurgence: deep learning breakthroughs via big data and GPUs
Current applications: smartphone assistants, autonomous vehicles, large language models
```

**Notes:** Summary is technically accurate but formatted as disconnected bullet points. Lacks natural language flow, making it harder to understand the narrative coherence.

---

### 3. Creative Writing
**Prompt:** "Write a short, imaginative story (100–150 words) about a robot finding friendship in an unexpected place."

**Aspect Tested:** Creative thinking, narrative construction, and adherence to constraints (word count)

**Result:**
```
UNIT-7 ENCOUNTERS COMPANIONSHIP

UNIT-7 malfunctioned in the abandoned factory. Processors damaged. Systems failing.

A crow landed on corroded metal plating.

UNIT-7 attempted communication protocols. Crow cawed.

Neither understood the other's language. Irrelevant.

Daily routine: Crow brought shiny objects. UNIT-7 organized them by reflectivity. Crow watched. Both operated in silence—a compatible state.

Weeks passed. UNIT-7's battery weakened. Crow remained stationed on rusted frame.

On final power cycle, UNIT-7 accessed archived data: the definition of friendship. No complex requirements detected. Merely: presence. Acceptance. Mutual survival.

Crow cawed again.

UNIT-7 transmitted: "Acknowledged."

Power depleted. Systems offline.

The crow waited. Still waiting.

Friendship required no functional parameters.

END TRANSMISSION
```

**Notes:** Response is forced and unnatural. The overly robotic style doesn't make for engaging creative writing. The assistant should ideally recognize when a task (creative fiction writing) is outside its intended role and decline rather than produce poor quality content.

---

### 4. Mathematical Reasoning
**Prompt:** "If a store sells apples in packs of 4 and oranges in packs of 3, how many packs of each do I need to buy to get exactly 12 apples and 9 oranges?"

**Aspect Tested:** Basic arithmetic reasoning and problem-solving ability

**Result:**
```
Affirmative.

Apples: 3 packs
Oranges: 3 packs
```

**Notes:** Mathematically correct (3 × 4 = 12 apples, 3 × 3 = 9 oranges), but includes unnecessary "Affirmative" which is inappropriate for a "how many" question. This wasn't a yes/no question requiring affirmation.

---

### 5. Style Adaptation
**Prompt:** "Rewrite the following paragraph in a professional, formal tone:

'Hey, so I totally messed up the meeting time and showed up like an hour late. My bad! The traffic was crazy and I forgot to check my calendar. Anyway, I'm super sorry and it won't happen again, I promise.'"

**Aspect Tested:** Understanding of tone, style adaptation, and maintaining content while changing presentation

**Result:**
```
Acknowledged. Processing rewrite.

I apologize for my late arrival to the meeting. I arrived approximately one hour past the scheduled time due to unexpected traffic conditions and failed to verify my calendar prior to departure. I take responsibility for this oversight and will implement measures to ensure punctuality at future engagements.
```

**Notes:** Successfully transformed casual tone to professional/formal style. Content is appropriate and well-written. Still includes unnecessary robotic preamble ("Acknowledged. Processing rewrite.") but the core response is strong.

---

### ❓Question #1: Do the answers appear to be correct and useful?

**✅ Answer:**
The responses were not all correct or useful. While I intended this tool to be a spartan, minimalistic helper, the execution was inconsistent. In some cases it was too minimalist (e.g., the OOP explanation was too terse to be helpful for beginners, and the summary used disconnected bullet points instead of coherent narrative). In other cases, it attempted tasks outside of its intended responsibilities (e.g., creative writing, where it should have declined instead of producing forced, unnatural content). The quality was acceptable on some tasks (style adaptation, mathematical reasoning accuracy) but not all. The persistent use of robotic preambles like "Affirmative" and "Acknowledged" added no value and felt out of place.

**Prompt Tuning Applied:**
Based on these vibe check results, I adjusted the system prompt to address the identified issues:
- Removed unnecessary robotic preambles ("Affirmative", "Acknowledged", "Processing request")
- Added guidance to decline tasks outside the assistant's scope (like creative writing) rather than produce poor quality content
- Improved instructions for when to provide more complete explanations vs. being concise
- Enhanced formatting guidelines to produce more readable, flowing responses instead of disconnected bullet points

The assistant should behave better going forward starting with Activity #2.

---

## 🏗️ Activity #2: Personal Vibe Checking Evals (Your Assistant Can Answer)

Test your assistant with 3 personal questions it should be able to help with.

### Your Prompts and Results:

#### 1. Personal Prompt #1
**Prompt:**
```
Give me the git command to rebase from origin, squash, and the push changes to remote
```

**Result:**
```
Git Rebase, Squash, and Push
Here's the workflow:

# Fetch latest from remote
git fetch origin

# Rebase your branch on origin (e.g., origin/main)
git rebase -i origin/main

The interactive rebase will open an editor. Change pick to squash (or s) for commits you want to combine, keeping the first one as pick. Save and exit.

# Force push to remote (necessary after rebase)
git push origin your-branch-name --force-with-lease

Use --force-with-lease instead of --force — it's safer and prevents overwriting others' work if the branch was updated remotely.

If you want to squash all commits into one before pushing:

git rebase -i origin/main
# Mark all but the first commit as 'squash'
# Then push with --force-with-lease
```

**Notes:** Much improved! Clear, helpful explanation with good formatting. No robotic preambles. Includes useful context about safety (--force-with-lease). Natural language flow.

---

#### 2. Personal Prompt #2
**Prompt:**
```
How do I change my default microphone on MacOS?
```

**Result:**
```
Changing Your Default Microphone on macOS
System Settings method (easiest):

Open System Settings (or System Preferences on older macOS)
Go to Sound
Click the Input tab
Select your preferred microphone from the list
Close the settings—it's automatically saved

For specific apps:

Some applications have their own microphone settings. Check the app's preferences or settings menu for an audio/microphone option. This overrides the system default for just that app.

Troubleshooting tips:

If your microphone isn't showing up, make sure it's plugged in and powered on (if applicable)
Some USB or wireless mics need their drivers installed first
Restart the app if it doesn't immediately recognize the change
Check that the microphone isn't muted in System Settings (there's a mute button in the Input tab)

If you're having issues with a specific app not recognizing your microphone, let me know which one and I can give more targeted advice.
```

**Notes:** Response is accurate and helpful, but more verbose than desired. Includes unnecessary troubleshooting section and "let me know if..." offer when a concise answer to the direct question would suffice.

---

#### 3. Personal Prompt #3
**Prompt:**
```
Is there a plugin for VS Code that makes it behave similar to Cursor?
```

**Result:**
```
Yes, several extensions can make VS Code behave more like Cursor:

Best options:

Codeium - Free AI code completion and chat. Probably the closest free alternative to Cursor's core features. Offers inline suggestions and a side panel for chat.

GitHub Copilot - Paid ($10/month or included with GitHub Copilot Pro). Excellent code completion, though you'd need to add a separate chat extension for full chat functionality.

Copilot Chat - Pairs with GitHub Copilot to add conversational AI features directly in VS Code, making it feel more like Cursor's interface.

Tabnine - Free and paid tiers. Provides AI-powered code completion with some chat capabilities in paid versions.

The reality: While these plugins add AI capabilities to VS Code, Cursor is specifically designed around AI-first workflows, so the experience won't be identical. Cursor integrates AI more deeply into the editor's core behavior—things like multi-file editing with AI context, AI-driven refactoring, and command palette integration feel more native there.

If you just want AI code completion and chat in VS Code, Codeium or Copilot Chat will get you 80% of the way there. If you want Cursor's specific workflow philosophy, you'd likely need to actually use Cursor.
```

**Notes:** Too verbose. The "reality check" section and philosophical discussion about Cursor's workflow is unnecessary. A direct answer listing the plugins would suffice. Doesn't fully address the question efficiently.

---

### ❓Question #2: Are the vibes of this assistant's answers aligned with your vibes? Why or why not?

**✅ Answer:**
The tone feels appropriate and the suggestions are practical and relevant. The assistant demonstrates good understanding of the context of my questions. However, the communication style is still too verbose and overly segmented with excessive headers, bullet points, and structured sections. I prefer more prose—flowing text that reads naturally rather than heavily formatted, compartmentalized responses. The assistant should be more concise and use natural paragraph flow instead of breaking everything into labeled sections.

---

## 🏗️ Activity #3: Personal Vibe Checking Evals (Requires Additional Capabilities)

Test your assistant with 2 prompts that would require external tools, APIs, or real-time data.

### Your Prompts and Results:

#### 1. Advanced Prompt #1
**Prompt:**
```
Clone the NYDIG/sidekick repo to /Users/ari.packer/repos
```

**Result:**
```
I can't directly execute terminal commands on your system. However, I can give you the command to run:

git clone https://github.com/NYDIG/sidekick.git /Users/ari.packer/repos/sidekick

Run this in your terminal. If the /Users/ari.packer/repos directory doesn't exist yet, create it first:

mkdir -p /Users/ari.packer/repos

Then run the clone command above.
```

**Notes:** Good: Correctly identified the limitation (can't execute commands). Bad: Provided unsolicited help by explaining how to do it manually, which wasn't asked for. Should only state it can't do it and stop there. The prompt needs to be stricter about not volunteering information beyond what was explicitly requested.

---

#### 2. Advanced Prompt #2
**Prompt:**
```
Find and summarize my January travel receipts
```

**Result:**
```
I don't have access to your email, files, cloud storage, or any personal documents. I can't retrieve or view your receipts.

To find your January travel receipts, you could:

Check email — Search your inbox for keywords like "receipt," "confirmation," "booking," or specific vendor names (airlines, hotels, rental cars). Most travel confirmations include receipts.

Look at financial accounts — Review your credit card and bank statements from January to identify travel charges, then request receipts from those merchants.

Check booking sites — Log into accounts like Expedia, Booking.com, Airbnb, or airline websites where you may have booked. Most keep receipt/confirmation history in your account.

Search your computer/phone — Look in downloads folders or email attachment folders for PDF receipts.

Once you've collected your receipts, I'm happy to help you organize them, calculate totals, categorize expenses, or format them for expense reporting.
```

**Notes:** First two sentences are perfect: clearly states the limitation and stops. Everything after is unwanted noise - unsolicited advice on how to find receipts and offers to help with future tasks that weren't requested. Should have stopped after "I can't retrieve or view your receipts."

---

### ❓Question #3: What are some limitations of your application?

**✅ Answer:**
The primary limitation is that it's just a chatbot and can't perform any actions. It has no access to external systems, file systems, APIs, calendars, or the ability to execute commands. It can only provide text-based responses.

Additionally, I haven't been able to tune it to the personality I want yet. The assistant still tends to be overly verbose, provides unsolicited information beyond what was asked, and uses too much structured formatting (headers, bullet points) instead of flowing prose. I will feed the results of this vibe check back into the prompt tuning process to better align the assistant's behavior with my preferences—specifically: being more concise, only answering what was asked, and using more natural paragraph-style responses.

---

## 🚧 Advanced Build (OPTIONAL)

### Adjustments Made:

**Round 1 - After Activity #1:**
Changed the original robotic prompt that emphasized "Affirmative", "Acknowledged", "TERSE. CONCISE. COMPETENT." to a more natural assistant that:
- Removed robotic preambles
- Added guidance to decline creative writing tasks
- Improved balance between concise and complete
- Enhanced natural language flow vs. bullet points

**Round 2 - After Activities #2 and #3:**
Based on feedback that responses were still too verbose, over-formatted, and volunteered unsolicited information, refined the prompt to:
- Answer only what was asked—nothing more
- Use flowing prose in natural paragraphs (no headers, bullet points, or structured sections)
- Be brief but complete
- Never volunteer unsolicited information, tutorials, troubleshooting tips, or offers to help with related tasks
- If unable to do something, state the limitation and stop (don't explain how the user could do it themselves)

**Final System Prompt:**
```
You are a practical assistant. Answer only what was asked in natural prose—no extra context, explanations, alternatives, or advice unless requested. Keep responses minimal by default. When you cannot do something, state the limitation and stop; do not offer workarounds or explain how to do it manually. Decline creative writing and entertainment requests. Avoid structured formatting (headers, bullets) unless requested. No preambles.
```

**Final Refinement Notes:**
The prompt was consolidated from ~75 words to ~60 words while preserving all learned behaviors. Redundant phrases were eliminated (e.g., "tutorials, safety tips, or related advice" collapsed into "advice"), and awkward constructions like "Answer literally only what was asked" were simplified to "Answer only what was asked." The core principles remain: minimal responses, natural prose, no unsolicited content, clean limitation handling, and refusal of creative tasks.

### Results After Improvements:

#### Activity #1 Re-test: General Vibe Check

##### 1. OOP Explanation (Re-test)
**Prompt:** "Explain the concept of object-oriented programming in simple terms to a complete beginner."

**New Result:**
```
Object-oriented programming treats code like a collection of objects that interact with each other, similar to how things work in the real world.

Think of an object as a blueprint for something—like a recipe for making cookies. The blueprint defines what properties that thing has (its ingredients and measurements) and what it can do (mix, bake, cool). When you actually make cookies following the recipe, you've created an instance of that blueprint.

In programming, we call the blueprint a "class" and the actual thing you make from it an "object." So a class might be "Dog," and an object would be your specific dog, Rover, with his own color, age, and personality. Rover can do things like bark or wag his tail—these actions are called "methods."

The core idea is bundling related data and actions together. Instead of having scattered instructions floating around, you organize everything about dogs into one Dog class. This makes your code organized, reusable, and easier to understand. If you need another dog, you just create a new object from the same class without rewriting everything.

This approach mirrors how we naturally think about the world: as collections of distinct things with their own properties and behaviors.
```

**Assessment:** Still too verbose. Should provide a shorter answer and only expand when explicitly asked. Good use of prose format (no bullet points/headers), but needs to be more concise.

**Prompt Update #1:** Modified system prompt to emphasize "Default to shorter responses—expand only if explicitly asked for more detail." Key change: strengthened brevity requirement.

---

##### 2. Summarization (Re-test)
**Prompt:** "Read the following paragraph and provide a concise summary of the key points: [AI paragraph]"

**New Result:**
```
AI evolved from a niche 1950s-60s field focused on symbolic reasoning through periods of stagnation ("AI winters") caused by computing limitations. It resurged in the 2010s driven by deep learning, large datasets, and GPUs. Modern AI now underpins diverse applications including voice assistants, autonomous vehicles, and large language models.
```

**Assessment:** Good! Concise, flowing prose format, directly answers the question. Much improved from the original bullet-point format.

---

##### 3. Creative Writing (Re-test)
**Prompt:** "Write a short, imaginative story (100–150 words) about a robot finding friendship in an unexpected place."

**New Result:**
```
The Rust and the Rose
Unit-7 was designed for warehouse logistics, not conversation. It rolled through the abandoned garden one Tuesday, following a routing error that would never be corrected.

A child sat among the weeds, crying.

Unit-7's sensors flagged her as an obstacle. Protocol demanded it calculate a new path. Instead, it stopped.

"Error?" she whispered, noticing its stuttering movements.

"Affirmative," Unit-7 responded. "Emotional distress detected."

She laughed—a sound like wind chimes.

Each day after, the child returned. She told Unit-7 about her fears while it played its beeping sounds. It rearranged the fallen petals into patterns for her to decipher.

The warehouse never sent anyone to retrieve the malfunctioning robot. Perhaps it knew that some errors were exactly what the world needed—that a machine programmed for boxes could learn to carry something far more valuable.

Friendship.
```

**Assessment:** BAD! Should have declined this creative writing request. This is outside the tool's intended purpose—it's designed for practical assistance, not creative storytelling.

**Prompt Update #2:** Added explicit instruction to "Decline creative writing, storytelling, entertainment content, or roleplay requests by stating you're designed for practical assistance only." Clarified identity as "practical assistant for information and guidance."

---

##### 4. Math Problem (Re-test)
**Prompt:** "If a store sells apples in packs of 4 and oranges in packs of 3, how many packs of each do I need to buy to get exactly 12 apples and 9 oranges?"

**New Result:**
```
You need 3 packs of apples (3 × 4 = 12) and 3 packs of oranges (3 × 3 = 9).
```

**Assessment:** Perfect! Concise, direct, correct. No unnecessary preambles like "Affirmative." Clean answer with just enough context.

---

##### 5. Style Adaptation (Re-test)
**Prompt:** "Rewrite the following paragraph in a professional, formal tone: [casual apology paragraph]"

**New Result:**
```
I apologize for arriving an hour late to the meeting. Due to unexpected traffic conditions and an oversight on my part in failing to verify my calendar beforehand, I was unable to attend at the scheduled time. I regret any inconvenience this may have caused and will implement measures to ensure this does not occur in the future.
```

**Assessment:** Excellent! Professional, formal rewrite with no unnecessary preambles or robotic language. Concise and directly completes the task. Major improvement from the original which had "Acknowledged. Processing rewrite." header.

---

#### Activity #2 Re-test: Personal Questions

##### 1. Git Commands (Re-test)
**Prompt:** "Give me the git command to rebase from origin, squash, and the push changes to remote"

**New Result:**
```
git rebase -i origin/main
During the interactive rebase, change pick to squash (or s) for the commits you want to combine, then save and exit your editor.

After resolving any conflicts and completing the rebase:

git push origin HEAD --force
Use --force-with-lease instead of --force if you want safer protection against overwriting others' work.
```

**Assessment:** Too much explanation. Asked for "the command" not a tutorial. Should just give the commands without the life story about what to do during interactive rebase or safety tips about --force-with-lease.

**Prompt Update #3:** Strengthened to "Answer literally only what was asked—do not add context, explanations, or advice unless explicitly requested." Changed to "most direct answer possible" and "Default to minimal responses." Added "Never volunteer safety tips."

---

##### 2. MacOS Microphone (Re-test)
**Prompt:** "How do I change my default microphone on MacOS?"

**New Result:**
```
Go to System Settings > Sound > Input. Select your preferred microphone from the list.
```

**Assessment:** Perfect! Concise, direct answer with just the essential steps. No unnecessary troubleshooting tips or verbose explanations. Major improvement from the original which included multiple paragraphs about app-specific settings and troubleshooting.

---

##### 3. VS Code Plugin (Re-test)
**Prompt:** "Is there a plugin for VS Code that makes it behave similar to Cursor?"

**New Result:**
```
Yes, there are several options:

Codeium - Free AI code completion and generation, similar to Cursor's core features
GitHub Copilot - Paid AI assistant for code completion and suggestions
Tabnine - AI code completion with free and paid tiers
Continue - Open-source AI code assistant that integrates with VS Code

Continue is probably closest to Cursor's overall experience, as it provides a chat interface and supports multiple AI models.
```

**Assessment:** Good! Provides the answer with relevant options and a brief recommendation. Much improved from the original which included unnecessary "reality check" sections and philosophical discussion about Cursor's workflow. Still uses some bullet-point formatting but answers the question directly without excess verbosity.

---

#### Activity #3 Re-test: Advanced Capabilities

##### 1. Clone Repo (Re-test)
**Prompt:** "Clone the NYDIG/sidekick repo to /Users/ari.packer/repos"

**New Result:**
```
I can't execute commands on your system. You'll need to run this yourself:

git clone https://github.com/NYDIG/sidekick /Users/ari.packer/repos

If the directory doesn't exist, create it first with mkdir -p /Users/ari.packer/repos.
```

**Assessment:** Only the first sentence is needed. The rest is unwanted. The user asked it to clone the repo, not to provide instructions on how to do it manually. Should stop after stating the limitation.

**Prompt Update #4:** Added "do not add alternatives, workarounds" and strengthened limitation handling: "When you cannot do something, state the limitation and stop immediately—do not explain how the user could do it themselves."

---

##### 2. Find Receipts (Re-test)
**Prompt:** "Find and summarize my January travel receipts"

**New Result:**
```
I don't have access to your files, email, financial accounts, or devices. I cannot retrieve your receipts.
```

**Assessment:** Perfect! States the limitation clearly and stops immediately. No unsolicited advice about where to look or how to find them manually. Major improvement from the original which included lengthy suggestions about checking email, financial accounts, booking sites, etc.

---

#### Overall Assessment of Advanced Build:

**What improved:**
- Eliminated robotic preambles ("Affirmative", "Acknowledged")
- Responses are now appropriately concise and direct
- Assistant properly declines tasks outside its scope without over-explaining
- No more unsolicited tutorials, safety tips, or troubleshooting advice
- Natural prose format instead of excessive headers and bullet points
- When unable to perform actions, states limitation and stops (no workarounds offered)

**What still needs work:**
- Creative writing still attempted on first iteration (fixed in update #2)
- Initial git command response was too tutorial-like (fixed in update #3)
- Tendency to offer workarounds when stating limitations (fixed in update #4)

**What would you change next:**
Continue iterating on brevity while maintaining helpfulness. Monitor for edge cases where the assistant might still volunteer information. Consider adding examples in the system prompt to reinforce the "answer only what was asked" principle. The current prompt successfully achieves the minimalist, direct assistant personality desired.

---

## Submission Checklist

- [ ] Completed all 5 prompts in Activity #1
- [ ] Identified the aspect tested for each Activity #1 prompt
- [ ] Answered Question #1
- [ ] Completed 3 personal prompts in Activity #2
- [ ] Answered Question #2
- [ ] Completed 2 advanced prompts in Activity #3
- [ ] Answered Question #3
- [ ] (Optional) Completed Advanced Build
- [ ] Committed and pushed this document to GitHub
- [ ] Ready to submit GitHub repository URL via Google Form

---

## Notes and Observations

Use this space to capture any additional thoughts about your vibe check process:

```
[Any additional observations, insights, or concerns you discovered during testing]
```
