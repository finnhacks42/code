import smtplib
 
def sendemail(from_addr, to_addr_list,subject, message,login, password,smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems

sendemail('hollycomputes@gmil.com',['finnlattimore@gmail.com'],'Holly is alive','Holly is computing','hollycomputes@gmail.com','silentdog')
print "DONE"
