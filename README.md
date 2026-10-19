# Public skills from APG

Guided question-and-answer setups that APG Software gives to the businesses it works with. They
run in your own Claude account. Nothing in this repository is about any one business.

| Type this | What it does | How long |
|---|---|---|
| **/business-walkthrough** | Your leadership team talks Claude through how the business runs. Claude draws it as you go so you can check it, and you keep the page at the end | About an hour, with Adam |

## Setup (once, about 5 minutes)

You need a paid Claude plan. Do this in the Claude account that will be on the screen on the day.

**Upload the skill**
1. Adam sends you `business-walkthrough.zip`. Don't unzip it.
2. Go to **claude.ai**, then **Customize**, then **Skills**, then **Upload a skill**, and choose the zip.
3. Switch it on.

**Then check two settings are on.** On a Team plan the **Owner** checks these in Organization
settings → Capabilities:
- **Code execution and file creation** (needed for the drawings and the file)
- **Web search** (so Claude can read your website)

**Using Claude Code instead?** Two lines:

```
/plugin marketplace add APG-Software/public-skills
/plugin install business-walkthrough@public-skills
```

## On the day

Adam sets up a Project called "How [your business] works" with a one-page starter sheet in it.
Open a new chat in that Project, type **/business-walkthrough** and send it. Talk using the
microphone button in the message box, or type. Rough answers are fine.

## What happens to my information?

The walkthrough runs in your own Claude account, and the page and the file stay there. Nothing is
sent to APG or anyone else unless you share the file. Adam records the meeting with your
agreement; anyone can say no. Never put passwords or bank details in the chat.
