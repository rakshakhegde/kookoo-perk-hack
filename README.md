# Kookoo Perk Hack
Read the conversations below to understand how the demo works.

While conversing please be loud and clear and please be patient for the response as the server needs to process for the first time. Call **08067947469** for the demo.

Basically, this project aims to bring Google Now from online to completely offline state. You can book a cab, order food or just about collect any other kind of information by calling the number mentioned above.

Tech stack used:
- The backend SIP is hosted on **Google App Engine**
- For the speech to text (S2T) analysis, **IBM's Watson Service: Speech to Text** is used
- For encoding the recorded voice from mp3 to flac format, which is taken as input by IBM's S2T service, a VM is hosted on an **Amazon EC2 instance**

Now, let's have a conversation.
Conversaton 1:

*Bot*: Query *beep*
*You*: Order Uber cab
*Bot*: Booking an Uber cab. State your pickup and end location
*You*: From Electronic City to Majestic
*Bot*: You will be picked up from Electronic City and dropped off at Majestic
**"Perk" Audio AD plays here and BTW sorry as it was poorly recorded from an Youtube ad**
