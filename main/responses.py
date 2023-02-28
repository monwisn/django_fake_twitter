from simple_chatbot.responses import GenericRandomResponse


class GreetingResponse(GenericRandomResponse):
    choices = ("Hi, how can I help you?",
               "Hey friend. How are you? How can I help you?",
               "Hello, how are you?",
               "Hey there!",
               )


class GoodbyeResponse(GenericRandomResponse):
    choices = ("See you later.",
               "Thanks for visiting.",
               "See ya! Have a nice day.",
               "Bye Bye",
               "Goodbye",
               )
