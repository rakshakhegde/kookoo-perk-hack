# Kookoo Perk Hack
Read the conversations below to understand how the demo works.

While conversing please be loud and clear and please be patient for the response as the server needs to process for the first time. Call **08067947469** for the demo.

Basically, this project aims to bring Google Now from online to completely offline state. You can book a cab, order food or just about collect any other kind of information by calling the number mentioned above.

Please do check the call flow specified below but generally the call workflow goes like this: You state the query, bot responds with a series of questions to complete your request and finally confirmation message is sent to your phone after you hangup.

###Tech stack used:
- The backend SIP is hosted on **Google App Engine**
- For the speech to text (S2T) analysis, **IBM's Watson Service: Speech to Text** is used
- For encoding the recorded voice from mp3 to flac format, which is taken as input by IBM's S2T service, a VM is hosted on an **Amazon EC2 instance**

###Potential Applications of this project
- Getting info about virtually anything, like weather, prices, biz market stats, edu content, etc by leveraging Google APIs
- Book a Uber cab
- Order food with third-party APIs
- **Major non-profit** side of this project could be that farmers of India could call and retrieve market prices of agricultural items like rice, pulses and many other items so that under-price selling of goods can be stopped and so that farmers can get rightfully paid for all their hard work.

Now, let's have a conversation.
Conversaton 1:
```
Bot: Query *beep*
You should say: Order Uber cab
Bot: Booking an Uber cab. State your pickup and end location
You: From Electronic City to Majestic
Bot: You will be picked up from Electronic City and dropped off at Majestic. Please Wait.

"Perk" Audio AD plays here and sorry as it was poorly recorded from an Youtube ad

Bot: Your total fare is ___ rupees. Details of the driver will be sent by SMS to you. Have a happy journey.
```

Conversation 2:
```
Bot: What would you like to eat?
You should say: Pizza
Bot: Pizza confirmed. Any particular toppings you would like?
You: Tomatoes
Bot: Would you like pickup or delivery?
You: Pickup
Bot: You can pick up your Pizza at your nearest Dominos. Please wait.

"Perk" Audio AD plays here and sorry as it was poorly recorded from an Youtube ad

You: Your total price is ___ rupees. Details will be sent as SMS to you. Bon Appetite.
```
