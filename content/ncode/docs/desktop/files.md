---
title: Images, search and export
description: Attach screenshots and images to a message, search every conversation, find project files with ⌘P and export a conversation as Markdown.
---

## Attaching images

Show the model what you mean: paste a screenshot into the composer ([[⌘]]+[[V]]) or drag an image file onto the window.

- Accepted: PNG, JPEG, GIF and WebP.
- Up to 5 MB per image and 4 images per message.
- The images are saved as files in the `attachments` folder inside `{{data_dir}}` and sent to the model with the message. Use a model that accepts images.

## Searching every conversation

The search box at the top of the sidebar, [[⌘]]+[[K]], filters your conversations by title as you type. With three or more characters it also searches the text of every message in every conversation and shows the hits under **Message matches**, with a snippet. Click a hit to open that conversation.

![The sidebar search for “retry”: one conversation title matches, and a Message matches section shows two snippets.](/assets/shots/desktop/files-search.webp)

## Finding a file in the project

Press [[⌘]]+[[P]] and start typing part of a file name. The finder matches loosely (letters in order, not necessarily together), skips what `.gitignore` excludes and shows the best 50 hits. Use the arrow keys and [[Return]], or click, to open the file in the **Changes** view of the agents pane, where you can read it and edit it.

## Exporting a conversation

Open the conversation's header menu and choose **Export**. {{product}} saves the transcript as a readable Markdown file: your messages, the answers and the runs, in order.

<!-- source: D:lib/swarm_code/attachments.ex:1-28, D:lib/swarm_code/projects/workspace.ex:52-53, D:CHANGELOG.md:302-306,312-314, D:lib/swarm_code/settings.ex:98-110, D:lib/swarm_code_web/live/workspace_live.ex:3791-3830, D:lib/swarm_code_web/live/workspace_live/workspace.html.heex:680-700, D:lib/swarm_code_web/components/chat_header.ex:75-80 -->
