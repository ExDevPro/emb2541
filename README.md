Default Placeholder:
Make sure all the placeholder from default/ uploaded leads columns file (uppercase) or (lowercase) will detect automatically, there is no needed to use exact (uppercase) or (lowercase) charecter, tool must need to detect them automatically,eg:
{{campaign}} user can use directly this as placeholder or can use as {{CAMPAIGN}} or even {{Campaign}} all of these tool will detect automatically as {{campaign}}. like this others any placeholder too.

and give also add more button to add any placeholder name and their content with one per line and configurable for rotation with each placeholder.

-{{Counter}} = Incrementing number for each email sent, this sould be real counter so user can specify counter number with each email they send.
-{{FakerFirstName}}
-{{FakerLastName}}
-{{FakerFullName}}
-{{FakerGender}}
-{{FakerEmail}}
-{{FakerUsername}}
-{{FakerPassword}}
-{{FakerCompany}}
-{{FakerCompanySuffix}}
-{{FakerJobTitle}}
-{{FakerPhone}}
-{{FakerPhoneNumber}}
-{{FakerCity}}
-{{FakerState}}
-{{FakerCountry}}
-{{FakerCountryCode}}
-{{FakerAddress}}
-{{FakerStreetName}}
-{{FakerStreetAddress}}
-{{FakerBuildingNumber}}
-{{FakerPostcode}}
-{{FakerLatitude}}
-{{FakerLongitude}}
-{{FakerDate}}
-{{FakerTime}}
-{{FakerDateTime}}
-{{FakerDayOfWeek}}
-{{FakerMonthName}}
-{{FakerYear}}
-{{FakerUrl}}
-{{FakerUUID}} = this is faker generated  automatically uniqe for each receipients.
-{{FakerColor}}
-{{FakerHexColor}}
-{{FakerLocale}}
-{{FakerCurrencyCode}}
-{{FakerIBAN}}
-{{FakerBIC}}
-{{FakerBoolean}}
-{{FakerUserAgent}}
-{{FakerIPv4}}
-{{FakerIPv6}}
-{{FakerMACAddress}}
-{{FakerSlug}}
-{{FakerWord}}
-{{FakerWords}}
-{{FakerSentence}}
-{{FakerParagraph}}
-{{FakerText}}
-{{FakerRandomNumber}}
-{{FakerDigit}}
-{{FakerNumberBetween}}
-{{FakerTimezone}}
-{{FakerLanguageCode}}
-{{FakerAsciiSafeEmail}}
-{{FakerFreeEmail}}
-{{FakerSafeEmail}}
-{{sequence}}
-{{timestamp}} = current time.
-{{hash}} = give option also to use customization for (MD5? SHA256? random?). Must specify algorithm or even all user can edit as they needed.
-{{uuid}} = this is system-generated  automatically uniqe for each receipients.
-{{year}}
-{{month}}
-{{day}}
-{{hour}}
-{{minute}}
-{{second}}
-{{subject}} = current subject using to send email.
-{{email}} = receiver email, user can use also directly from uploaded leads file columns name as {email} both can be supported.
-{{user_id}} = unique receiver user id for each leads
-{{random}} = random number/words etc, user can specify the lenth or adjust from default placeholder config.
-{{ENCODED_URL}} = default as which link user want to track will auto generate based on email template link.
-{{token}} = unique token for each receipients/email/leads.
-{{date}} = current date.
-{{domain}} = option to input box with multiple domain, one domain per line, if use this placeholder it will rotate domain automatically duirng each time use this. user will add their own domain from default placeholder config settings, by default give as few example domain name.
-{{random_alphanum}} = option to set minimum/maximum lenth for alphanum
-{{batch}} = with one custom input box to input name or any uniqe content of batch one per line, user can add as many as needed to use later on header or anywhere.
-{{campaign}} = with one custom input box to input name of campaigns one per line, user can add as many as needed to use later on header or anywhere.
-{{custom_string}} = with one custom input box to input custom_string one per line, user can add as many as needed to use later on header or anywhere.
-{{list_name}} = with one custom input box to input list_name one per line, user can add as many as needed to use later on header or anywhere.
-{{unsubscribe}} = option to input box with one per line as bellow format:

<mailto:unsubscribe@yourdomain.com> = can use direct user specific domain.
<mailto:unsubscribe@{{domain}}> = can use any custom text instead of unsubscribe & default placeholder {{domain}} will automatic replace with picking domain randomly from this default domain placeholder.
<mailto:{{FakerFullName}}@yourdomain.com> = will filup automatically each time with faker full name@domain.com and send.
<mailto:{{FakerFullName}}@{{domain}}> = will filup automatically from faker full name and provided domain randomly.
<mailto:{{campaign}}@yourdomain.com> = will filup campaign name automatically from picking default provided campaign name.
<mailto:{{campaign}}@{{domain}}> = will filup them automatically.
<mailto:unsubscribe@yourdomain.com?{{subject}}=unsubscribe> = {{subject}} will replace with subject text which used to send this email.
<https://yourdomain.com/unsubscribe?email={email}> = email with filup automatically with receipients email.
<https://yourdomain.com/unsubscribe/{{token}}> = {{token}} will filup with uniqe token for each recepients.
<mailto:unsubscribe@yourdomain.com>, <https://yourdomain.com/unsubscribe/{{token}}> = will be both as single header.

like this way user can add/edit/delete/ customize as many as unsubscibe format need. and if use default placeholder {{unsubscribe}} the tool will automatically use randomly with each time with generate uniqe unsubscribe link/ mail to / both.



spinword/ spintext:
Spinword / Spintext Configuration Specification:
Spinword/Spintext will be a separate configuration section, where users can add as many spinwords/spintexts as needed.
There will be an “Add More” button to add a new entry.
Each entry includes:
A Main Word or Sentence input (e.g., struggling)
A corresponding Spintext Options input (e.g., struggling|having trouble|facing challenges|finding it hard)
The separator between variations will be the pipe symbol (|)

💡 Example:
If the user adds:
Main Word: struggling
Spintext Options: struggling|having trouble|facing challenges|finding it hard
The tool will randomly pick one of those options whenever the word {{{struggling}}} is used.

Usage in Message or Subject:
Users can use spintext anywhere in their subject, message body, or headers by wrapping the main word with triple curly braces:
{{{struggling}}} → Will randomly be replaced with one of the defined options.


Placeholder Syntax Summary:
Lead Column: {column_name} : Refers to any column from the uploaded leads file (e.g., {email})
Default Placeholder: {{placeholder}} : Refers to system or user-defined placeholders (e.g., {{uuid}}, {{domain}})
Spinword / Spintext: {{{word}}} : Refers to spinword entries from the spintext configuration (e.g., {{{offer}}})
The tool will automatically detect and replace these during sending based on the defined configurations and imported data.

Main Final Requirments:
Software Name: DeepMailer v1.0
Target OS: Windows 10/11 only
Programming Language: Python with  pyqt6 and design as qss file and option to change theme/qss file from settings so I can use multiple theme with crate qss file/code, for the GUI can show browser inside software so it give feel like not any external browser, and also can use any professional loading animation or gif after click any option or button so during switch an option to another option it will give better ui feel instead of showing blank anything or use something that work instant click for any option. As it will be computer software software so I don’t want to intregated any external database or such instead do all as json or whatever save state automatically.
I'll be protecting the entire tool — both GUI and core — using my full code protection setup. So it must be fully compatible with tools like Nuitka, Cython, or PyInstaller when compiling to .exe. After compilation, everything should work exactly the same as the original .py code — no broken buttons, no input fields failing, no random closing, freezing, or crashing issues. Same code I wish to use as python pyqt6 with qss as design .
I don’t want to use any emojis since this will be a fully commercial software. Wherever icons are needed (like for buttons or menus), I’ll use external .svg or .png images. No hardcoding paths either — I want one clean JSON file where I’ll define all image paths, like this:
ProjectDirectory/Data/images/logo.ico (for the tool icon).
Each icon or image must have a unique file name, and I want a documentation file that clearly explains each one — file name, path, where it’s used, and even its size.
The software must use background threads for every feature or option. Each task should run on its own thread to avoid the UI freezing, getting slow, or becoming unresponsive.
It should also support running multiple campaigns at the same time — each campaign with its own background thread, so they don’t interfere with each other. You should be able to start, stop, pause, or resume any campaign without affecting the others.
Everything the user does — editing, saving, updating status — must be stored instantly in real-time. No chance of losing any data, ever.
Right now I don’t need any email tracking feature. I might add that later. Also, in the future I’ll build a SaaS version of this same software for web use with multi-user support. So from now, the code structure should be clean — core logic separated from GUI code — so I can later drop the GUI and plug in a frontend easily. For now though, I don’t need any frontend for web, just focusing on the Windows desktop version with full multithread and multi-campaign support.
File Structure Plan:
All data saved by the user will be stored under the ProjectDirectory/Data/ folder like this:
•	Leads/ → Uploaded or edited lead data
•	SMTP/ → User-added SMTPs
•	Subject/ → Added or edited subject lines
•	Message/TemplateName/ → User’s message templates
•	Campaigns/CampaignName/ → Data for each campaign
•	Campaigns/CampaignName/Reports/ → Sending logs for that campaign
•	Settings/ → All app settings
•	Logs/ → Error logs or runtime logs
Resource Structure:
All themes, images, and fonts will be placed like this:
•	Resource/Images/logo.ico → Main tool icon (and other icons follow this pattern)
•	Resource/Theme/Theme1.qss → UI themes (switchable from settings)
•	Resource/Fonts/fonts.ttf → Fonts used in the app (users can change them from settings)


Full software must be automatically responsive based on any screen size, and have to use proper placement, alignment, sizing, etc., in a professional way. You have to think and understand properly, like a professional, which option needs how much space and where to place it for better UI. Also, you must keep all options clean and separated from each other — like, suppose on the left side we added one option to set the maximum limit, and on the right side of that, a small input box is placed where the user can put the value. Just like that, everything needs to be designed professionally.
The application layout will be something like this:
Main left-side panel:
•	Dashboard
•	Leads
•	SMTPs
•	Subject
•	Messages
•	Campaigns
•	Configurations
•	Settings

And on the right side of each selected menu, another panel will show the related data in table view (like Excel style).
Dashboard: This will be the default selected panel after opening the software. The right panel will show all counters and stats that I already mentioned.
Leads: If the user clicks on Leads, the right panel will show some buttons like Create / Edit / Delete.
If the user clicks Create, a small popup/window will open where they can enter a name and an optional short description for the leads list. After clicking OK/Cancel, the tool will instantly create a CSV file inside:
ProjectDirectory/Data/Leads/

Example:
If the list name is Test List, then it will create:
ProjectDirectory/Data/Leads/Test List.csv

Once the list is selected, the right panel will show it in a table format. By default, only one column will be there — Email — which is required for sending. If the column name is lowercase like email, the tool must detect that automatically. Any extra columns from the uploaded file will also show exactly as they are in the UI. If the user uploads a .txt file, the tool will treat the first line as header/column names, and use colon (:) as separator — like:
Name:Email:Address
On the right panel, some more buttons will be available:
•	Import: Opens file picker to import leads from CSV/Excel/Text — no matter what file the user selects, the tool will convert and store it in the created .csv file with the same list name instantly.
•	Export: User can export the data anytime as CSV/Excel/Text. If exporting as text, the first line will be added as header using colon as separator, and the rest of the data will follow the same format.
•	+ Header: If the user clicks this, a new window will open with an “Add More” button and input box for name. This allows adding custom column names manually, one by one, with OK/Cancel. These will update the CSV file header and appear in the UI too.
•	+ Manually: When clicked, a window opens showing current headers in a dropdown, and input boxes to add data for each column. The user can fill any or all fields, and leave some blank if they want. Clicking OK will add that data as a new row in the UI and store it in the CSV file.
•	+ Merge: On clicking this, a new window will open with the option to import another leads file (CSV/Text/Excel). It will show all current column names on the left and the imported file's column names on the right. The user can map them using dropdowns — like match Email to email, Name to First Name, etc. After that, clicking OK will merge the new data with the existing file.
•	For example:
Current leads = 100
Imported merge leads  as = 50
→ Final total = 150 leads in the same list
•	Also, give full flexibility to edit, resize, delete, insert new rows directly in the UI. Right-click on any row should open a context menu with more options like Delete Row, Insert New Row Below, etc., just like other professional tools.

Smart Duplicate Detection
After importing or manually adding leads, automatically check for duplicates in the Email column and prompt the user with options:
•	Keep all
•	Remove duplicates
•	Merge rows (if extra fields differ)
You can even show how many duplicates were found before confirming import or merge.

Inline Cell Editing
Allow inline editing directly inside the table from ui just double-click a cell to edit the value and auto-save instantly after finished editing.
This will make it faster to fix typos or update entries.

Bulk Edit & Delete
Support selecting multiple rows (via row highlighting ), then offer:
•	Bulk delete
•	Bulk export
•	Copy/Paste

Column Type Detection automatically
Try to detect if columns contain special data (e.g., phone numbers, dates, countries), and show small icons next to header labels (e.g., 📞, 📧, 🗓️). This is optional, but adds polish.

Real-time Row Count, Valid/Invalid Stats
Show live stats like:
•	Total Rows: 150
•	Valid Emails: 140
•	Invalid Emails: 10
You can validate email format during import or show errors as inline badges.

Search/Filter Bar
Add a simple search box above the table to let users filter leads by Email, Name, or any column — especially useful when working with large lists.

Pagination 
If the user adds 100 millions+ Email Leads data, loading all in a single table might slow down the UI.
Add pagination (e.g., 100/500/1000 per page)— this will keep the UI fast.



- SMTPs:
If the user clicks on SMTPs, the right side panel will show all the data in a table view format with the following default column names:
•	Server Name
•	Short Description
•	SMTP Host
•	SMTP Port
•	Username / Email
•	From Email
•	SMTP Added Date
•	Last Update Date
•	Status
If there are already any SMTPs saved, those will be shown in this table with their data.
For each SMTP, there will be 2 quick options shown directly in the UI:
•	Test SMTP → to check if this SMTP is active or not
•	Details → if user clicks on this, a new popup window will open and show all the configuration/data in full table view properly. This includes everything that was set when the SMTP was added.
Inside the Details popup:
•	Show all fields in table format
•	Make the UI professional with horizontal scroll buttons — so if data is too long, user can press and hold the mouse and scroll left/right easily to view hidden content
There will also be buttons like:
•	Add SMTP Server → to open the form for adding a new SMTP
•	Edit Server → to edit any selected SMTP (loads all fields same as during SMTP creation, user can edit any part needed)
•	Test SMTP → user can select one row or multiple rows, and click this button
o	If one SMTP selected → test only that
o	If multiple/all selected → test all of them automatically
o	If any server fails during test, the full row will be highlighted in red, and the reason for failure will be shown clearly
o	All successful SMTPs will also be shown as "Passed"
•	Delete → user can select one or more SMTPs and click delete. The tool will directly delete the corresponding .json file that contains that SMTP's configuration/details.

Below is the full list of all column names that will be shown with their data in the full view table:
-Server Name (Used as filename)
-Short Description (optional)
-SMTP Host
-SMTP Port
-Authentication Method (Options: Auto, PLAIN, LOGIN, CRAM-MD5)
-Security Type (Options: Auto, None, SSL, TLS)
-Username / Email
-SMTP Password
-From Email
-From Name (optional)
-From Name Header Option (Enable/Disable)
-From Name Header Mode (Custom/Faker)
-Custom From Names (if Custom is selected)
-Faker From Settings (auto-generated if Faker is selected)
-From Name Rotation Type:
Each time
After X to Y sends

-From Name Rotation Range (From/To) (if applicable)
-From Name Header Use Policy
Must Use (default)
Random
Random Header Usage From
Random Header Usage To
-Reply-To Email (optional)
-Reply-To Header Option (Enable/Disable)
-Reply-To Header Mode (Custom/Faker)
-Custom Reply-To Emails (if Custom is selected)
-Faker Domains for Reply-To (one per line, if Faker is selected)
-Reply-To Rotation Type:
Each time
After X to Y sends

-Reply-To Rotation Range (From/To)
-Reply-To Header Use Policy
Must Use (default)
Random
Random Reply-To Usage From
Random Reply-To Usage To

-Proxy Enabled (Enable/Disable)
-Proxy IP/Host
-Proxy Port
-Proxy Type (HTTP/HTTPS/SOCKS5)
-Proxy Requires Authentication (Yes/No)
-Proxy Username (if auth enabled)
-Proxy Password (if auth enabled)
-SMTP Host for Proxy Test
-Proxy Fallback Option
Stop using SMTP
Fallback to system default (no proxy)

-Multiple Proxies List (rotate if more than one added)
-Limit Control Enabled (Enable/Disable)
-Limit Type (Per Minute, Hourly, Daily, Weekly, Monthly)
Limit Value (X per unit time)
Total Limit (0 = Unlimited)

-Used Count
-Reset Limit Triggered? (Yes/No, for reset button)
-SMTP Status (Active/Inactive)
-Deactivation Reason (e.g., Limit Reached)
-Added Timestamp (Date, Time, Seconds)
-SMTP Test Result (Success/Failure)

Add SMTPs Server Process:
Pagination 
If the user adds 100+ SMTPs, loading all in a single table might slow down the UI.
Add pagination (e.g., 10/25/50 per page)— this will keep the UI fast.and give this default settings configuration option on this “Configurations” panel so user can adjust this based on need.

Column Filtering / Search
Sometimes users might want to find an SMTP quickly.
Add a small search box above the table, with support for filtering by Server Name, Host, or Status.


Tag or Category Field (Optional)
If a user has 50 SMTPs from different providers (e.g., Zoho, Gmail, custom), it might be helpful to group them.
Add a Tag or Category field (optional), with a dropdown to filter/sort by tags later.



When a new SMTP list is created, the system will automatically generate a file with the same name as the list.
Once a list is selected, the right-hand side panel will display all SMTPs in that list in a table view format.

a dedicated button will be added: ➕ Add SMTP Server (with a professional placeholder style and clear visibility).

SMTP Storage Format: Each SMTP server's full configuration will be saved as a JSON file. The file will be saved under the folder "ProjectDirectory/Data/SMTP/Server Name.json"

Add SMTP Server Window:
When clicking "Add SMTP Server", a new window will appear with the following fields:

SMTP Server Details:
Server Name: User-defined name to help identify the SMTP easily in the UI. (Used as filename when saving)


Short Description (Optional): A short note or label the user can enter to describe or tag the SMTP for future reference.


SMTP Connection Details:
SMTP Host: Input field for the SMTP hostname or IP address.

SMTP Port: Input field for the SMTP port. Supports all standard ports (465, 587, 25, 2525, etc.).

Authentication Method: Dropdown options: Auto, PLAIN, LOGIN, CRAM-MD5

Security Type: Dropdown options: Auto, None, SSL, TLS

Credentials:
Username / Email: Input field for the SMTP username or email address.
SMTP Password: input field for the SMTP password.

From Email:
From Email: Input field to specify the sender's email address to be used as the "From" email when sending.


From Name (Optional): This is an input box where the user can enter a From Name. It's optional — if the user doesn’t input anything, it’ll just use the SMTP’s default From Name.

Header Option:
There’s a dropdown with options: Enable and Disable (default is Disable)  (will be also an edit icon/button to edit/reconfigure this option configuration again in later)..
If the user selects Enable, a new window will pop up with two choices: Custom and Faker.

If Custom is selected:
An input box appears where the user can enter one or multiple custom From Names.
If multiple names are entered, the tool will rotate them based on the rotation settings (i’ll explain that next).

If Faker is selected:
The input box is disabled — the user can’t type anything.
Instead, the tool will auto-generate unique From Names with Faker (if one will genrate only one and will use this if do rotation it for each email / others will generate uniqe name for each time use or whatever user configure on rotation settings).
It’ll rotate these names automatically based on the rotation settings, so each send has a new one or same based on rotation settings.


Rotation Settings for From Name:
There’s a label (placeholder-style): “How do you want to rotate the From Name?”

The user gets a dropdown with two options:
Each time – means the From Name changes with every single time use this smtp to send email.
Rotate after specific number of sends – lets the user define a range like “after X to Y emails”, and the tool will rotate From Names within that pattern.
This applies whether the names are custom or auto-generated by Faker.


Header Use Policy:
Another dropdown labeled “Header Use Policy” with the following options:
1. Must Use (Default):
This means every time the tool uses this SMTP, it will must need to use this provided header configurations.

2. Random:
If this is selected, two input boxes appear: "From" and "To".
The user can define a range like: From 10 To 20.
Use the header for 12 emails, Then automaatically skip using the header for 20 emails.
Then use it again for another random number between that range — and so on.
This way, the pattern of using the From Name header becomes random and less predictable — making it much harder for filters to detect, and improving inbox placement.


Reply to (Optional): This is an input box where the user can enter a Reply-To email address.
It’s optional — if the user doesn’t enter anything, the tool will use the SMTP’s default Reply-To email.

Header Option:
There’s a dropdown with two options: Enable and Disable (default is Disable)  (will be also an edit icon/button to edit/reconfigure this option configuration again in later)..
If the user selects Enable, a new window opens with two choices in dropdown: Custom and Faker.

If Custom is selected:
An input box appears where the user can input one or multiple custom Reply-To email addresses.
If multiple emails are provided, the tool will rotate them based on the selected rotation settings, if single will use this always.


If Faker is selected:
The custom input box is disabled (non-editable).
A new input field appears to input domain names (one per line).
The tool will then automatically generate unique Reply-To email addresses using the given domain(s) automatically during use this smtp each time..
These Faker Reply-To addresses will be rotated each time the SMTP is used, based on the rotation settings.



Rotation Settings:
A dropdown with label like: “How do you want to rotate the Reply-To address?”
Options:
Rotate each time – rotate the Reply-To email every time an email is sent.
Rotate after X to X emails – define a range (e.g., From 10 to 20) so the Reply-To email rotates randomly within that range of sent messages.


Example:
If set to “From 10” and “To 20,” the same Reply-To will be used for 10 to 20 emails, then it rotates to the next one, and so on.


Header Use Policy:
This controls how often the Reply-To header is applied when sending emails/using this smtp each time.

Dropdown Options:
1. Must Use (Default):
The Reply-To header will be must applied every time this SMTP is used — either from custom input or Faker-generated addresses.

2. Random:
If this is selected, two input boxes appear: "From" and "To".
The tool will randomly apply the Reply-To header for a number of emails between the defined "From" and "To" range,
Then skip using the header for the next range of emails, Then apply again — repeating this cycle.

Example:
If set to use the header for from 10 and to 15.
tool will automatically Use the header for 12 emails,
Then automatically skip for 15 (use smtp default Reply-To mail/no Reply-To),
Then use again for 11, skip for 14, and so on.

This random rotation helps avoid detection and improves inbox placement.



Proxy (Optional):
Dropdown with options: Enable / Disable (default is Disable) (will be also an edit icon/button to edit/reconfigure this option configuration again in later).
If the user selects Enable, another window will be opens with the option to manually add proxy details using the "Add Proxy" button.

Add Proxy Fields:
When adding a proxy, the following fields are required:
IP/Host: Input field to enter the IP address or hostname of the proxy.
Port: Input field to specify the proxy port.
Proxy Type: Dropdown with options: HTTP, HTTPS, SOCKS5 — user selects the type.
Authentication: A checkbox (default is unchecked). If enabled:
Username: Input field for proxy username.
Password: Input field for proxy password.
SMTP Host: Input field where the user enters the SMTP host. This is used for testing whether the proxy can connect to the SMTP server.

Test Button:
After entering proxy details, the user can click "Test" to check if the proxy can connect to the provided SMTP host.
The tool will use the entered proxy settings to test reachability.
Result will show either Success or Failed.


Multiple Proxies Support:
The user can add one or multiple proxies to use with this SMTP.
If multiple proxies are added, the tool will automatically rotate between them each time the SMTP is used.

Mandatory Proxy Use (When Enabled):
Once proxy is enabled for the SMTP, the tool must use a proxy every time this SMTP is used for sending.
If a proxy connection fails, the behavior will depend on the selected Fallback Option (see below).
Fallback Option (If Proxy Fails):
Dropdown options:
Stop using this SMTP – SMTP will no longer be used if smtp failed to connect with proxy or proxy is dead.
Fallback to system default (no proxy) – SMTP will continue using system network with no proxy if proxy fails.

User can choose either behavior from this dropdown based on their use case.

Button for save/cancel
Save – Saves the proxy configuration and returns to the previous window.
Cancel – Cancels the setup and returns without saving.


Limit Control (Optional):

If the user wishes, they can enable limit control for the SMTP. If no limit is set, the server can be used for unlimited campaigns and can send unlimited emails without any restriction.

There will be a dropdown with "Disable/Enable" Disable as the default option. An edit icon/button will also be available to reconfigure or modify the limit settings later if needed. Additionally, a "Reset Limit" button will be present — this will be non-clickable unless any limit has been used. If limits have been used, the button becomes clickable. When clicked, it will reset the usage count back to 00, while keeping the original total limit & others configuration unchanged. For example: if the total limit was set to 100 and 50 has already been used, clicking this button will reset the used count back to 0, but the total limit will remain as 100.

if user select as Enable will open another window with again dropdown option as:
Per Minutes
Hourly
Daily
Weekly
Monthly

user can selects any of these options from the dropdown, 

For example, if the user selects "Per Minutes", a option will be appear with an input box to set the value X per minute. This means the tool will not use the SMTP more than X times per minute. eg: If the user inputs 10, the tool will make sure this SMTP is not used more than 10 times per minute.

Another input box will allow the user to set a "Total X Limit", meaning how many times the SMTP can be used in total. The default value is 0, which means unlimited. If a total limit is set, for example 100, once that limit is reached, the tool will stop using the SMTP and mark its status in the smtp table view options.
SMTP Status: Inactive
Reason: Limit Reached
The user can then manually reset the limit if needed.

The same logic applies to Hourly, Daily, Weekly, and Monthly — user can select any of these and can set limit based on user need. The tool will automatically store all limit settings as a JSON file linked to each SMTP, and it will also track and store /update the SMTP’s added date, time, and second, in precise detail, to maintain proper timing and calculations internally.

Hourly = 60 minutes (1 hour)
Daily = 24 hours (1 day)
Weekly = 7 days (1 week)
Monthly = 30 days (1 month)

A Save/Cancel button will be available to return to the previous screen.

After completing all the configuration for this specific SMTP, there will be a "Test SMTP" button. The user can use it to test the SMTP setup and view logs to check whether it is configured correctly and ready to use. If any errors are found, they will be displayed.
After a successful test, the user can choose to either Save or Cancel the configuration for this specific SMTP.



Subject Manager — Feature Specification
After user click this from left side, on the right side will show all the created Subject Lists. Each Subject List can contain one or multiple subject lines. Tool will use these subject lines during email sending based on the selected subject list and rotation settings. User can create/edit/delete Subject List. When user clicks "Create Subject New List", it will open a small window where user must input the list name (required) and optional short description. After clicking OK, the tool will automatically create a CSV file inside ProjectDirectory/Data/Subject/ folder. For example, if list name is "Test Subject List", then the path will be: ProjectDirectory/Data/Subject/Test Subject List.csv. After selecting any list from the right side, tool will show all subjects under that list as table view format. Each subject can be edited, deleted, or new subject lines can be added. There will be an "Import" button to import subjects from CSV, Excel, or Text file. Whatever file user adds, tool will convert it automatically to CSV and save each subject as one line in the list and if upload again any data on this same list where already subject line appear it will merge automatically and imported after remove duplicate automatically. If user uploads a text file, each line will be stored as one subject line. Also there will be "Add Manually" button – when user clicks it, another window will appear with an input box to enter subjects manually (one per line), and it will support emoji as well. Subjects must support personalization using {ColumnName} (based on user data from leads file), or {{placeholdername}} for software built-in placeholders included faker data all the default placeholder set on configuration page, and also must support spintext using {{{spinword}}} format. User can define spintext from Configurations section. In spintext, user can define one Main Word like: "struggling", and give spintext value like: {struggling|having trouble|finding it hard}, so in subject, user can just write {{{struggling}}} and tool will automatically fill this randomly with any of the defined values during sending. User can define as many spintext as needed. After importing subjects or adding manually, user can also edit/delete/add single or bulk subject lines directly from the table, and changes will be saved automatically to the CSV file. Also from Configuration, user can set how many subject lines to show per page when viewing from UI (pagination). So the tool must support unlimited subjects per list, and unlimited subject lists, full management, full dynamic personalization, emoji, and spintext support.


Add a real-time "Preview" button with each subject to show how the final subject would look after applying:
•	{ColumnName}
•	{{placeholdername}}
•	{{{spinword}}}
This  Helps users validate spintext and personalization instantly before sending.
Highlight {ColumnName}, {{placeholder}}, and {{{spinword}}} in different colors when viewed in the table or editor or in Preview to Makes it visually easier to recognize and edit placeholders..


Search + Filter in Subject Table
•	Add a small search bar above the subject table to filter or find specific lines.
•	Helps manage large subject lists easily.

Import Summary Popup
•	After import, show a small summary:
o	Total imported
o	Duplicates skipped
o	Errors (if any)
•	Gives clear feedback and improves trust.






Messages — Message Template Manager
When the user clicks on Messages from the left-side panel, the right-hand side will display all the existing message templates in a table view format. Each message template is stored as a separate folder under:
ProjectDirectory/Data/Message/{TemplateName}/
This folder structure helps keep things organized, with each template having its own directory for content, configuration, and attachments.

➕ Create New Message Template
Clicking “Create New Template” opens a new window where the user must enter:
•	Template Name (required)
•	Short Description (optional)
After clicking OK, the software automatically creates a folder with the given template name inside:
ProjectDirectory/Data/Message/{TemplateName}/
This folder will be store here everything related to that message template.

Email Editor – WYSIWYG HTML Editor full features with preview button/editor live
Once the template is created, the system opens WYSIWYG HTML Editor email editor. By default, the editor starts with a blank canvas, and the user can design/edit how they want to build the message:
•	Design a full HTML email using full featruees WYSIWYG HTML Editor
•	Use plain text or HTML
•	Can add image within design email template as direct file or can insert also image source link it will need to load automatically and can specify also size/alter text etc everything professionally. 
•	Add only attachments if needed, without writing any content (optional)
There’s a simple checkbox labeled “Enable Content”, which is checked by default. If the user unchecks this, the tool will disable the message body — meaning the template will be used for attachments only.
Users can save the template in any state: blank, HTML, plain text, or attachments only or can even combine all of them wihin a single template.

Design an area where the user can create an email template and add an attachments button to include attachments with the template. The user should be able to add attachments even without any message content if needed.
and also for unsubscribe within message content , user can directly select text as "unsubscribe" and can insert any like of them as single link:
<mailto:unsubscribe@yourdomain.com> = can use direct user specific domain.
<mailto:unsubscribe@{{domain}}> = can use any custom text instead of unsubscribe & default placeholder {{domain}} will automatic replace with picking domain randomly from this default domain placeholder.
<mailto:{{FakerFullName}}@yourdomain.com> = will filup automatically each time with faker full name@domain.com and send.
<mailto:{{FakerFullName}}@{{domain}}> = will filup automatically from faker full name and provided domain randomly.
<mailto:{{campaign}}@yourdomain.com> = will filup campaign name automatically from picking default provided campaign name.
<mailto:{{campaign}}@{{domain}}> = will filup them automatically.
<mailto:unsubscribe@yourdomain.com?{{subject}}=unsubscribe> = {{subject}} will replace with subject text which used to send this email.
<https://yourdomain.com/unsubscribe?email={email}> = email with filup automatically with receipients email.
<https://yourdomain.com/unsubscribe/{{token}}> = {{token}} will filup with uniqe token for each recepients.
<mailto:unsubscribe@yourdomain.com>, <https://yourdomain.com/unsubscribe/{{token}}> = will be both as single header.

Additionally, without selecting any "unsubscribe" text, the user can directly use the default placeholder {{unsubscribe}}. The tool will automatically generate and pick an unsubscribe link randomly from the default provided options, ensuring uniqueness for each one.

Attachments Support
The user can upload one or multiple attachments with any message template. These files will be saved inside the template’s folder.
A message can contain:
•	Just content
•	Just attachments
•	Or both
The tool gives complete flexibility in how the template is used.


The template fully supports:
-Spintext using {{{word}}} format
-personalized placeholders based on lead data (like {email})” (or specify actual column names)
-Built-in default placeholders like {{FakerFirstName}}, {{FakerLastName}}, and more any of default placeholder— all defined in the Configuration section


Template Configuration — After Editor
Once the user clicks Next, the tool will open an advanced configuration window for this specific message template.




Fingerprint Obfuscation
To help bypass spam filters, users can enable a feature called Fingerprint Obfuscation. This option is disabled by default, but when enabled, the tool will automatically insert randomized invisible code into the message, such as:
•	<div style="display:none">random string</div>
•	<span style="font-size:0">invisible</span>
•	Random HTML comments like <!-- abc123 -->
•	Rotating inline CSS styles (e.g., random padding, margin values)
These invisible changes ensure that every time the message is sent, it has a unique HTML fingerprint — even though it looks exactly the same to the recipient. This reduces the chances of being flagged as spam.

Fingerprint Rotation Policy
Along with enabling fingerprinting, the user can choose how often the fingerprint changes. There’s a dropdown with two options:
•	Each time – a new fingerprint is generated for every single email send
•	Custom – the user can define a range like “From 10 to 25 sends,” and the tool will reuse the same fingerprint for a random number of emails within that range before rotating to the next one
•	Skip Sometimes (Optional): A checkbox (default unchecked).
If enabled, the tool will occasionally skip rotation and just use the fingerprints  as originally written in the template means no fingerprints. This adds randomness to avoid pattern detection by spam filters.
This gives flexibility for power users who want more control over delivery behavior.

✨ Emoji Rotation (Optional)
If the user adds any emoji to the message template, the system will detect this automatically and display a clickable option labeled Emoji Rotation, with a dropdown to Enable/Disable it. This option is always disabled by default, even if emojis are present in the message.
If the user enables Emoji Rotation, a new configuration window will open with the following:
Emoji Rotation Setup Window
•	Left Panel: Table showing all current emojis detected in the email template.
•	Right Panel: For each emoji, the user can define alternative emojis to rotate with, separated by commas.
Example:


Current Emoji	Rotate With
😊	🙂, 😁, 😃
🚀	✈️, 🛸, 🛫
The tool will randomly replace each detected emoji with one of the alternatives provided during sending.

Rotation Settings
Below the emoji table, the user can define how the emoji rotation behaves:
•	Rotation Type: Dropdown with two options:
o	Each time — Rotates emojis randomly on every email send
o	Custom — Allows defining a From and To count
Example: Rotate emojis every 5 to 15 emails
•	Skip Sometimes (Optional): A checkbox (default unchecked).
If enabled, the tool will occasionally skip rotation and just use the emoji as originally written in the template. This adds randomness to avoid pattern detection by spam filters.
This feature is designed to make emoji usage feel more natural and undetectable, while still offering variation during sending.



Preview Functionality
Each message template includes a Preview button. When clicked, it renders a real-time preview of the message — showing exactly how it will look after:
•	Applying spintext values
•	Inserting personalization
•	Replacing placeholders
In the preview:
•	{lead_column} values appear in blue
•	{{default placeholders}} in green
•	{{{spintext}}} in orange
This helps users visually identify placeholders and confirm everything looks correct before sending.
Storage Structure Example
Here’s what the file structure looks like for a message template called “WelcomeEmail”:
ProjectDirectory/
└── Data/
    └── Message/
        └── WelcomeEmail/
            ├── email.html          → HTML version (if designed)
            ├── plain.txt           → Plain text version (if used)
            ├── attachments/        → Folder containing all uploaded files
            └── metadata.json       → Stores all settings & configurations

The tool will automatically keep everything inside the right folders — ensuring easy backup, future edits, or sharing.

Search, Pagination, and Organization
As the number of templates grows, the Messages panel will support:
•	Search bar to find templates by name or content
•	Pagination to view templates in batches (10/25/50 per page)
•	Sorting by name, date created, or status
All these options are customizable from the Configuration panel.
Campaign Setup
After finishing all previous steps, the next step is to go to the campaign options where the user can set up a new campaign. On the left side of the window is a panel named "Campaigns". In the right side of this panel, all campaign names are listed in order. Clicking a campaign name opens its tab on the right side, showing a progress bar, counters, and other details. There are also buttons to delete a campaign or create a new one. At the bottom, a small area will display a short description of the selected campaign.


Creating a New Campaign
Clicking "Create New Campaign" opens a small window to enter the campaign name and an optional short description, with OK/Cancel buttons. After confirming, the new campaign appears in the list. From the right-side panel can configure rest in bellow.


SMTP Selection and Configuration
On the right side, there is a "Select SMTP" dropdown. The user can check one or multiple SMTP servers from the list and then click OK/Cancel to confirm. Next to it is a "Configuration" button. Clicking Configure opens a window for SMTP Rotation. There is a dropdown with "Each Mail" or "Custom":
•	Each Mail: The tool automatically rotates through the selected SMTP servers for each email sent.
•	Custom: The user specifies a range (e.g. from 10 to 15). The tool uses each SMTP to send a number of emails within that range before rotating to the next.
The tool ensures each SMTP’s sending limits, headers, etc. are respected. If all smtp limit is exceeded, sending stops and an error/stop message appears. OK/Cancel buttons confirm these SMTP settings.
By default, if multiple SMTPs are selected, the tool will rotate the SMTP for each email. If only one SMTP is selected, that SMTP will be used for all emails.


Leads List and Sending Sequence
Below that is the Leads List selection. There is a dropdown showing all lead list names. The user selects one list. Next to it is a "Configuration" button. By default, emails are sent serially from the first lead to the last. Clicking Configure opens a window for Sending Sequence, with a dropdown offering four options:
•	First to Last: Start sending from the first lead (top row) and finish with the last lead.
•	Last to First: Start from the last lead and finish with the first.
•	Randomly: Pick a random lead each time. The tool will randomly select a lead, send an email, then pick another random lead, and continue until all leads have been emailed.
•	Domain Based Send: The tool extracts all unique email domains from the selected leads list. On the right side, the user will see these domains and can drag to reorder them (for example: outlook.com, yahoo.com, gmail.com). The tool then sends emails to all leads with the first domain in the list, then all with the second domain, and so on in the specified order.
If selected as Domain based send , There is also a "Rotation" checkbox (default off). If enabled, the tool rotates domains with each email. For example, if the domains are ordered as outlook.com, yahoo.com, gmail.com, the tool sends one email to a lead at outlook.com, then one to yahoo.com, then one to gmail.com, then back to outlook.com, and so on until all leads are emailed.
The tool ensures no duplicate emails are sent – each recipient address gets only one email.


Subject Configuration
Next is the Subject option. There is a "Disable/Enable" toggle. By default the subject is enabled. If the user disables the subject, the tool will send emails without any subject, and the subject-selection dropdown becomes non-clickable. When enabled, the user can use a dropdown and checkboxes to select one or multiple subject lines, with OK/Cancel to confirm. A "Configuration" button is on the right.
By default, if multiple subject lines are selected, the tool will rotate the subject with each email. If only one subject is selected, that same subject is used for all emails. Clicking Configure opens a window for Subject Rotation, with a dropdown "Each Time / Custom":
•	Each Time: The subject line will automatically change for each email sent. (Default when multiple subjects are selected.)
•	Custom: The user can set a range (e.g. from 1 to 5). The tool will rotate through the subjects according to that range of emails per subject.
OK/Cancel confirm the subject rotation settings.


Template & Attachments
Next is "Template & Attachments." There is a dropdown listing all message template names. The user can check one or multiple templates (with or without attachments) to select them, and click OK/Cancel. A "Configuration" button is on the right. Clicking it opens a window for Template Rotation, with a dropdown "Each Mail / Custom":
•	Each Mail: The tool rotates automatically between each selected template with every email sent.
•	Custom: The user specifies a range (from X to Y). The tool rotates templates between these counts of emails.
OK/Cancel confirms the template configuration.




Custom Tracking
Below that is "Custom Tracking" (disabled by default). If the user enables it and clicks Configure, a window opens with tracking settings:
•	Tracking Domain/Subdomain: The user enters their main tracking domain or subdomain (used for the tracking panel/API).
•	API Key: The user enters the API key for that tracking domain. This key is used to submit data to the database and read counts for opens, clicks, or unsubscribes.
Another option is when to read/submit tracking data: a dropdown "Before/After send". By default it is set to "Before". The user can choose to submit data either before or after send.
Then there is how often to perform the tracking API call, with a dropdown "Every/Custom":
•	Every: If set to "Before/Every", the tool submits/reads data via API before sending every email.
•	Custom: Two input boxes appear for "From" and "To" counts. For example, if set to "Before/Custom" from 1 to 5, the tool will prepare 1 email, submit its tracking data, and send it; then prepare 5 emails, submit data for those 5, and send them. The tool submits/reads data in batches based on the custom range.
OK/Cancel to save these tracking settings.


Email Open Tracking
Another option is Email Open tracking. Clicking its Configure button opens a window with a text box (one URL per line) for the tracking URL format. Examples (one per line) might be:
https://domain.com/open?{{uuid}}&{{campaign}}
https://domain2.com/open?{{uuid}}&{email}
https://domain3.com/open?{email}
The user can customize as many formats as needed using placeholders or columns from the leads file. Click OK/Cancel to save these open-tracking settings.

Email Click Tracking
Next is Email Click tracking. Clicking Configure opens a window with:
•	Specify Link: A dropdown with "All" or "Custom".
o	All (default): All links in the message will be tracked (including any placeholders or randomly/ default provided placeholder generated links).
o	Custom: Shows a list of all unique links used in the templates for this campaign (with checkboxes). The user can select which specific links to track.
Below is a text box to specify the click-tracking URL format (one per line, each with single or multiple domains). For example, default lines may appear as:
https://domain.com/click?uid={{uuid}}&cid={{CAMPAIGN}}&redirect={{ENCODED_URL}}
https://domain2.com/click?uid={{uuid}}&cid={{CAMPAIGN}}&email={EMAIL}&fname={FIRST_NAME}&redirect={{ENCODED_URL}}
The user can add, edit, or delete formats (one per line). Supported all the default placeholders and uploaded leads file columns name as placeholder, Placeholders work as follows:
•	{{uuid}} – a unique ID generated for each email/lead.
•	{{CAMPAIGN}} – the campaign name or ID provided on default placeholder config (spaces are handled to fit URLs).
•	{{ENCODED_URL}} – the URL from the email template, URL-encoded.
•	{EMAIL} – the recipient’s email (from the leads file).
•	{FIRST_NAME} – the recipient’s first name (from the leads file). (this just as example, user may used any others columns name as placeholder from their uploaded leads file data/columns)
Click OK/Cancel to save the click-tracking settings. Another OK/Cancel is then used to save the entire campaign configuration.
The tracking server (to be implemented separately) will handle the tracking. The sender tool simply generates and sends the tracking links and rest. When a recipient opens or clicks, the tracking server records it.

Custom Headers
On the right side of the campaign setup, there is a "Custom Header" option (default disabled). If enabled and Configure is clicked, a window opens listing header options. Each header has its own settings (Disable/Enable, Configure, etc.). Below is a summary of each header option:
Message-ID
•	Enable/Disable: Dropdown (default disabled) and a Configure button.
•	Configure: Opens a window with formats (one per line), for example:
o	<{{uuid}}@{{domain}}>
o	<{{timestamp}}.{{random}}@{{domain}}>
o	<{{timestamp}}-{{user_id}}@{{domain}}>
o	<{{campaign}}-{{batch}}-{{uuid}}@{{domain}}>
o	<{{random_alphanum}}@{{domain}}>
o	<{{custom_string}}@{{domain}}>
o	<{{date}}-{{sequence}}@{{domain}}>
o	<{{hash}}@{{domain}}>
o	<{{email}}-{{uuid}}@{{domain}}>
o	<{{FakerFullName}}-{{sequence}}@{{domain}}>
o	<{{email}}.{{random_alphanum}}@{{domain}}>
o	<{{FakerCompany}}-{{uuid}}@{{domain}}>
o	<{{email}}-{{list_name}}-{{counter}}@{{domain}}>
o	<{{ColumnName}}-{{uuid}}@{{domain}}> (use an actual column name)
o	<{{FakerWord}}-{{uuid}}@{{domain}}>
The tool will automatically rotate through these formats for each email. The user can add or remove lines, using placeholders, but each must end in @{{domain}}. (the domain may get from default placeholder configuration with one per line will use them randomly each time)

If The following placeholders have custom input options (one per line) can set from default config and also can do overwrite if needed:
o	{{random_alphanum}} – set minimum/maximum length for the string.
o	{{batch}} – enter batch names.
o	{{campaign}} – enter campaign names.
o	{{custom_string}} – enter custom text strings.
o	{{list_name}} – enter list names.
If custom values are provided, they override the placeholder. Otherwise defaults are used.
•	Format Rotation: Dropdown "Each Mail / Custom". "Each Mail" rotates the format each email. "Custom" lets you specify a range (from X to Y) of emails per format.
•	Header Use Policy: Dropdown "Must use each time / Optional".
o	Must use: The header is added to every email.
o	Optional: The header may be skipped some times during rotation. The user can set minimum and maximum number of headers to use each time (e.g. min 3, max 5). The tool will always use at least the minimum, up to the maximum, and rotate the rest. If "Must use" is selected, the tool will adjust the minimum count so it cannot be lower than required.
Click OK/Cancel to confirm.


X-Tracking-ID
•	Enable/Disable: Dropdown (default disabled) and Configure.
•	Configure: Formats (one per line), e.g.:
o	{{uuid}}
o	{{hash}}
o	{{random}}
o	{{random_alphanum}}
o	{{FakerUUID}}
o	{{FakerRandomNumber}}
o	{{timestamp}}
o	{{date}}-{{sequence}}
o	{{timestamp}}-{{counter}}
o	{{year}}{{month}}{{day}}-{{hour}}{{minute}}{{second}}
o	{{email}}-{{uuid}}
o	{{email}}-{{timestamp}}
o	{{FakerFirstName}}-{{FakerLastName}}-{{uuid}}
o	{{campaign}}-{{batch}}-{{uuid}}
o	{{campaign}}-{{timestamp}}
o	{{campaign}}-{{email}}
o	{{campaign}}-{{batch}}-{{email}}-{{uuid}}
o	{{hash}}-{{counter}}
o	{{user_id}}-{{uuid}}
o	{{list_name}}-{{counter}}
o	{{column1}}-{{column2}}-{{uuid}}
Users can add/edit/remove formats and combine placeholders as needed. The same custom-input placeholders ({{random_alphanum}}, {{batch}}, etc.) apply here as well.
•	Format Rotation: "Each Mail / Custom" (as above).
•	Header Use Policy: "Must use each time / Optional" (as above).
Click OK/Cancel.


X-Campaign-ID
•	Enable/Disable: Dropdown (default disabled) and Configure.
•	Configure: The user can enter multiple campaign names or IDs (one per line) under "Static Campaign Name/ID." They can also include placeholders (Faker, default, or columns) in these lines.
•	Format Rotation: "Each Mail / Custom" (rotates the X-Campaign-ID value each email or custom range).
•	Header Use Policy: "Must use each time / Optional" (as above).
Click OK/Cancel.


X-UID
•	Enable/Disable: Dropdown and Configure.
•	Configure: Works like the other headers. The user can enter formats or values (one per line) for X-UID.
•	Format Rotation & Use Policy: Same "Each Mail/Custom" and "Must/Optional" options apply.
Click OK/Cancel.


X-Mailer
•	Enable/Disable: Dropdown and Configure.
•	Configure: A list of common X-Mailer values is shown (one per line), for example:
o	Microsoft Outlook 16.0
o	Microsoft Outlook 15.0
o	Microsoft Outlook 14.0
o	Microsoft Outlook Express 6.00.2900.2869
o	Microsoft Windows Live Mail 16.4.3528.0331
o	Microsoft Exchange Server 2016
o	Microsoft Exchange Server 2013
o	Microsoft-MacOutlook/16.81.0.24062400
o	Apple Mail (2.3696.100.31)
o	Apple Mail (2.3654.120.0.1.13)
o	iPhone Mail (17G68)
o	iPhone Mail (20A5358e)
o	iPad Mail (15E148)
o	Mozilla Thunderbird 115.3.1
o	Mozilla Thunderbird 102.10.0
o	Mozilla Thunderbird 91.13.1
o	Android Mail 9.0.0.20702
o	Samsung Email 6.1.00.16
o	Gmail Web
o	YahooMailWebService/0.8.111_71
o	Airmail 3.6.70 (527)
o	The Bat! (v9.5.1)
o	The Bat! (v7.4.16)
o	Lotus Notes Release 8.5
o	Lotus Notes Release 9.0
o	Zimbra 8.8.15_GA_3869
o	Roundcube Webmail/1.6.2
o	Roundcube Webmail/1.4.13
o	Alpine 2.23 (LNX 1166 2018-08-05)
o	Postbox 7.0.42
o	Claws Mail 3.18.0 (GTK+ 2.24.32; x86_64-pc-linux-gnu)
o	Evolution 3.46.4-1
o	KMail/5.21.3 (20.12.3)
o	Mutt/1.14.7 (2020-09-21)
o	MailMate (5878)
o	PHPMailer 6.7.1 (https://github.com/PHPMailer/PHPMailer)
o	PHPMailer 5.2.27 (https://github.com/PHPMailer/PHPMailer)
o	SwiftMailer 6.3.0
o	SwiftMailer 5.4.12
o	Mailgun PHP 4.0.0
o	SendGrid Mailer
o	Amazon Simple Email Service (SES)
o	MailChimp Mailer
o	Mailgun Mailer
o	Sendmail 8.16.1
o	Sendmail 8.15.2
o	Exim 4.96
o	Exim 4.94
o	Postfix 3.6.4
o	Postfix 3.4.13
o	Sympa 6.2.60
o	MailEnable Standard 10.36
The user can add or remove items in this list. These are the default values that will appear in the UI.
•	X-Mailer Rotation: Dropdown "Each Mail / Custom" (rotate each email or set a range).
•	Header Use Policy: "Must use each time / Optional" (as above).
Click OK/Cancel.

X-Origin
•	Enable/Disable: Dropdown and Configure.
•	Configure: The user can enter values one per line, for example:
o	webmail.google.com
o	outbound-mail.company.com
o	app-server-01.internal
o	relay01.hostingprovider.net
o	{{FakerIPv4}}
Any custom text or placeholders are allowed (Faker, default, or lead columns).
•	X-Origin Rotation: "Each Mail / Custom" (rotate value each email or set range).
•	Header Use Policy: "Must use each time / Optional" (as above).
Click OK/Cancel.

X-Email-Type
•	Enable/Disable: Dropdown and Configure.
•	Configure: The user enters values one per line. Example types include:
o	Transactional
o	Marketing
o	Notification
o	Alert
o	Reminder
o	Welcome
o	PasswordReset
o	AccountActivation
o	Receipt
o	Invoice
o	Newsletter
o	Survey
o	Invitation
o	System
o	Support
o	Promotion
Placeholders (like {{FakerWord}} or lead columns) are also supported in these values.
•	X-Email-Type Rotation: "Each Mail / Custom".
•	Header Use Policy: "Must use each time / Optional".
Click OK/Cancel.

X-Campaign-Name
•	Enable/Disable: Dropdown and Configure.
•	Configure: The user enters lines for campaign names, e.g.:
o	SummerSale2025
o	BlackFridayPromo
o	WelcomeSeries
o	JulyNewsletter
o	BlackFridayPromo-{{uuid}}
o	{{campaign}}
o	{{FakerWord}}
o	{{FakerCompany}}-{{campaign}}
o	{{campaign}}-{{batch}}
These are examples. The user can also include placeholders in these values. There are two additional input fields to override the default values of {{campaign}} and {{batch}} if desired.
•	Rotation: "Each Mail / Custom".
•	Header Use Policy: "Must use each time / Optional".
Click OK/Cancel.


Auto-Submitted
•	Enable/Disable: Dropdown and Configure.
•	Configure: A dropdown with options:
o	auto-generated
o	auto-replied
o	no
o	random
If "auto-generated" or "auto-replied" is selected, that value is used. "No" means no Auto-Submitted header. If "random" is chosen, the user can specify a range (from X to Y), and the tool will randomly choose between "auto-generated", "auto-replied", or "no" according to that range.
•	Header Use Policy: "Must use each time / Optional".
Click OK/Cancel.

Precedence
•	Enable/Disable: Dropdown and Configure.
•	Configure: A dropdown with options:
o	bulk
o	list
o	junk
o	normal
o	random
The user selects one. If "random" is selected, two input boxes appear for "From" and "To". The tool will then rotate randomly among "bulk", "list", "junk", and "normal" for each email, within the specified count range.
•	Header Use Policy: "Must use each time / Optional".
Click OK/Cancel.


Priority
•	Enable/Disable: Dropdown and Configure.
•	Configure: A dropdown with options:
o	high
o	normal
o	low
o	random
If "random" is selected, the user specifies a range (From/To), and the tool rotates between high/normal/low within that range.
•	Header Use Policy: "Must use each time / Optional".
Click OK/Cancel.


X-Priority
•	Enable/Disable: Dropdown and Configure.
•	Configure: A dropdown with options:
o	1 (Highest)
o	2 (High)
o	3 (Normal)
o	4 (Low)
o	5 (Lowest)
o	random
If "random" is selected, a range is specified and the tool rotates among 1–5 (with their labels) within that range.
•	Header Use Policy: "Must use each time / Optional".
Click OK/Cancel.

Importance
•	Enable/Disable: Dropdown and Configure.
•	Configure: A dropdown with options:
o	high
o	normal
o	low
o	random
If "random" is selected, a range is set and the tool rotates among high/normal/low within that range.
•	Header Use Policy: "Must use each time / Optional".
Click OK/Cancel.


X-Auto-Response-Suppress
•	Enable/Disable: Dropdown and Configure.
•	Configure: A dropdown with:
o	All (suppress all automatic responses)
o	OOF (suppress Out of Office replies)
o	AutoReply (suppress automatic replies)
o	AutoForward (suppress auto-forwarding)
o	DR (suppress Delivery Receipts)
o	RN (suppress Read Notifications)
o	NRN (suppress Non-Read Notifications)
o	Random
If "Random" is selected, the tool will randomly pick one of the above for each email.
•	Type Rotation: Dropdown "Each Time / Custom" – "Each Time" rotates the chosen type with each email; "Custom" allows setting a range (From/To) for how often to rotate.
•	Header Use Policy: "Must use each time / Optional".
Click OK/Cancel.


Unsubscribe Header
•	Enable/Disable: Dropdown and Configure.
•	Configure: The user can enter unsubscribe header formats (one per line). They can also use the default {{unsubscribe}} placeholder. Also can overwrite with directly added as Examples:
o	<mailto:unsubscribe@yourdomain.com>
o	<mailto:unsubscribe@{{domain}}>
o	<mailto:{{FakerFullName}}@yourdomain.com>
o	<mailto:{{FakerFullName}}@{{domain}}>
o	<mailto:{{campaign}}@yourdomain.com>
o	<mailto:{{campaign}}@{{domain}}>
o	<mailto:unsubscribe@yourdomain.com?{{subject}}=unsubscribe>
o	<https://yourdomain.com/unsubscribe?email={email}>
o	<https://yourdomain.com/unsubscribe/{{token}}>
o	<mailto:unsubscribe@yourdomain.com>, <https://yourdomain.com/unsubscribe/{{token}}> (two values on one line)
The tool will randomly pick one format for each email and generate unique unsubscribe links if using placeholders. User-added lines will overwrite the default.
•	Format Rotation: "Each Time / Custom" (rotate format each email or set a range).
•	Header Use Policy: "Must use each time / Optional".
Click OK/Cancel.
•	List-Unsubscribe-Post (One-Click): A dropdown with "Disable/Enable/Random." "Disable" omits the header, "Enable" includes it, "Random" means it will be included randomly.

Add More Headers
There is an "Add more header" button. Clicking it opens an input box for a custom header name (e.g. "X-Custom-Header"). A remove (–) button appears to delete it if needed. A Configure button opens a window where the user can enter custom values (one per line) or use text combined with any placeholders. Below that, there is a "Rotation" option ("Each Mail/Custom") for the custom header, just like the others.

Header Use Limit
Below all headers is "Header Use Limit". A dropdown has "All" or "Custom":
•	All: Use all enabled headers for each email.
•	Custom: The user specifies a minimum and maximum number of headers to use per email. The minimum is automatically at least the number of headers marked "Must use". The user can increase the minimum if desired (but not decrease below the required amount). The maximum can be any number up to the total headers. Optional headers will rotate among themselves up to that maximum.
There is also a "Disable Sometimes" checkbox (default off). If checked, even headers marked "Must use" may be omitted some of the time, so some emails are sent with no custom headers at all. This completely randomizes the header usage, which can help avoid spam filters.


Sending Mode
Below the header options is the "Sending Mode" dropdown with four choices: Single Mode, Batch Mode, Date & Time Mode, and Spike Mode. Only one can be selected at a time:
•	Single Mode: Sends emails one by one with a delay between each. The user enters "Delay from" and "Delay to" (with units sec/min/hour). For example, if Delay from 10 sec to Delay to 20 sec, the tool will send one email, then wait a random time between 10 and 20 seconds, then send the next, and so on, until all emails are sent.
•	Batch Mode: Sends emails in batches. The user specifies a batch size range (Min and Max, e.g. 10 to 20). Each send attempt will send between 10 and 20 emails at once. There is also a "Batch Delay" (from/to with sec/min/hour) meaning the tool waits that delay between batches.
•	Date & Time Mode: Sends emails on specific date/time ranges. The UI shows current date/time. The user selects a "From Date & Time" and a "To Date & Time" using calendars. Then the user sets a send limit (e.g. 100). The tool automatically calculates delays to send exactly 100 emails between the From and To times. The UI will display the total leads and how many remain after that limit, so the user knows how many emails are left. The user can add multiple date/time ranges (click "Add more") with their own limits. If the configuration does not cover all leads (i.e., it would send fewer emails than total leads), a warning will appear that not all leads will be emailed.
•	Spike Mode: Allows a day-by-day send plan. For each day, the user specifies how many emails to send (e.g. Day 1: 100). The UI shows the total leads and remaining after each day's limit. The tool will send the specified number of emails on each day. For example, if Day 1 is 100 emails, the tool will send 100 emails within that 24-hour day (adjusting speed as needed). The user can click "Add more" to add Day 2, Day 3, etc., each with its own limit. The tool follows this daily schedule accordingly.

Scheduling
Below Sending Mode is a "Scheduling" toggle (Disable/Enable). By default scheduling is off. If enabled, the user picks a date and time (with hours/minutes, am/pm) when the campaign should start. After clicking Start, the tool will wait (count down) until the scheduled date/time and then begin sending. If scheduling is disabled, sending starts immediately when Start is clicked.

Status, Progress, and Controls
Below that, live status counters are shown:
•	Total Leads
•	Total Subjects
•	Total SMTPs
•	Total Message Templates
•	Sent Success
•	Sent Failed
•	Remaining
•	Total Opens
•	Total Clicks
If tracking (opens/clicks) is disabled, those counters show as "Off". All counters update in real time. A progress bar below these shows completion percentage in real time.
Below the counters are buttons:
•	Start: Begin the campaign.
•	Stop: Stops the campaign (enabled only after starting).
•	Pause: Pauses sending (enabled only while sending).
•	Resume: Resumes sending (enabled only when paused).
•	Save as Draft: Saves the current configuration and progress, allowing the campaign to be continued later.
All campaign data (configuration, settings, reports, status) is saved as JSON files inside the campaign’s folder. If the tool closes unexpectedly, the user can restart and resume the campaign where it left off, with all counters and data intact.

Reports
On the right side of the campaign setup page is a "Report" tab. It displays a table of all send details: status (success/failed), SMTP used, subject, headers, message template, lead data, date/time, etc. There is an export button (Excel/CSV). By default, a CSV report is automatically saved in the campaign folder and updated live after each send. The report includes columns for SMTP, headers, and all columns from the leads file, showing exactly the same data as the leads file for each sent email.




Important:
After the software is fully completed, I will require two types of documentation. First, a detailed technical guide explaining how to compile the software into a standalone .exe file using Nuitka, PyInstaller, or Cython. This guide must include all necessary steps such as dependency setup, environment configuration, directory structure, compilation commands, handling of resource files like images and JSON, and any troubleshooting tips for common issues. The purpose is to ensure I can recreate the executable version of the software independently, without errors or broken functionality.
Secondly, I will need a comprehensive, user-friendly documentation written in natural language, just like a human would explain things — not robotic or overly technical. This user guide should cover every single feature and option in the software. It should explain what each feature does, how to access it, where to click, what happens when certain options are selected, and how different settings interact. For example, if enabling one setting unlocks additional options, that behavior must be clearly described. It should also include practical examples and usage scenarios to help users understand when and how to use each feature. The goal is to make the software fully understandable and accessible, even to users who aren’t technical.

Clearification:
1. File Structure
You mentioned both:
•	ProjectDirectory/Data/SMTP/Server Name.json
•	SMTP lists (like Leads lists)
Should SMTPs be organized in lists or individual files? The requirements seem to suggest both approaches.
Clarification:  each smtp will save separetly with its own configuration settings etc, and in ui will show by serially like a list of smtp server each smtp can add/edit/modify individually.

2. WYSIWYG Editor
For the HTML email editor, do you have a preference for the editor library? Options include:
•	TinyMCE
•	CKEditor
•	Quill
•	Custom implementation
Clarification: Custom implementation with  fully all the options supported for html message template writing and preview.

3. Faker Integration
Should I use the Python Faker library for generating fake data, or implement custom generators?
Clarification: you must have to use faker library as well as I describe this.

4. UI Framework
Use pyqt6 with qss file as design

5. Threading Architecture
For multi-campaign support, should each campaign run in:
•	Separate threads
•	Separate processes
•	Async/await pattern
•	Thread pools
Clarification: each campoaing will work individually with its own thread each one will not affect others one, each single campaign manage/add/edit/run or can do anything individually, and can run multiple campaign at a same time each one will work with their own configuration/thread or whatever needed.

6. Configuration Management
The "Default Placeholder.txt" and "spinword.txt" files suggest a configuration system. Should these be:
•	Editable through the GUI
•	Stored as JSON files
•	Both file-based and GUI-editable
Clarification: both, store + editable from gui and edited data will update automatically on this store data and also reset option for to do reset everything as default.
And make sure read/write do same work even package as exe.

7. Email Sending
Should I implement:
•	Direct SMTP sending
•	Queue-based sending
•	Both approaches
Clarification: based on overall requirements you can do whatever is required, just make sure each single features work perfectly without any issue, and as it will be computer windows based software so think about it as its not any web server based, I may later convert this as web based application with database or others thing for right now I don’t need database or such as its computer software for only windows os.

8. Error Handling
For SMTP failures, campaign errors, etc., do you want:
•	Detailed logging
•	User notifications
•	Retry mechanisms
•	All of the above
  Clarification: all of above details loggin and user notification with ui only and retry mechanism with customizable option from ui so user can set retry count/limit etc that is needed.




1.	File Permissions: Since this will be packaged as an EXE, should the data files be stored in:
o	The same directory as the EXE
o	User's AppData folder
o	A configurable data directory
Clarification: the same directory as the exe and will create file/folder whatever needed if not appear on this path automatically.

1.	Browser Integration: For the embedded browser interface, should I use:
o	System default browser (opens in external window)
o	Embedded browser component (like CEF/Chromium within the app)
o	Both options available to user
Clarification: No need to open any external window, do everything inside within app like cef or chromium or whatever needed.

1.	Campaign Data Persistence: Should campaign configurations and progress be:
o	Saved automatically
o	Saved on user action
o	Both (auto-save + manual save)
Clarification: Both

1.	SMTP Testing: Should there be a "Test SMTP Connection" feature before running campaigns?
Clarification: no need from campaign page/section, smtp related test or such others will handle directly from this smtp page/options, campaign setup is just place to combination and configuration everything and run or schedule or whatever. So no need smtp testing or such related from campaign setup page.

1.	Email Templates: Should templates be:
o	Stored as separate files
o	Embedded in campaign configurations
o	Both options available
Clarification: as I mentioned from email template section/page/features can do design/edit /add email template and each template with all the files/attachments/image etc will be store separet folder for each email template, and from campaign setup page user can select which want to use, and tool will directly use from the message template folder which is selected with randomly or whatever configure by user.






