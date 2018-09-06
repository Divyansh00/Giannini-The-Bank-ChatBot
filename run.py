import main
while True:
    message = unicode("User: "+str(raw_input()),"utf-8")
    ##print(message)
    if message == unicode("User: Thankyou","utf-8") or message ==  unicode("User: Thanks","utf-8") or message ==  unicode("User: thankyou","utf-8") or message ==  unicode("User: thanks","utf-8"):
        print("Bot: Welcome, I am exiting")
        break
    main.response(message)
    
    
